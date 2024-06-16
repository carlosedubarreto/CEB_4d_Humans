from scipy.spatial.transform import Rotation as R
import numpy as np
import joblib

file = r"D:\0_usuarios\Vinay_Yadav\demo_youtube.pkl"
#file = r'D:\AI\0_mocap\4d-humans\4D-Humans-main\outputs\demo_gymnasts.pkl'
results = joblib.load(file)

quaternion= []

for f,value in enumerate(results.items()):
    video_name = value[0]
    frame4dhuman= value[1]['3d_joints'][0]
    frame4dhumanRotMat= value[1]['smpl'][0]['global_orient'][0]
    r = R.from_matrix(frame4dhumanRotMat)
    quaternion.append(r.as_quat())


joblib.dump(quaternion, 'quaternion.pkl', compress=3)

# print(frame4dhumanRotMat)

# r = R.from_matrix(frame4dhumanRotMat)
# quat = r.as_quat()
# print('quat: ',quat)


## coloquei no blender para importar no pelvis
import bpy
import joblib
#D:\AI\0_mocap\4d-humans\4D-Humans-main\quaternion.pkl


file = r"D:\AI\0_mocap\4d-humans\4D-Humans-main\quaternion.pkl"
#file = r'D:\AI\0_mocap\4d-humans\4D-Humans-main\outputs\demo_gymnasts.pkl'
results = joblib.load(file)


armature = bpy.context.scene.objects['Armature']
bone = armature.pose.bones[0]

for f,rq in enumerate(results):
    bone.rotation_quaternion = rq
    bone.keyframe_insert(data_path='rotation_quaternion',frame=f)
