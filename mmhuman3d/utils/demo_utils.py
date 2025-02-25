import colorsys
import os
from collections import defaultdict
from contextlib import contextmanager
from functools import partial
from pathlib import Path

import mmcv
import numpy as np
from mmcv import Timer
from scipy import interpolate

from mmhuman3d.core.post_processing import build_post_processing

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal


def xyxy2xywh(bbox_xyxy):
    """Transform the bbox format from x1y1x2y2 to xywh.

    Args:
        bbox_xyxy (np.ndarray): Bounding boxes (with scores), shaped (n, 4) or
            (n, 5). (left, top, right, bottom, [score])

    Returns:
        np.ndarray: Bounding boxes (with scores),
          shaped (n, 4) or (n, 5). (left, top, width, height, [score])
    """
    if not isinstance(bbox_xyxy, np.ndarray):
        raise TypeError(
            f'Input type is {type(bbox_xyxy)}, which should be numpy.ndarray.')
    bbox_xywh = bbox_xyxy.copy()
    bbox_xywh[..., 2] = bbox_xywh[..., 2] - bbox_xywh[..., 0]
    bbox_xywh[..., 3] = bbox_xywh[..., 3] - bbox_xywh[..., 1]

    return bbox_xywh


def xywh2xyxy(bbox_xywh):
    """Transform the bbox format from xywh to x1y1x2y2.

    Args:
        bbox_xywh (np.ndarray): Bounding boxes (with scores), shaped
        (n, 4) or (n, 5). (left, top, width, height, [score])

    Returns:
        np.ndarray: Bounding boxes (with scores),
          shaped (n, 4) or (n, 5). (left, top, right, bottom, [score])
    """
    if not isinstance(bbox_xywh, np.ndarray):
        raise TypeError(
            f'Input type is {type(bbox_xywh)}, which should be numpy.ndarray.')
    bbox_xyxy = bbox_xywh.copy()
    bbox_xyxy[..., 2] = bbox_xyxy[..., 2] + bbox_xyxy[..., 0] - 1
    bbox_xyxy[..., 3] = bbox_xyxy[..., 3] + bbox_xyxy[..., 1] - 1

    return bbox_xyxy


def box2cs(bbox_xywh, aspect_ratio=1.0, bbox_scale_factor=1.25):
    """Convert xywh coordinates to center and scale.

    Args:
    bbox_xywh (numpy.ndarray): the height of the bbox_xywh
    aspect_ratio (int, optional): Defaults to 1.0
    bbox_scale_factor (float, optional): Defaults to 1.25
    Returns:
        numpy.ndarray: center of the bbox
        numpy.ndarray: the scale of the bbox w & h
    """
    if not isinstance(bbox_xywh, np.ndarray):
        raise TypeError(
            f'Input type is {type(bbox_xywh)}, which should be numpy.ndarray.')

    bbox_xywh = bbox_xywh.copy()
    pixel_std = 1
    center = np.stack([
        bbox_xywh[..., 0] + bbox_xywh[..., 2] * 0.5,
        bbox_xywh[..., 1] + bbox_xywh[..., 3] * 0.5
    ], -1)

    mask_h = bbox_xywh[..., 2] > aspect_ratio * bbox_xywh[..., 3]
    mask_w = ~mask_h

    bbox_xywh[mask_h, 3] = bbox_xywh[mask_h, 2] / aspect_ratio
    bbox_xywh[mask_w, 2] = bbox_xywh[mask_w, 3] * aspect_ratio
    scale = np.stack([
        bbox_xywh[..., 2] * 1.0 / pixel_std,
        bbox_xywh[..., 3] * 1.0 / pixel_std
    ], -1)
    scale = scale * bbox_scale_factor

    return center, scale


