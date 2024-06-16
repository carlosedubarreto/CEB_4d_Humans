
# from scipy.signal import savgol_filter
import pickle
import numpy as np
import os
from scipy.spatial.transform import Rotation as R
import argparse
import copy
import numpy as np
from mmhuman3d.utils.demo_utils import smooth_process

# Create the parser
parser = argparse.ArgumentParser()
# Add an argument
parser.add_argument('--tot_characters', type=int, required=True)
parser.add_argument('--pkl_file_input', type=str, required=True) # normalmente vai ser 'demo_video_converted.pkl' ou 'demo_video_converted_smooth.pkl'
parser.add_argument('--smooth_what', type=str, required=True) # trans,pose,both
# Parse the argument
args = parser.parse_args()



path_addon = os.path.dirname(os.path.abspath(__file__))
pkl_folder = os.path.join(path_addon,'4D-Humans-main','outputs','results')


# file = r"D:\0_Programs\CEB_4D_Human_prj\CEB_4d_Human\4D-Humans-main\outputs\results\demo_video_converted.pkl"
# file_smooth = r"D:\0_Programs\CEB_4D_Human_prj\CEB_4d_Human\4D-Humans-main\outputs\results\demo_video_converted_smooth.pkl"
# file_smooth2 = r"D:\0_Programs\CEB_4D_Human_prj\CEB_4d_Human\4D-Humans-main\outputs\results\demo_video_converted_smooth.pkl"

# file = os.path.join(pkl_folder,'demo_video_converted.pkl')
file = os.path.join(pkl_folder,args.pkl_file_input)

file_smooth = os.path.join(pkl_folder,'demo_video_converted_smooth.pkl')

with open(file, 'rb') as handle:
    b = pickle.load(handle)

print('tot characters: '+str(args.tot_characters))
characters = args.tot_characters

for num_character in range(0,characters):
    trans = None
    trans_temp = None
    smpl_trans = None
    global_orient = None
    body_pose = None
    final_body_pose = None
    body_pose_vec = None
    smpl_pose = None
    print('charcter: '+str(num_character))
    first_exec = 1
    fframe_real=0
    frame_ref = []
    for fframe, data in enumerate(b.items()):

        if num_character <= len(data[1]['smpl'])-1:
            if args.smooth_what == 'trans' or  args.smooth_what == 'both':
                trans = data[1]['camera'][num_character]
                trans_temp = [trans[0],trans[1],0]
                # if fframe==0:
                # if smpl_trans==None:
                if first_exec==1:
                    smpl_trans =trans_temp
                else:
                    smpl_trans = np.vstack([smpl_trans,trans_temp])
                
            #shape = data[1]['smpl'][character]['betas']
            if args.smooth_what == 'pose' or  args.smooth_what == 'both':
                global_orient = data[1]['smpl'][num_character]['global_orient']
                body_pose = data[1]['smpl'][num_character]['body_pose']
                final_body_pose = np.vstack([global_orient, body_pose])
                r = R.from_matrix(final_body_pose)
                body_pose_vec = r.as_rotvec() 
                # if fframe==0:
                # if smpl_pose==None:
                if first_exec==1:
                    smpl_pose = body_pose_vec.reshape(1,72)
                else:
                    smpl_pose = np.vstack([smpl_pose,body_pose_vec.reshape(1,72)])
            first_exec = 0 #desabilita primeira execucao
            frame_ref.append([fframe,fframe_real])
            fframe_real = fframe_real+1
        else:
            print('skipping to the next')
            # first_exec = 1
            frame_ref.append([fframe,None])

        


    # print('trans: ',smpl_trans.shape)
    # print('shape: ',smpl_pose.shape)

    smooth_type_s = 'smoothnet_windowsize8'
    # smooth_type_s = 'smoothnet_windowsize16'
    # smooth_type_s = 'savgol'
    # smooth_type_s = 'oneeuro'
    # smooth_type_s = 'guas1d'
    # smooth_type_s = 'smoothnet_windowsize32'
    # smooth_type_s = 'smoothnet_windowsize64'

    if args.smooth_what == 'trans' or  args.smooth_what == 'both':
        trans = smpl_trans # (N,3), "global_t" in npz file
        t0 = trans[::2]
        frame_num = t0.shape[0]
        new_trans_0 = smooth_process(t0[:, np.newaxis], 
                                        # smooth_type='smoothnet_windowsize8',
                                        smooth_type=smooth_type_s,
                                        cfg_base_dir='configs_cliff/_base_/post_processing/').reshape(frame_num,3)

    if args.smooth_what == 'pose' or  args.smooth_what == 'both':
        pose = smpl_pose # (N,72), "pose" in npz file
        p0 = pose[::2]
        frame_num = p0.shape[0]
        new_pose_0 = smooth_process(p0.reshape(frame_num,24,3), 
                                    # smooth_type='smoothnet_windowsize8',
                                    smooth_type=smooth_type_s,
                                    cfg_base_dir='configs_cliff/_base_/post_processing/').reshape(frame_num,72)

    # start from 1, the interval is 2
    if args.smooth_what == 'trans' or  args.smooth_what == 'both':
        t1 = trans[1::2]
        frame_num = t1.shape[0]
        new_trans_1 = smooth_process(t1[:, np.newaxis], 
                                        # smooth_type='smoothnet_windowsize8',
                                        smooth_type=smooth_type_s,
                                        cfg_base_dir='configs_cliff/_base_/post_processing/').reshape(frame_num,3)

    if args.smooth_what == 'pose' or  args.smooth_what == 'both':
        p1 = pose[1::2]
        frame_num = p1.shape[0]
        new_pose_1 = smooth_process(p1.reshape(frame_num,24,3), 
                                    # smooth_type='smoothnet_windowsize8',
                                    smooth_type=smooth_type_s,
                                    cfg_base_dir='configs_cliff/_base_/post_processing/').reshape(frame_num,72)

    if args.smooth_what == 'pose' or  args.smooth_what == 'both':
        new_pose = copy.copy(pose)
        new_pose[::2] = new_pose_0
        new_pose[1::2] = new_pose_1

    if args.smooth_what == 'trans' or  args.smooth_what == 'both':
        new_trans = copy.copy(trans)
        new_trans[::2] = new_trans_0
        new_trans[1::2] = new_trans_1

    # realimentando pparar criar o pickle
    for ffnew, data_new in enumerate(b.items()):
        if num_character <= len(data_new[1]['smpl'])-1:
            if args.smooth_what == 'trans' or  args.smooth_what == 'both':
                # b[data_new[0]]['camera'][num_character] = new_trans[ffnew]
                b[data_new[0]]['camera'][num_character] = new_trans[frame_ref[ffnew][1]]
            
            if args.smooth_what == 'pose' or  args.smooth_what == 'both':
                ## De volta de rot vec para rot matrix
                # r_new = R.from_rotvec(new_pose[ffnew].reshape(24,3))
                r_new = R.from_rotvec(new_pose[frame_ref[ffnew][1]].reshape(24,3))
                body_pose_matrix = r_new.as_matrix() 

                global_orient_new = body_pose_matrix[0].reshape(1,3,3)
                body_pose_new = body_pose_matrix[1:]
                b[data_new[0]]['smpl'][num_character]['global_orient'] = global_orient_new
                b[data_new[0]]['smpl'][num_character]['body_pose'] = body_pose_new
        else:
            print('skipping to the next')


with open(file_smooth, 'wb') as handle:
    pickle.dump(b, handle, protocol=pickle.HIGHEST_PROTOCOL)
