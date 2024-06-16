import bpy
from bpy.props import (PointerProperty)
from .four_d_humans_blender import *
from . panel import *
import os

bl_info = {
    "name" : "CEB 4D Humans",
    "author" : "Shubham Goel, Georgios Pavlakos, Jathushan Rajasegaran, Angjoo Kanazawa, Jitendra Malik, Shin, Soyong and Kim, Juyong and Halilaj, Eni and Black, Michael J., Carlos Barreto",
    "description" : "",
    "blender" : (3, 5, 0),
    "version" : (1, 0,12),
    "location" : "UI > SidePanel",
    "warning" : "",
    "category" : "General"
}

# 1.12 Beta: fixes for installation of 4d humans, added option to import smpl pkl model
# 1.11 Beta: Fix to make IK Control to work with WHAM, enable IK control in all 3 animation types (4d humans, wham and slahmr), added the source selector to choose which character to transform to IK Control, added the load video on screen option to 4D Humans and WHAM, adding quick save and quick load for markers, better error handling on 4d humans, update to work with blender 4.1
# 1.10 Beta: Enabled to retarget the result after using the IK Control tools. Fixed the import PKL in 4d Humans
# 1.09 Beta - IK - FK control, Better Foor Lock and floor detection
# 1.08 Beta - Offline install of WHAM checkpoints using file "wham_offline_checkpoints.zip", actorcore rig preset
# 1.07 Beta - Fixing instalation problems, fixed the load video, in case the image plane addon was not loaded
# 1.06 Beta - WHAM Update 2024-02-19, packing with the SMPL fbx
# 1.05 Beta - Finish adding SLAHMR
# 1.04 Beta - Adding SLAHMR (incomplete) to the addon,fix 4d humans creation and import
# 1.03 Beta - Fixing the bugs introduced on 1.02 Beta
# 1.02 Beta - Option to load pose/pose_world and trans/trans_world. Export and import of pkl files
# 1.01Beta - Added possibility of multiple characters, and the correction to get all the animation if there is a glitch on the detection, it will come as another chracter.
# 1.00Beta - Wham project was added, enabling you to process and load the character
# 0.57  - Preset for DAZ Genesis2
# 0.56  - Preset for DAZ Genesis9, fiz retarget for character with more modifiers other than Armature one.
# 0.55  - Presets for UE4,UE5 and Metahuman
# 0.54  - mudando posicao do target armature caso ele nao esteja em T pose (apply armature modifier - apply pose as rest pose - add armature again)
#       - preset para character creator +
#       - correcao para ler o tamanho do video e colocar esse tamanho como o limite (o padrao era 1300)
# 0.53  - inclindo o codigo do "unbind" depois que terminar o retarget, do contrario teria bones sobrando no souce armature
#       - opcao para poder limpar frames, marcando com marker e elimiando os outros que estao fora do marker
# 0.52 - colocar custom end frame for video, or automatic
# tentando para 0.6 - colocar edit do armature mais facil, usando ik, por exemplo (so que vou ter que criar o ik em tempo real e depois bake)

# Adicionando path para usar GIT e ffmpeg
path_addon = os.path.dirname(os.path.abspath(__file__))
print('Path addon',path_addon)

path_git = os.path.join(path_addon,'3rdparty','PortableGit','bin')
print('Path git',path_git)

path_ffmpeg = os.path.join(path_addon,'3rdparty','ffmpeg_essentials','bin')
print('Path ffmpeg',path_ffmpeg)

os.environ['PATH'] += ';'+path_git+';'+path_ffmpeg
print('paths added')