def convert_crop_cam_to_orig_img(cam: np.ndarray,
                                 bbox: np.ndarray,
                                 img_width: int,
                                 img_height: int,
                                 aspect_ratio: float = 1.0,
                                 bbox_scale_factor: float = 1.25,
                                 bbox_format: Literal['xyxy', 'xywh',
                                                      'cs'] = 'xyxy'):
    """This function is modified from [VIBE](https://github.com/
    mkocabas/VIBE/blob/master/lib/utils/demo_utils.py#L242-L259). Original
    license please see docs/additional_licenses.md.

    Args:
        cam (np.ndarray): cam (ndarray, shape=(frame, 3) or
        (frame,num_person, 3)):
        weak perspective camera in cropped img coordinates
        bbox (np.ndarray): bbox coordinates
        img_width (int): original image width
        img_height (int): original image height
        aspect_ratio (float, optional):  Defaults to 1.0.
        bbox_scale_factor (float, optional):  Defaults to 1.25.
        bbox_format (Literal['xyxy', 'xywh', 'cs']): Defaults to 'xyxy'.
            'xyxy' means the left-up point and right-bottomn point of the
            bbox.
            'xywh' means the left-up point and the width and height of the
            bbox.
            'cs' means the center of the bbox (x,y) and the scale of the
            bbox w & h.
    Returns:
        orig_cam: shape = (frame, 4) or (frame, num_person, 4)
    """
    if not isinstance(bbox, np.ndarray):
        raise TypeError(
            f'Input type is {type(bbox)}, which should be numpy.ndarray.')
    bbox = bbox.copy()
    if bbox_format == 'xyxy':
        bbox_xywh = xyxy2xywh(bbox)
        center, scale = box2cs(bbox_xywh, aspect_ratio, bbox_scale_factor)
        bbox_cs = np.concatenate([center, scale], axis=-1)
    elif bbox_format == 'xywh':
        center, scale = box2cs(bbox, aspect_ratio, bbox_scale_factor)
        bbox_cs = np.concatenate([center, scale], axis=-1)
    elif bbox_format == 'cs':
        bbox_cs = bbox
    else:
        raise ValueError('Only supports the format of `xyxy`, `cs` and `xywh`')

    cx, cy, h = bbox_cs[..., 0], bbox_cs[..., 1], bbox_cs[..., 2] + 1e-6
    hw, hh = img_width / 2., img_height / 2.
    sx = cam[..., 0] * (1. / (img_width / h))
    sy = cam[..., 0] * (1. / (img_height / h))
    tx = ((cx - hw) / hw / (sx + 1e-6)) + cam[..., 1]
    ty = ((cy - hh) / hh / (sy + 1e-6)) + cam[..., 2]

    orig_cam = np.stack([sx, sy, tx, ty], axis=-1)
    return orig_cam


def convert_bbox_to_intrinsic(bboxes: np.ndarray,
                              img_width: int = 224,
                              img_height: int = 224,
                              bbox_scale_factor: float = 1.25,
                              bbox_format: Literal['xyxy', 'xywh'] = 'xyxy'):
    """Convert bbox to intrinsic parameters.

    Args:
        bbox (np.ndarray): (frame, num_person, 4), (frame, 4), or (4,)
        img_width (int): image width of training data.
        img_height (int): image height of training data.
        bbox_scale_factor (float): scale factor for expanding the bbox.
        bbox_format (Literal['xyxy', 'xywh'] ): 'xyxy' means the left-up point
            and right-bottomn point of the bbox.
            'xywh' means the left-up point and the width and height of the
            bbox.
    Returns:
        np.ndarray: (frame, num_person, 3, 3), (frame, 3, 3) or (3,3)
    """
    if not isinstance(bboxes, np.ndarray):
        raise TypeError(
            f'Input type is {type(bboxes)}, which should be numpy.ndarray.')
    assert bbox_format in ['xyxy', 'xywh']

    if bbox_format == 'xyxy':
        bboxes = xyxy2xywh(bboxes)

    center_x = bboxes[..., 0] + bboxes[..., 2] / 2.0
    center_y = bboxes[..., 1] + bboxes[..., 3] / 2.0

    W = np.max(bboxes[..., 2:], axis=-1) * bbox_scale_factor

    num_frame = bboxes.shape[0]
    if bboxes.ndim == 3:
        num_person = bboxes.shape[1]
        Ks = np.zeros((num_frame, num_person, 3, 3))
    elif bboxes.ndim == 2:
        Ks = np.zeros((num_frame, 3, 3))
    elif bboxes.ndim == 1:
        Ks = np.zeros((3, 3))
    else:
        raise ValueError('Wrong input bboxes shape {bboxes.shape}')

    Ks[..., 0, 0] = W / img_width
    Ks[..., 1, 1] = W / img_height
    Ks[..., 0, 2] = center_x - W / 2.0
    Ks[..., 1, 2] = center_y - W / 2.0
    Ks[..., 2, 2] = 1
    return Ks


def get_default_hmr_intrinsic(num_frame=1,
                              focal_length=1000,
                              det_width=224,
                              det_height=224) -> np.ndarray:
    """Get default hmr intrinsic, defined by how you trained.

    Args:
        num_frame (int, optional): num of frames. Defaults to 1.
        focal_length (int, optional): defined same as your training.
            Defaults to 1000.
        det_width (int, optional): the size you used to detect.
            Defaults to 224.
        det_height (int, optional): the size you used to detect.
            Defaults to 224.

    Returns:
        np.ndarray: shape of (N, 3, 3)
    """
    K = np.zeros((num_frame, 3, 3))
    K[:, 0, 0] = focal_length
    K[:, 1, 1] = focal_length
    K[:, 0, 2] = det_width / 2
    K[:, 1, 2] = det_height / 2
    K[:, 2, 2] = 1
    return K


def convert_kp2d_to_bbox(
        kp2d: np.ndarray,
        bbox_format: Literal['xyxy', 'xywh'] = 'xyxy') -> np.ndarray:
    """Convert kp2d to bbox.

    Args:
        kp2d (np.ndarray):  shape should be (num_frame, num_points, 2/3)
            or (num_frame, num_person, num_points, 2/3).
        bbox_format (Literal['xyxy', 'xywh'], optional): Defaults to 'xyxy'.

    Returns:
        np.ndarray: shape will be (num_frame, num_person, 4)
    """
    assert bbox_format in ['xyxy', 'xywh']
    if kp2d.ndim == 2:
        kp2d = kp2d[None, None]
    elif kp2d.ndim == 3:
        kp2d = kp2d[:, None]
    num_frame, num_person, _, _ = kp2d.shape
    x1 = np.max(kp2d[..., 0], axis=-2)
    y1 = np.max(kp2d[..., 1], axis=-2)
    x2 = np.max(kp2d[..., 2], axis=-2)
    y2 = np.max(kp2d[..., 3], axis=-2)
    bbox = np.concatenate([x1, y1, x2, y2], axis=-1)
    assert bbox.shape == (num_frame, num_person, 4)
    if bbox_format == 'xywh':
        bbox = xyxy2xywh(bbox)
    return bbox


def convert_verts_to_cam_coord(verts,
                               pred_cams,
                               bboxes_xy,
                               focal_length=5000.,
                               bbox_scale_factor=1.25,
                               bbox_format='xyxy'):
    """Convert vertices from the world coordinate to camera coordinate.

    Args:
        verts ([np.ndarray]): The vertices in the world coordinate.
            The shape is (frame,num_person,6890,3), (frame,6890,3),
            or (6890,3).
        pred_cams ([np.ndarray]): Camera parameters estimated by HMR or SPIN.
            The shape is (frame,num_person,3), (frame,3), or (3,).
        bboxes_xy ([np.ndarray]): (frame, num_person, 4|5), (frame, 4|5),
            or (4|5,)
        focal_length ([float],optional): Defined same as your training.
        bbox_scale_factor (float): scale factor for expanding the bbox.
        bbox_format (Literal['xyxy', 'xywh'] ): 'xyxy' means the left-up point
            and right-bottomn point of the bbox.
            'xywh' means the left-up point and the width and height of the
            bbox.
    Returns:
        np.ndarray: The vertices in the camera coordinate.
            The shape is (frame,num_person,6890,3) or (frame,6890,3).
        np.ndarray: The intrinsic parameters of the pred_cam.
            The shape is (num_frame, 3, 3).
    """
    K0 = get_default_hmr_intrinsic(
        focal_length=focal_length, det_height=224, det_width=224)
    K1 = convert_bbox_to_intrinsic(
        bboxes_xy,
        bbox_scale_factor=bbox_scale_factor,
        bbox_format=bbox_format)
    # K1K0(RX+T)-> K0(K0_inv K1K0)
    Ks = np.linalg.inv(K0) @ K1 @ K0
    # convert vertices from world to camera
    cam_trans = np.concatenate([
        pred_cams[..., [1]], pred_cams[..., [2]], 2 * focal_length /
        (224 * pred_cams[..., [0]] + 1e-9)
    ], -1)
    verts = verts + cam_trans[..., None, :]
    if verts.ndim == 4:
        verts = np.einsum('fnij,fnkj->fnki', Ks, verts)
    elif verts.ndim == 3:
        verts = np.einsum('fij,fkj->fki', Ks, verts)
    elif verts.ndim == 2:
        verts = np.einsum('fij,fkj->fki', Ks, verts[None])
    return verts, K0