classes = (PIXELMySettings,FOURDHUMANS_PT_Panel
    ,CreateVirtualEnviroment,InstallPYTORCHOnVenv,InstallPREDETECTRONOnVenv,InstallDETECTRONOnVenv,VenvPathSelect,InstallREQPIXELOnVenv
    ,ImportVideo,Execute
    ,OpenOutputFolder
    ,ImportCharacter,ImportFBX
    ,Smooth,ExportRAWAnimation
    ,ReadPKLData,ImportPKLAnimation,SetIniFPS
    ,Smooth2
    ,FootLockMarker,FootLock,ZeroFrameTPose,RemoveLocationAnimation
    ,ImportOfflineFiles
    ,CreateNLAStrip,CopyNameToNLA
    ,ACTION_UL_list,ACTION_STRIP_UL_list,RemoveNLAStrip,LoadActionToCharFromNLA,SetNoAction
    ,AddTrack,AddActionToTrack,AddActionToTrackWTransition,RemoveActionFromtrack
    ,Open_NLA_VIEW,SelectActionOnStrip,OrganizeStrip
    ,MatchToPrevAction,CreateReferenceAction,Retarget,ExtractMarkedFrames,ClearMarkers,ExtractMarkedFramesForSelectedBones,OptimizeMarkerView,QuickSaveMarkers,QuickLoadMarkers,QuickSaveMarkersClear
    ,ChangeTargetRestPose,ClearTgtMeshShapekeys,StartChangeRestTgtPose,EndChangeRestTgtPose
    ,StartChangeRestSourcePose,EndChangeRestSourcePose
    ,Stg2Append,MR_switch_snap_anim,Stg2retarget,Stg2Full,SwitchFKIKPart
    ,Setupfloor,SetupFootLock,StartEndFootLock,ClearFootLock,FixFootFCurve
    ,CreateVirtualEnviromentWHAM,InstallPYTORCHOnVenvWHAM,InstallWHAMOnVenv,DownloadWHAMCheckpoints,DownloadWHAMBodymodels
    ,ImportSMPLPKL,ImportVideoWHAM,ExecuteWHAM
    ,InstallSLAHMROnVenv,CreateVirtualEnviromentSLAHMR,InstallPYTORCHOnVenvSLAHMR,InstallDETECTRONOnVenvSLAHMR,InstallSLAHMRandRESTOnVenv
    ,ExecuteSLAHMR,ImportVideoSLAHMR,Update_SLAHMR_Setting,LoadVideo3dview,ExportSLAHMRRAWAnimation,ImportZIPAnimation,ImportZIPSLAHMRDependencies
    ,ImportOfflineCheckpointWham
    )




def register():

    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
    bpy.types.Scene.fourd_prop = PointerProperty(type=PIXELMySettings)
    # bpy.types.Scene.ceb_bark_img_path = bpy.props.BoolProperty(default=False)
    bpy.types.Scene.fourd_venv = bpy.props.BoolProperty(default=False)
    bpy.types.Scene.fourd_venv_wham = bpy.props.BoolProperty(default=False)
    bpy.types.Scene.fourd_venv_slahmr = bpy.props.BoolProperty(default=False)
    bpy.types.Scene.ik_advanced = bpy.props.BoolProperty(default=False)
    # bpy.types.Object.progress_bar = bpy.props.FloatProperty( name="Progress", subtype="PERCENTAGE",soft_min=0, soft_max=100, precision=0,)
    # bpy.types.Scene.progress_bar = bpy.props.FloatProperty( name="Progress", subtype="PERCENTAGE",soft_min=0, soft_max=100, precision=0,)
    bpy.types.Scene.active_action_index = bpy.props.IntProperty()
    bpy.types.Scene.active_track_index = bpy.props.IntProperty(update=select_action_strip)

    #seleciona source e target
    bpy.types.Scene.source = PointerProperty(type=bpy.types.Object)
    bpy.types.Scene.target = PointerProperty(type=bpy.types.Object)
    bpy.types.Scene.target_mesh = PointerProperty(type=bpy.types.Object)
    bpy.types.Scene.target_stg2 = PointerProperty(type=bpy.types.Object)
    bpy.types.Scene.floor = PointerProperty(type=bpy.types.Object)
    
    bpy.types.Scene.foot_lock_right = PointerProperty(type=bpy.types.Object)
    bpy.types.Scene.foot_lock_left = PointerProperty(type=bpy.types.Object)


    

def unregister():
    from bpy.utils import unregister_class


    for cls in reversed(classes):
        unregister_class(cls) 
    del bpy.types.Scene.fourd_prop
    # del bpy.types.Scene.ceb_bark_img_path
    del bpy.types.Scene.fourd_venv
    del bpy.types.Scene.source
    del bpy.types.Scene.target
    del bpy.types.Scene.target_stg2

    # del bpy.types.Scene.render_scene_list
    # del bpy.types.Scene.render_scene_list_index


if __name__ == "__main__":
    register()
    