def smooth_process(x,
                   smooth_type='savgol',
                   cfg_base_dir='configs/_base_/post_processing/'):
    """Smooth the array with the specified smoothing type.

    Args:
        x (np.ndarray): Shape should be (frame,num_person,K,C)
            or (frame,K,C).
        smooth_type (str, optional): Smooth type.
            choose in ['oneeuro', 'gaus1d', 'savgol','smoothnet',
                'smoothnet_windowsize8','smoothnet_windowsize16',
                'smoothnet_windowsize32','smoothnet_windowsize64'].
            Defaults to 'savgol'. 'smoothnet' is default with windowsize=8.
        cfg_base_dir (str, optional): Config base dir,
                            default configs/_base_/post_processing/
    Raises:
        ValueError: check the input smoothing type.

    Returns:
        np.ndarray: Smoothed data. The shape should be
            (frame,num_person,K,C) or (frame,K,C).
    """
    if smooth_type == 'smoothnet':
        smooth_type = 'smoothnet_windowsize8'

    assert smooth_type in [
        'oneeuro', 'guas1d', 'savgol', 'smoothnet_windowsize8',
        'smoothnet_windowsize16', 'smoothnet_windowsize32',
        'smoothnet_windowsize64'
    ]

    cfg = os.path.join(cfg_base_dir, smooth_type + '.py')
    if isinstance(cfg, str):
        cfg = mmcv.Config.fromfile(cfg)
    elif not isinstance(cfg, mmcv.Config):
        raise TypeError('config must be a filename or Config object, '
                        f'but got {type(cfg)}')

    x = x.copy()

    assert x.ndim == 3 or x.ndim == 4

    smooth_func = build_post_processing(dict(cfg['smooth_cfg']))

    if x.ndim == 4:
        for i in range(x.shape[1]):
            x[:, i] = smooth_func(x[:, i])
    elif x.ndim == 3:
        x = smooth_func(x)

    return x


def speed_up_process(x,
                     speed_up_type='deciwatch',
                     cfg_base_dir='configs/_base_/post_processing/'):
    """Speed up the process with the specified speed up type.

    Args:
        x (np.ndarray): Shape should be (frame,num_person,K,C)
            or (frame,K,C).
        speed_up_type (str, optional): Speed up type.
            choose in ['deciwatch',
                        'deciwatch_interval5_q1',
                        'deciwatch_interval5_q2',
                        'deciwatch_interval5_q3',
                        'deciwatch_interval5_q4',
                        'deciwatch_interval5_q5',
                        'deciwatch_interval10_q1',
                        'deciwatch_interval10_q2',
                        'deciwatch_interval10_q3',
                        'deciwatch_interval10_q4',
                        'deciwatch_interval10_q5',]. Defaults to 'deciwatch'.
        cfg_base_dir (str, optional): Config base dir.
                                Defaults to 'configs/_base_/post_processing/'

    Raises:
        ValueError: check the input speed up type.

    Returns:
        np.ndarray: Completed data. The shape should be
            (frame,num_person,K,C) or (frame,K,C).
    """

    if speed_up_type == 'deciwatch':
        speed_up_type = 'deciwatch_interval5_q3'
    assert speed_up_type in [
        'deciwatch_interval5_q1',
        'deciwatch_interval5_q2',
        'deciwatch_interval5_q3',
        'deciwatch_interval5_q4',
        'deciwatch_interval5_q5',
        'deciwatch_interval10_q1',
        'deciwatch_interval10_q2',
        'deciwatch_interval10_q3',
        'deciwatch_interval10_q4',
        'deciwatch_interval10_q5',
    ]

    cfg = os.path.join(cfg_base_dir, speed_up_type + '.py')
    if isinstance(cfg, str):
        cfg = mmcv.Config.fromfile(cfg)
    elif not isinstance(cfg, mmcv.Config):
        raise TypeError('config must be a filename or Config object, '
                        f'but got {type(cfg)}')
    x = x.clone()

    assert x.ndim == 4 or x.ndim == 5

    cfg_dict = cfg['speed_up_cfg']
    cfg_dict['device'] = x.device

    speed_up_func = build_post_processing(cfg_dict)

    if x.ndim == 5:
        for i in range(x.shape[1]):
            x[:, i] = speed_up_func(x[:, i])
    elif x.ndim == 4:
        x = speed_up_func(x)

    return np.array(x.cpu())


def get_speed_up_interval(speed_up_type,
                          cfg_base_dir='configs/_base_/post_processing/'):
    """Get the interval of specific speed up type.

    Args:
        speed_up_type (str, optional): Speed up type.
            choose in ['deciwatch',
                        'deciwatch_interval5_q1',
                        'deciwatch_interval5_q2',
                        'deciwatch_interval5_q3',
                        'deciwatch_interval5_q4',
                        'deciwatch_interval5_q5',
                        'deciwatch_interval10_q1',
                        'deciwatch_interval10_q2',
                        'deciwatch_interval10_q3',
                        'deciwatch_interval10_q4',
                        'deciwatch_interval10_q5',]. Defaults to 'deciwatch'.
        cfg_base_dir (str, optional): Config base dir,
                            default configs/_base_/post_processing/

    Raises:
        ValueError: check the input speed up type.

    Returns:
        int: speed up interval
    """

    if speed_up_type == 'deciwatch':
        speed_up_type = 'deciwatch_interval5_q3'
    assert speed_up_type in [
        'deciwatch_interval5_q1',
        'deciwatch_interval5_q2',
        'deciwatch_interval5_q3',
        'deciwatch_interval5_q4',
        'deciwatch_interval5_q5',
        'deciwatch_interval10_q1',
        'deciwatch_interval10_q2',
        'deciwatch_interval10_q3',
        'deciwatch_interval10_q4',
        'deciwatch_interval10_q5',
    ]
    cfg = os.path.join(cfg_base_dir, speed_up_type + '.py')
    if isinstance(cfg, str):
        cfg = mmcv.Config.fromfile(cfg)
    elif not isinstance(cfg, mmcv.Config):
        raise TypeError('config must be a filename or Config object, '
                        f'but got {type(cfg)}')

    return cfg['speed_up_cfg']['interval']


def speed_up_interpolate(selected_frames, speed_up_frames, smpl_poses,
                         smpl_betas, pred_cams, bboxes_xyxy):
    """Interpolate smpl_betas, pred_cams, and bboxes_xyxyx for speed up.

    Args:
        selected_frames (np.ndarray): Shape should be (selected frame number).
        speed_up_frames (int): Total speed up frame number
        smpl_poses (np.ndarray): selected frame smpl poses parameter
        smpl_betas (np.ndarray): selected frame smpl shape paeameter
        pred_cams (np.ndarray): selected frame camera parameter
        bboxes_xyxy (np.ndarray): selected frame bbox

    Returns:
        smpl_poses (np.ndarray): interpolated frame smpl poses parameter
        smpl_betas (np.ndarray): interpolated frame smpl shape paeameter
        pred_cams (np.ndarray): interpolated frame camera parameter
        bboxes_xyxy (np.ndarray): interpolated frame bbox
    """
    selected_frames = selected_frames[selected_frames <= speed_up_frames]
    pred_cams[:speed_up_frames, :] = interpolate.interp1d(
        selected_frames, pred_cams[selected_frames, :], kind='linear', axis=0)(
            np.arange(0, max(selected_frames)))
    bboxes_xyxy[:speed_up_frames, :] = interpolate.interp1d(
        selected_frames,
        bboxes_xyxy[selected_frames, :],
        kind='linear',
        axis=0)(
            np.arange(0, max(selected_frames)))
    smpl_betas[:speed_up_frames, :] = interpolate.interp1d(
        selected_frames, smpl_betas[selected_frames, :], kind='linear',
        axis=0)(
            np.arange(0, max(selected_frames)))

    return smpl_poses, smpl_betas, pred_cams, bboxes_xyxy


def process_mmtracking_results(mmtracking_results,
                               max_track_id,
                               bbox_thr=None):
    """Process mmtracking results.

    Args:
        mmtracking_results ([list]): mmtracking_results.
        bbox_thr (float): threshold for bounding boxes.
        max_track_id (int): the maximum track id.
    Returns:
        person_results ([list]): a list of tracked bounding boxes
        max_track_id (int): the maximum track id.
        instance_num (int): the number of instance.
    """
    person_results = []
    # 'track_results' is changed to 'track_bboxes'
    # in https://github.com/open-mmlab/mmtracking/pull/300
    if 'track_bboxes' in mmtracking_results:
        tracking_results = mmtracking_results['track_bboxes'][0]
    elif 'track_results' in mmtracking_results:
        tracking_results = mmtracking_results['track_results'][0]

    tracking_results = np.array(tracking_results)

    if bbox_thr is not None:
        assert tracking_results.shape[-1] == 6
        valid_idx = np.where(tracking_results[:, 5] > bbox_thr)[0]
        tracking_results = tracking_results[valid_idx]

    for track in tracking_results:
        person = {}
        person['track_id'] = int(track[0])
        if max_track_id < int(track[0]):
            max_track_id = int(track[0])
        person['bbox'] = track[1:]
        person_results.append(person)
    person_results = sorted(person_results, key=lambda x: x.get('track_id', 0))
    instance_num = len(person_results)
    return person_results, max_track_id, instance_num


def process_mmdet_results(mmdet_results, cat_id=1, bbox_thr=None):
    """Process mmdet results, and return a list of bboxes.

    Args:
        mmdet_results (list|tuple): mmdet results.
        bbox_thr (float): threshold for bounding boxes.
        cat_id (int): category id (default: 1 for human)

    Returns:
        person_results (list): a list of detected bounding boxes
    """
    if isinstance(mmdet_results, tuple):
        det_results = mmdet_results[0]
    else:
        det_results = mmdet_results

    bboxes = det_results[cat_id - 1]

    person_results = []
    bboxes = np.array(bboxes)

    if bbox_thr is not None:
        assert bboxes.shape[-1] == 5
        valid_idx = np.where(bboxes[:, 4] > bbox_thr)[0]
        bboxes = bboxes[valid_idx]

    for bbox in bboxes:
        person = {}
        person['bbox'] = bbox
        person_results.append(person)

    return person_results


def prepare_frames(input_path=None):
    """Prepare frames from input_path.

    Args:
        input_path (str, optional): Defaults to None.

    Raises:
        ValueError: check the input path.

    Returns:
        List[np.ndarray]: prepared frames
    """
    if Path(input_path).is_file():
        img_list = [mmcv.imread(input_path)]
        if img_list[0] is None:
            video = mmcv.VideoReader(input_path)
            assert video.opened, f'Failed to load file {input_path}'
            img_list = list(video)
    elif Path(input_path).is_dir():
        # input_type = 'folder'
        file_list = [
            os.path.join(input_path, fn) for fn in os.listdir(input_path)
            if fn.lower().endswith(('.png', '.jpg'))
        ]
        file_list.sort()
        img_list = [mmcv.imread(img_path) for img_path in file_list]
        assert len(img_list), f'Failed to load image from {input_path}'
    else:
        raise ValueError('Input path should be an file or folder.'
                         f' Got invalid input path: {input_path}')
    return img_list


def extract_feature_sequence(extracted_results,
                             frame_idx,
                             causal,
                             seq_len,
                             step=1):
    """Extract the target frame from person results, and pad the sequence to a
    fixed length.

    Args:
        extracted_results (List[List[Dict]]): Multi-frame feature extraction
            results stored in a nested list. Each element of the outer list
            is the feature extraction results of a single frame, and each
            element of the inner list is the feature information of one person,
            which contains:
                features (ndarray): extracted features
                track_id (int): unique id of each person, required when
                    ``with_track_id==True```
                bbox ((4, ) or (5, )): left, right, top, bottom, [score]
        frame_idx (int): The index of the frame in the original video.
        causal (bool): If True, the target frame is the first frame in
            a sequence. Otherwise, the target frame is in the middle of a
            sequence.
        seq_len (int): The number of frames in the input sequence.
        step (int): Step size to extract frames from the video.

    Returns:
        List[List[Dict]]: Multi-frame feature extraction results stored in a
            nested list with a length of seq_len.
        int: The target frame index in the padded sequence.
    """

    if causal:
        frames_left = 0
        frames_right = seq_len - 1
    else:
        frames_left = (seq_len - 1) // 2
        frames_right = frames_left
    num_frames = len(extracted_results)

    # get the padded sequence
    pad_left = max(0, frames_left - frame_idx // step)
    pad_right = max(0, frames_right - (num_frames - 1 - frame_idx) // step)
    start = max(frame_idx % step, frame_idx - frames_left * step)
    end = min(num_frames - (num_frames - 1 - frame_idx) % step,
              frame_idx + frames_right * step + 1)
    extracted_results_seq = [extracted_results[0]] * pad_left + \
        extracted_results[start:end:step] + [extracted_results[-1]] * pad_right
    return extracted_results_seq


def get_different_colors(number_of_colors,
                         flag=0,
                         alpha: float = 1.0,
                         mode: str = 'bgr',
                         int_dtype: bool = True):
    """Get a numpy of colors of shape (N, 3)."""
    mode = mode.lower()
    assert set(mode).issubset({'r', 'g', 'b', 'a'})
    nst0 = np.random.get_state()
    np.random.seed(flag)
    colors = []
    for i in np.arange(0., 360., 360. / number_of_colors):
        hue = i / 360.
        lightness = (50 + np.random.rand() * 10) / 100.
        saturation = (90 + np.random.rand() * 10) / 100.
        colors.append(colorsys.hls_to_rgb(hue, lightness, saturation))
    colors_np = np.asarray(colors)
    if int_dtype:
        colors_bgr = (255 * colors_np).astype(np.uint8)
    else:
        colors_bgr = colors_np.astype(np.float32)
    # recover the random state
    np.random.set_state(nst0)
    color_dict = {}
    if 'a' in mode:
        color_dict['a'] = np.ones((colors_bgr.shape[0], 3)) * alpha
    color_dict['b'] = colors_bgr[:, 0:1]
    color_dict['g'] = colors_bgr[:, 1:2]
    color_dict['r'] = colors_bgr[:, 2:3]
    colors_final = []
    for channel in mode:
        colors_final.append(color_dict[channel])
    colors_final = np.concatenate(colors_final, -1)
    return colors_final


class RunningAverage():
    r"""A helper class to calculate running average in a sliding window.

    Args:
        window (int): The size of the sliding window.
    """

    def __init__(self, window: int = 1):
        self.window = window
        self._data = []

    def update(self, value):
        """Update a new data sample."""
        self._data.append(value)
        self._data = self._data[-self.window:]

    def average(self):
        """Get the average value of current window."""
        return np.mean(self._data)


class StopWatch:
    r"""A helper class to measure FPS and detailed time consuming of each phase
    in a video processing loop or similar scenarios.

    Args:
        window (int): The sliding window size to calculate the running average
            of the time consuming.

    Example:
        >>> from mmpose.utils import StopWatch
        >>> import time
        >>> stop_watch = StopWatch(window=10)
        >>> with stop_watch.timeit('total'):
        >>>     time.sleep(0.1)
        >>>     # 'timeit' support nested use
        >>>     with stop_watch.timeit('phase1'):
        >>>         time.sleep(0.1)
        >>>     with stop_watch.timeit('phase2'):
        >>>         time.sleep(0.2)
        >>>     time.sleep(0.2)
        >>> report = stop_watch.report()
    """

    def __init__(self, window=1):
        self.window = window
        self._record = defaultdict(partial(RunningAverage, window=self.window))
        self._timer_stack = []

    @contextmanager
    def timeit(self, timer_name='_FPS_'):
        """Timing a code snippet with an assigned name.

        Args:
            timer_name (str): The unique name of the interested code snippet to
                handle multiple timers and generate reports. Note that '_FPS_'
                is a special key that the measurement will be in `fps` instead
                of `millisecond`. Also see `report` and `report_strings`.
                Default: '_FPS_'.
        Note:
            This function should always be used in a `with` statement, as shown
            in the example.
        """
        self._timer_stack.append((timer_name, Timer()))
        try:
            yield
        finally:
            timer_name, timer = self._timer_stack.pop()
            self._record[timer_name].update(timer.since_start())

    def report(self, key=None):
        """Report timing information.

        Returns:
            dict: The key is the timer name and the value is the \
                corresponding average time consuming.
        """
        result = {
            name: r.average() * 1000.
            for name, r in self._record.items()
        }

        if '_FPS_' in result:
            result['_FPS_'] = 1000. / result.pop('_FPS_')

        if key is None:
            return result
        return result[key]

    def report_strings(self):
        """Report timing information in texture strings.

        Returns:
            list(str): Each element is the information string of a timed \
                event, in format of '{timer_name}: {time_in_ms}'. \
                Specially, if timer_name is '_FPS_', the result will \
                be converted to fps.
        """
        result = self.report()
        strings = []
        if '_FPS_' in result:
            strings.append(f'FPS: {result["_FPS_"]:>5.1f}')
        strings += [f'{name}: {val:>3.0f}' for name, val in result.items()]
        return strings

    def reset(self):
        self._record = defaultdict(list)
        self._active_timer_stack = []
