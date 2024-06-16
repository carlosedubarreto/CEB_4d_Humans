# from typing import Pattern
import bpy
from bpy.types import Operator
# from . helper import Helper
from bpy_extras.io_utils import ImportHelper,ExportHelper
from bpy.props import CollectionProperty
# from bpy.props import StringProperty
import json
import os,sys,glob
# from shutil import copyfile,rmtree,move
from os.path import join
from .panel import *
import shutil
import subprocess
import glob
import pickle
import mathutils
from mathutils import *




def read_pkl_data(context,character=0): #0=4d humans, 1=wham
    path_addon = os.path.dirname(os.path.abspath(__file__))
    fourd_prop = context.scene.fourd_prop
    #pegando a quantidade de characters
    # import pickle
    if character==0:
        base_file = os.path.join(path_addon,'4D-Humans-main','outputs','results')
        file_converted = os.path.join(base_file,'demo_video_converted.pkl')
        file = file_converted
        with open(file, 'rb') as handle:
            b = pickle.load(handle)
            
        num_character = 0
        for fframe, data in enumerate(b.items()):
            len_char = len(data[1]['smpl'])
            print('len_char: ',len_char)
            if num_character < len_char:
                num_character = len_char
                print('num_char:',num_character)


    if character==1:
        base_file = os.path.join(path_addon,'WHAM','output','demo','video')
        file_converted = os.path.join(base_file,'wham_output.pickle')
        file = file_converted
        with open(file, 'rb') as handle:
            b = pickle.load(handle)

        list_characters = []
        for i in b:
            if len(b[i]) >0:
                list_characters.append(str(i))

        num_character = len(list_characters)


        fourd_prop.str_list_characters = json.dumps(list_characters)
    fourd_prop.int_tot_character = num_character

# def simple_gen_exec(context,code): #code: 0 - 4d humans, 1- WHAM, 2-SLAHMR
# def simple_gen_exec(context): 

#     fourd_prop = context.scene.fourd_prop

#     path_addon = os.path.dirname(os.path.abspath(__file__))
#     path_venv = fourd_prop.str_venv_path
#     path_venv_4dhumans = join(path_venv,fourd_prop.str_custom_venv_name) #4d humans venv
#     # path_venv_cuda = join(path_venv,fourd_prop.str_custom_venv_name,'CUDA')
#     path_venv_activate_4dhumans = join(path_venv_4dhumans,'Scripts','activate.bat')
    
#     drive_addon = path_addon.split(':')[0]
#     rest_path_addon = path_addon.split(':')[1]

    # rest_path_stable_diffusion = join(rest_path_addon,'stable-diffusion-main')

    # if os.path.exists(path_venv_activate_4dhumans):
        
        # with open(path_venv_activate_4dhumans, "rt") as fin: #cria um bat com a ativacao do venv e inclui instalacao dos pacotes para Stable diffusion
        #     with open(join(path_addon,'install_SDM_reqs.bat'), "wt") as fout:
        #         for line in fin:
        #             # fout.write(line.replace('####RESULTS_DIR####', folder_prj))
        #             fout.write(line)
        #         fout.write('\nrem %1 - drive env')
        #         fout.write('\nrem %2 - path to venv (wihtout drive)')
        #         fout.write('\nrem %3 - env_folder')
        #         fout.write('\n'+drive_addon+':')
        #         fout.write('\ncd'+rest_path_addon)
        #         fout.write('\ncd')
        #         fout.write('\npython -mpip install -r requirements.txt')
        #         fout.write('\necho --------------------------------------------------------------')
        #         fout.write('\necho YOU CAN CLOSE THIS WINDOW NOW')
        #         fout.write('\necho --------------------------------------------------------------')
                
        # print('Re created install_SDM_reqs.bat')

        # with open(join(path_addon,'stable-diffusion-main','req_local.txt'), "wt") as fout:
        #     fout.write('\n-e '+join(path_venv_full,'src','taming-transformers')+'\\.')
        #     fout.write('\n-e '+join(path_venv_full,'src','CLIP')+'\\.')
        # print('Re created stable-diffusion-main/req_local.bat')

        # with open(path_venv_activate, "rt") as fin: #Generic Python execution
        #     with open(join(path_addon,'execute_python_generic.bat'), "wt") as fout:
        #         for line in fin:
        #             # fout.write(line.replace('####RESULTS_DIR####', folder_prj))
        #             fout.write(line)
        #         fout.write('\n'+drive_addon+':')
        #         fout.write('\ncd'+rest_path_stable_diffusion)

        #         fout.write('\nEcho path of the addon, execute')
        #         fout.write('\ncd')
        #         fout.write('\necho --------------------------------------------------')
        #         fout.write('\npython %*')
        #         # fout.write('\n%*')
        # print('Re created execute_python_generic.bat')


        # with open(path_venv_activate_4dhumans, "rt") as fin: #Generic Python with custom folder
        #     with open(join(path_addon,'execute_python_generic_custom_folder.bat'), "wt") as fout:
        #         for line in fin:
        #             # fout.write(line.replace('####RESULTS_DIR####', folder_prj))
        #             fout.write(line)
        #         fout.write('\nEcho path of the addon, execute')
        #         fout.write('\ncd')
        #         fout.write('\necho --------------------------------------------------')
        #         fout.write('\npython %*')
        #         # fout.write('\n%*')
        # print('Re created execute_python_generic_custom_folder.bat')

        # if code == 1: #1 = WHAM

        #     path_venv_wham_full = join(path_venv,fourd_prop.str_custom_venv_name_wham)
        #     path_venv_activate_wham = join(path_venv_wham_full,'Scripts','activate.bat')

        #     with open(path_venv_activate_wham, "rt") as fin: #cria um bat com a ativacao do venv e inclui instalacao dos pacotes para Stable diffusion
        #         with open(join(path_addon,'execute_python_generic_custom_folder_wham.bat'), "wt") as fout:
        #             for line in fin:
        #                 # fout.write(line.replace('####RESULTS_DIR####', folder_prj))
        #                 fout.write(line)
        #             fout.write('\nEcho path of the addon, execute')
        #             fout.write('\ncd')
        #             fout.write('\necho --------------------------------------------------')
        #             fout.write('\npython %*')
        #             # fout.write('\n%*')
        #     print('Re created execute_python_generic_custom_folder_wham.bat')



def bind(context,rig,target):
    # fourd_prop = context.scene.fourd_prop
    scn = context.scene

    scn.source.select_set(True)
    bpy.context.view_layer.objects.active = scn.source
    
    if bpy.context.active_object.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')

    #etapa 1 - duplica armature origem, e criar constraint de "copy transforms" mix: before original(aligned); target: local; owner: local


    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True) # aplica transform no source



        
    #duplicando armature para apply scale
    bpy.ops.object.select_all(action='DESELECT')
    if target == 'stg2':
        scn.target_stg2.select_set(True)
    else:
        scn.target.select_set(True)
    
    bpy.ops.object.duplicate(linked=False)

    target_duplicate = bpy.context.selected_objects[0]

    #com a armture destino duplicada, apply scale
    # bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)


    scn.source.select_set(True)

    if bpy.context.active_object.mode != 'EDIT':
        bpy.ops.object.mode_set(mode='EDIT')

    #copiando bones, e suas informacoes
    for b in rig:
        if scn.source.name.startswith('STG2_Armature') and b[0] in ["m_avg_root","m_avg_L_Hand","m_avg_R_Hand"]:
            continue
        bone = scn.source.data.edit_bones[b[0]]
        copy_bone = scn.source.data.edit_bones.new(bone.name+'_CEB4D')
        copy_bone.length = bone.length
        if bone.parent:
            copy_bone.parent = scn.source.data.edit_bones[bone.parent.name+'_CEB4D']
        copy_bone.matrix = bone.matrix.copy()
        #colocar copia do destino nesse rig
        if b[1] != '':
            bone_dest = target_duplicate.data.edit_bones[b[1]]
            copy_bone_dest = scn.source.data.edit_bones.new(bone_dest.name+'_CP_CEB4D')
            copy_bone_dest.length = bone_dest.length
            copy_bone_dest.parent = scn.source.data.edit_bones[b[0]+'_CEB4D']
            copy_bone_dest.matrix = bone_dest.matrix.copy()

    #"""
    bpy.ops.object.mode_set(mode='OBJECT')

    for b in rig:
        if scn.source.name.startswith('STG2_Armature') and b[0] in ["m_avg_root","m_avg_L_Hand","m_avg_R_Hand"]:
            continue
        scn.source.pose.bones[b[0]+'_CEB4D'].constraints.new('COPY_TRANSFORMS')
        scn.source.pose.bones[b[0]+'_CEB4D'].constraints[0].target = scn.source
        scn.source.pose.bones[b[0]+'_CEB4D'].constraints[0].subtarget = b[0]
        scn.source.pose.bones[b[0]+'_CEB4D'].constraints[0].mix_mode = 'BEFORE'
        scn.source.pose.bones[b[0]+'_CEB4D'].constraints[0].target_space = 'LOCAL'
        scn.source.pose.bones[b[0]+'_CEB4D'].constraints[0].owner_space = 'LOCAL'




    # fazr a copia do transform do armature clonado
    for b in rig:
        if b[1] != '':
            if target == 'stg2':
                cp_rot = scn.target_stg2.pose.bones[b[1]].constraints.new('COPY_ROTATION')
            else:
                cp_rot = scn.target.pose.bones[b[1]].constraints.new('COPY_ROTATION')
            cp_rot.name = cp_rot.name + '_CEB4D'
            cp_rot.target = scn.source
            cp_rot.subtarget = b[1]+'_CP_CEB4D'
        if b[0] == 'm_avg_Pelvis':
            # if context.scene.target.name.startswith('STG2_'):
            if target == 'stg2':
                cp_loc = scn.target_stg2.pose.bones['Ctrl_Hips'].constraints.new('COPY_LOCATION')
            else:
                cp_loc = scn.target.pose.bones[b[1]].constraints.new('COPY_LOCATION')
            cp_loc.name = cp_loc.name + '_CEB4D'
            cp_loc.target = scn.source
            cp_loc.subtarget = b[0] 

    #apagar a copia do armature que fiz para "apply scale"
    bpy.ops.object.select_all(action='DESELECT')
    target_duplicate.select_set(True)
    bpy.context.view_layer.objects.active = target_duplicate
    bpy.ops.object.delete() #apaga duplicata que fiz "apply transforms"

    if target == 'stg2':
        scn.target_stg2['bind']=1
    else:
        scn.target['bind']=1


# def unbind(context,type): #type = 0 apenas unbind, type =1 retaarget e depois unbind
def unbind(context,target): 
    scn = context.scene
    armature = context.scene.source
    armature.select_set(True)
    bpy.context.view_layer.objects.active = armature #estou selecionando o armature aqui para poder fazer o mode abaixo funcionar, caso o personagem nao esteja selecionado


    if bpy.context.active_object.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')

    bpy.ops.object.select_all(action='DESELECT')

    armature.select_set(True)
    bpy.context.view_layer.objects.active = armature


    if target == 'stg2':
        for b in scn.target_stg2.pose.bones:
            for b_c in b.constraints:
                if b_c.name.endswith('_CEB4D'):
                    b.constraints.remove(b_c)
        scn.target_stg2['bind']=0
    else:
        for b in scn.target.pose.bones:
            for b_c in b.constraints:
                if b_c.name.endswith('_CEB4D'):
                    b.constraints.remove(b_c)
        scn.target['bind']=0


    ## apagando bones criados
    bpy.ops.object.mode_set(mode='EDIT')
    for bone in armature.data.edit_bones:
        # print(bone.name)
        if bone.name.find("_CEB4D")> 0: 
            # print('apagar: ',bone.name)
            armature.data.edit_bones.remove(bone)

    bpy.ops.object.mode_set(mode='OBJECT')


def retarget(context,target):
    fourd_prop = context.scene.fourd_prop
    scn = context.scene

    if target == 'stg2':
        scn.target_stg2.select_set(True)
        bpy.context.view_layer.objects.active = scn.target_stg2
    else:
        scn.target.select_set(True)
        bpy.context.view_layer.objects.active = scn.target

    start_frame = context.scene.frame_start
    end_frame = context.scene.frame_end
    # if context.scene.target.name.startswith('STG2_'):
    if target == 'stg2':
        bpy.ops.nla.bake(frame_start=start_frame, frame_end=end_frame, 
                    only_selected=fourd_prop.bool_selected_bones, visual_keying=True, clear_constraints=False, 
                    clear_parents=False, use_current_action=True, clean_curves=False, bake_types={'POSE'})
    else:
        bpy.ops.nla.bake(frame_start=start_frame, frame_end=end_frame, 
                    only_selected=fourd_prop.bool_selected_bones, visual_keying=True, clear_constraints=True, 
                    clear_parents=False, use_current_action=True, clean_curves=False, bake_types={'POSE'})
    
    #removendo bones criados no bind
    unbind(context,target)
    
    if fourd_prop.bool_retarget_hide_source:
        scn.source.hide_render = True
        scn.source.hide_viewport = True

        for ob in bpy.data.objects:
            if ob.parent == scn.source:
                src_mesh = ob
                print('found mesh')
        src_mesh.hide_viewport = True
        src_mesh.hide_render = True    

    if target == 'stg2':
        scn.target_stg2['bind']=0    
    else:
        scn.target['bind']=0    

class CreateVirtualEnviroment(Operator):

    bl_idname = "fdh.create_virtual_env"
    bl_label = "Create Venv"
    bl_description = "Create Virtual Enviroment"

    def execute(self,context):

        import subprocess
        import sys

        fourd_prop = context.scene.fourd_prop
        path_addon = os.path.dirname(os.path.abspath(__file__))
        path_venv = fourd_prop.str_venv_path
        env_folder_name = fourd_prop.str_custom_venv_name
        # path_pip_ini = join(path_venv,fourd_prop.str_custom_venv_name,'pip.ini')

        drive_env = path_venv.split(':')[0]
        # rest_path_env = path_venv.split(':')[1]

        # install venv
        os.chdir(path_venv)#muda diretorio 
        if os.path.exists(join(path_venv,fourd_prop.str_custom_venv_name)):
            print('Environment already created')
        else:
            subprocess.run([join(path_addon,'install_venv_p310.bat'),drive_env, path_addon , path_venv, env_folder_name]) #Cria o venv
        
        #arquivo criado para poder usar o pip pra instalar tudo de uma so vez
        # with open(path_pip_ini, "wt") as fout:
        #     fout.write('[global]')
        #     fout.write('\nindex-url=https://pypi.org/simple')
        #     fout.write('\nextra-index-url=https://download.pytorch.org/whl/cu116')
        # print('pip.ini file created')

        # simple_gen_exec(context)
        # simple_gen_exec(context,0) #code: 0 - 4d humans, 1- WHAM, 2-SLAHMR
    

        return{'FINISHED'}


class CreateVirtualEnviromentWHAM(Operator):

    bl_idname = "fdh.create_virtual_env_wham"
    bl_label = "Create WHAM Venv"
    bl_description = "Create Virtual Enviroment for WHAM"

    def execute(self,context):

        import subprocess
        import sys

        fourd_prop = context.scene.fourd_prop
        path_addon = os.path.dirname(os.path.abspath(__file__))
        path_venv = fourd_prop.str_venv_path
        env_folder_name_wham = fourd_prop.str_custom_venv_name_wham
        # path_pip_ini = join(path_venv,fourd_prop.str_custom_venv_name,'pip.ini')

        drive_env = path_venv.split(':')[0]
        # rest_path_env = path_venv.split(':')[1]

        # install venv
        os.chdir(path_venv)#muda diretorio 
        if os.path.exists(join(path_venv,fourd_prop.str_custom_venv_name_wham)):
            print('Environment already created')
        else:
            subprocess.run([join(path_addon,'install_venv_p39.bat'),drive_env, path_addon , path_venv, env_folder_name_wham]) #Cria o venv
        
        #arquivo criado para poder usar o pip pra instalar tudo de uma so vez
        # with open(path_pip_ini, "wt") as fout:
        #     fout.write('[global]')
        #     fout.write('\nindex-url=https://pypi.org/simple')
        #     fout.write('\nextra-index-url=https://download.pytorch.org/whl/cu116')
        # print('pip.ini file created')

        # simple_gen_exec(context)
        # simple_gen_exec(context,1) #code: 0 - 4d humans, 1- WHAM, 2-SLAHMR
        
        return{'FINISHED'}

class CreateVirtualEnviromentSLAHMR(Operator):

    bl_idname = "fdh.create_virtual_env_slahmr"
    bl_label = "Create SLAHMR Venv"
    bl_description = "Create Virtual Enviroment for SLAHMR"

    def execute(self,context):

        import subprocess
        import sys

        fourd_prop = context.scene.fourd_prop
        path_addon = os.path.dirname(os.path.abspath(__file__))
        path_venv = fourd_prop.str_venv_path
        env_folder_name_wham = fourd_prop.str_custom_venv_name_slahmr
        # path_pip_ini = join(path_venv,fourd_prop.str_custom_venv_name,'pip.ini')

        drive_env = path_venv.split(':')[0]
        # rest_path_env = path_venv.split(':')[1]

        # install venv
        os.chdir(path_venv)#muda diretorio 
        if os.path.exists(join(path_venv,fourd_prop.str_custom_venv_name_slahmr)):
            print('Environment already created')
        else:
            # subprocess.run([join(path_addon,'install_venv_p39.bat'),drive_env, path_addon , path_venv, env_folder_name_wham]) #Cria o venv
            subprocess.run([join(path_addon,'install_venv_p310.bat'),drive_env, path_addon , path_venv, env_folder_name_wham]) #Cria o venv

        # simple_gen_exec(context)
        # simple_gen_exec(context,2) #code: 0 - 4d humans, 1- WHAM, 2-SLAHMR
        
        return{'FINISHED'}


class InstallPYTORCHOnVenv(Operator):

    bl_idname = "fdh.install_pytorch_venv"
    bl_label = "Install Pytorch on Venv"
    bl_description = "Install Pytorch, only needed you you dont have one already with the same version this addon needs"

    def execute(self,context):

        path_addon = os.path.dirname(os.path.abspath(__file__))
        fourd_prop = context.scene.fourd_prop
        path_venv = fourd_prop.str_venv_path
        path_venv_full = join(path_venv,fourd_prop.str_custom_venv_name)
        batch_file = 'install_pytorch.bat'

        with open(join(path_addon,batch_file), "wt") as fout:
            fout.write('call \"'+join(path_venv_full,'Scripts','activate.bat')+'\"')
            # fout.write('\npython sdm_unips/main_batch.py --session_name results --target '+fourd_prop.enum_target+' --test_dir "'+path_batch+'" --checkpoint "'+path_ckpt+'" %*')
            fout.write('\npython -mpip install torch==1.13.0 torchvision==0.14.0 --index-url https://download.pytorch.org/whl/cu117')

            fout.write('\n@echo -----------------------------------------------')
            fout.write('\n@echo --------- YOU CAN CLOSE THIS WINDOW  ----------')
            fout.write('\n@echo -----------------------------------------------')

        #Executa oprocesso
        os.system('start cmd /k \""'+join(path_addon,'install_pytorch.bat')+'" \"')

        return{'FINISHED'}


class InstallPYTORCHOnVenvWHAM(Operator):

    bl_idname = "fdh.install_pytorch_venv_wham"
    bl_label = "Install Pytorch wham on Venv"
    bl_description = "Install Pytorch, only needed you you dont have one already with the same version this addon needs"

    def execute(self,context):

        path_addon = os.path.dirname(os.path.abspath(__file__))
        fourd_prop = context.scene.fourd_prop
        path_venv = fourd_prop.str_venv_path
        path_venv_full = join(path_venv,fourd_prop.str_custom_venv_name_wham)
        batch_file = 'install_pytorch_wham.bat'

        with open(join(path_addon,batch_file), "wt") as fout:
            fout.write('call \"'+join(path_venv_full,'Scripts','activate.bat')+'\"')
            # fout.write('\npython sdm_unips/main_batch.py --session_name results --target '+fourd_prop.enum_target+' --test_dir "'+path_batch+'" --checkpoint "'+path_ckpt+'" %*')
            fout.write('\npython -mpip install torch==1.11.0+cu113 torchvision==0.12.0+cu113 torchaudio==0.11.0 --extra-index-url https://download.pytorch.org/whl/cu113')

            fout.write('\n@echo -----------------------------------------------')
            fout.write('\n@echo --------- YOU CAN CLOSE THIS WINDOW  ----------')
            fout.write('\n@echo -----------------------------------------------')

        #Executa oprocesso
        os.system('start cmd /k \""'+join(path_addon,'install_pytorch_wham.bat')+'" \"')

        return{'FINISHED'}

class InstallPYTORCHOnVenvSLAHMR(Operator):

    bl_idname = "fdh.install_pytorch_venv_slahmr"
    bl_label = "Install Pytorch slahmr on Venv"
    bl_description = "Install Pytorch, only needed you you dont have one already with the same version this addon needs"

    def execute(self,context):

        path_addon = os.path.dirname(os.path.abspath(__file__))
        fourd_prop = context.scene.fourd_prop
        path_venv = fourd_prop.str_venv_path
        path_venv_full = join(path_venv,fourd_prop.str_custom_venv_name_slahmr)
        batch_file = 'install_pytorch_slahmr.bat'
        drive_addon = path_addon.split(':')[0]
        rest_path_addon = path_addon.split(':')[1]

        with open(join(path_addon,batch_file), "wt") as fout:
            fout.write('call \"'+join(path_venv_full,'Scripts','activate.bat')+'\"')
            # fout.write('\npython sdm_unips/main_batch.py --session_name results --target '+fourd_prop.enum_target+' --test_dir "'+path_batch+'" --checkpoint "'+path_ckpt+'" %*')
            fout.write('\npython -mpip install torch==1.13.0 torchvision==0.14.0 --index-url https://download.pytorch.org/whl/cu117')
            # fout.write('\npython -mpip install torch-scatter -f https://data.pyg.org/whl/torch-1.13.0+cu117.html')
            fout.write('\n'+drive_addon+':')
            fout.write('\ncd "'+rest_path_addon+'"')
            fout.write('\ncd "slahmr"')
            fout.write('\npython -mpip install torch_scatter-2.1.1+pt113cu117-cp310-cp310-win_amd64.whl')

            fout.write('\n@echo -----------------------------------------------')
            fout.write('\n@echo --------- YOU CAN CLOSE THIS WINDOW  ----------')
            fout.write('\n@echo -----------------------------------------------')

        #Executa oprocesso
        os.system('start cmd /k \""'+join(path_addon,batch_file)+'" \"')

        return{'FINISHED'}


class InstallPREDETECTRONOnVenv(Operator):

    bl_idname = "fdh.install_pre_detectron_venv"
    bl_label = "Install Pre Detectron on Venv"
    bl_description = "Install Pre Detectron"

    def execute(self,context):

        path_addon = os.path.dirname(os.path.abspath(__file__))
        fourd_prop = context.scene.fourd_prop
        path_venv = fourd_prop.str_venv_path
        path_venv_full = join(path_venv,fourd_prop.str_custom_venv_name)
        batch_file = 'install_pre_detectron.bat'

        drive_addon = path_addon.split(':')[0]
        rest_path_addon = path_addon.split(':')[1]

        with open(join(path_addon,batch_file), "wt") as fout:
            fout.write('call \"'+join(path_venv_full,'Scripts','activate.bat')+'\"')
            # fout.write('\npython sdm_unips/main_batch.py --session_name results --target '+fourd_prop.enum_target+' --test_dir "'+path_batch+'" --checkpoint "'+path_ckpt+'" %*')
            fout.write('\nset python_include="'+path_addon+'\\python_source\\include"')
            fout.write('\nset python_pc="'+path_addon+'\\python_source\\PC"')
            fout.write('\nset python_libs="'+path_addon+'\\python_source\\libs"')
            fout.write('\nset INCLUDE=%python_include%;%python_pc%;%INCLUDE%')
            fout.write('\nset LIB=%python_libs%;%LIB%')
            fout.write('\npython -mpip install pywin32==305')
            fout.write('\npython -mpip install Cython')
            fout.write('\npython -mpip install git+https://github.com/facebookresearch/fvcore')

            fout.write('\n'+drive_addon+':')
            fout.write('\ncd "'+rest_path_addon+'"')
            fout.write('\npython -mpip install pycocotools-2.0-cp310-cp310-win_amd64.whl')
            # fout.write('\ncd ..')
            # fout.write('\npython -mpip install git+https://github.com/philferriere/cocoapi.git#subdirectory=PythonAPI')
            fout.write('\npython -mpip install av==10.0.0')
            fout.write('\npython -mpip install scipy==1.10.0')
            fout.write('\npython -mpip install ninja')
            
            fout.write('\n@echo -----------------------------------------------')
            fout.write('\n@echo --------- YOU CAN CLOSE THIS WINDOW  ----------')
            fout.write('\n@echo -----------------------------------------------')
            


            # fout.write('\npython -mpip install numpy==1.23.0')
            # fout.write('\npython -mpip install -r "'+os.path.join(path_addon,'requirements_pre_detectron2.txt"'))

        #Executa oprocesso
        os.system('start cmd /k \""'+join(path_addon,'install_pre_detectron.bat')+'" \"')
        
        return{'FINISHED'}


class InstallWHAMOnVenv(Operator):

    bl_idname = "fdh.install_wham_venv"
    bl_label = "Install WHAM Reqs on Venv"
    bl_description = "Install WHAM"

    def execute(self,context):

        path_addon = os.path.dirname(os.path.abspath(__file__))
        fourd_prop = context.scene.fourd_prop
        path_venv = fourd_prop.str_venv_path
        path_venv_full = join(path_venv,fourd_prop.str_custom_venv_name_wham)
        batch_file = 'install_WHAM.bat'

        drive_addon = path_addon.split(':')[0]
        rest_path_addon = path_addon.split(':')[1]

        with open(join(path_addon,batch_file), "wt") as fout:
            fout.write('call \"'+join(path_venv_full,'Scripts','activate.bat')+'\"')
            # fout.write('\npython sdm_unips/main_batch.py --session_name results --target '+fourd_prop.enum_target+' --test_dir "'+path_batch+'" --checkpoint "'+path_ckpt+'" %*')
            # fout.write('\nset python_include="'+path_addon+'\\python_source\\include"')
            # fout.write('\nset python_pc="'+path_addon+'\\python_source\\PC"')
            # fout.write('\nset python_libs="'+path_addon+'\\python_source\\libs"')
            # fout.write('\nset INCLUDE=%python_include%;%python_pc%;%INCLUDE%')
            # fout.write('\nset LIB=%python_libs%;%LIB%')
            # fout.write('\npython -mpip install pywin32==305')
            # fout.write('\npython -mpip install Cython')
            # fout.write('\npython -mpip install git+https://github.com/facebookresearch/fvcore')

            fout.write('\n'+drive_addon+':')
            fout.write('\ncd "'+rest_path_addon+'"')
            fout.write('\ncd "WHAM"')
            fout.write('\npython -mpip install -r requirements_wham.txt')
            fout.write('\npython -mpip install mmpose-0.24.0-py2.py3-none-any.whl')
            fout.write('\npython -mpip install dpvo-0.0.0-cp39-cp39-win_amd64.whl')
            # fout.write('\ncd ..')
            # fout.write('\npython -mpip install git+https://github.com/philferriere/cocoapi.git#subdirectory=PythonAPI')
            # fout.write('\npython -mpip install scipy==1.10.0')
            # fout.write('\npython -mpip install ninja')
            
            fout.write('\n@echo -----------------------------------------------')
            fout.write('\n@echo --------- YOU CAN CLOSE THIS WINDOW  ----------')
            fout.write('\n@echo -----------------------------------------------')
            


            # fout.write('\npython -mpip install numpy==1.23.0')
            # fout.write('\npython -mpip install -r "'+os.path.join(path_addon,'requirements_pre_detectron2.txt"'))

        #Executa oprocesso
        os.system('start cmd /k \""'+join(path_addon,'install_WHAM.bat')+'" \"')
        
        return{'FINISHED'}



class InstallSLAHMROnVenv(Operator):

    bl_idname = "fdh.install_slahmr_venv_reqs"
    bl_label = "Install SLAHMR Reqs on Venv"
    bl_description = "Install SLAHMR"

    def execute(self,context):

        path_addon = os.path.dirname(os.path.abspath(__file__))
        fourd_prop = context.scene.fourd_prop
        path_venv = fourd_prop.str_venv_path
        path_venv_full = join(path_venv,fourd_prop.str_custom_venv_name_slahmr)
        batch_file = 'install_SLAHMR.bat'

        drive_addon = path_addon.split(':')[0]
        rest_path_addon = path_addon.split(':')[1]

        with open(join(path_addon,batch_file), "wt") as fout:
            fout.write('call \"'+join(path_venv_full,'Scripts','activate.bat')+'\"')

            fout.write('\n'+drive_addon+':')
            fout.write('\ncd "'+rest_path_addon+'"')
            fout.write('\ncd "slahmr"')
            fout.write('\npython -mpip install -r requirements_slahmr.txt')
            # fout.write('\npython -mpip install mmpose-0.24.0-py2.py3-none-any.whl')
            # fout.write('\npython -mpip install dpvo-0.0.0-cp39-cp39-win_amd64.whl')
            # fout.write('\ncd ..')
            
            fout.write('\n@echo -----------------------------------------------')
            fout.write('\n@echo --------- YOU CAN CLOSE THIS WINDOW  ----------')
            fout.write('\n@echo -----------------------------------------------')

        #Executa oprocesso
        os.system('start cmd /k \""'+join(path_addon,batch_file)+'" \"')
        
        return{'FINISHED'}


class DownloadWHAMCheckpoints(Operator):

    bl_idname = "fdh.download_whan_checkpoints"
    bl_label = "WHAM Checkpoints"
    bl_description = "WHAM Checkpoints"

    def execute(self,context):

        path_addon = os.path.dirname(os.path.abspath(__file__))
        fourd_prop = context.scene.fourd_prop
        path_venv = fourd_prop.str_venv_path
        path_venv_full = join(path_venv,fourd_prop.str_custom_venv_name_wham)
        batch_file = 'install_WHAM_checkpoints.bat'

        drive_addon = path_addon.split(':')[0]
        rest_path_addon = path_addon.split(':')[1]

        with open(join(path_addon,batch_file), "wt") as fout:
            fout.write('call \"'+join(path_venv_full,'Scripts','activate.bat')+'\"')

            fout.write('\n'+drive_addon+':')
            fout.write('\ncd "'+rest_path_addon+'"')
            fout.write('\ncd "WHAM"')
            # fout.write('\npython -mpip install -r requirements_wham.txt')
            fout.write('\nif not exist "checkpoints" mkdir checkpoints')
            fout.write('\nif not exist "checkpoints/wham_vit_w_3dpw.pth.tar" gdown "https://drive.google.com/uc?id=1i7kt9RlCCCNEW2aYaDWVr-G778JkLNcB&export=download&confirm=t" -O "checkpoints/wham_vit_w_3dpw.pth.tar"')
            fout.write('\nif not exist "checkpoints/wham_vit_bedlam_w_3dpw.pth.tar" gdown "https://drive.google.com/uc?id=19qkI-a6xuwob9_RFNSPWf1yWErwVVlks&export=download&confirm=t" -O "checkpoints/wham_vit_bedlam_w_3dpw.pth.tar"')
            fout.write('\nif not exist "checkpoints/hmr2a.ckpt" gdown "https://drive.google.com/uc?id=1J6l8teyZrL0zFzHhzkC7efRhU0ZJ5G9Y&export=download&confirm=t" -O "checkpoints/hmr2a.ckpt"')
            fout.write('\nif not exist "checkpoints/dpvo.pth" gdown "https://drive.google.com/uc?id=1kXTV4EYb-BI3H7J-bkR3Bc4gT9zfnHGT&export=download&confirm=t" -O "checkpoints/dpvo.pth"')
            fout.write('\nif not exist "checkpoints/yolov8x.pt" gdown "https://drive.google.com/uc?id=1zJ0KP23tXD42D47cw1Gs7zE2BA_V_ERo&export=download&confirm=t" -O "checkpoints/yolov8x.pt"')
            fout.write('\nif not exist "checkpoints/vitpose-h-multi-coco.pth" gdown "https://drive.google.com/uc?id=1xyF7F3I7lWtdq82xmEPVQ5zl4HaasBso&export=download&confirm=t" -O "checkpoints/vitpose-h-multi-coco.pth"')
            
            # fout.write('\ncd ..')
            # fout.write('\npython -mpip install git+https://github.com/philferriere/cocoapi.git#subdirectory=PythonAPI')
            # fout.write('\npython -mpip install scipy==1.10.0')
            # fout.write('\npython -mpip install ninja')
            
            fout.write('\n@echo -----------------------------------------------')
            fout.write('\n@echo --------- YOU CAN CLOSE THIS WINDOW  ----------')
            fout.write('\n@echo -----------------------------------------------')
            


            # fout.write('\npython -mpip install numpy==1.23.0')
            # fout.write('\npython -mpip install -r "'+os.path.join(path_addon,'requirements_pre_detectron2.txt"'))

        #Executa oprocesso
        os.system('start cmd /k \""'+join(path_addon,batch_file)+'" \"')
        
        return{'FINISHED'}



class DownloadWHAMBodymodels(Operator):

    bl_idname = "fdh.download_whan_bodymodels"
    bl_label = "WHAM BodyModels"
    bl_description = "WHAM BodyModels"

    def execute(self,context):

        path_addon = os.path.dirname(os.path.abspath(__file__))
        fourd_prop = context.scene.fourd_prop
        path_venv = fourd_prop.str_venv_path
        path_venv_full = join(path_venv,fourd_prop.str_custom_venv_name_wham)
        batch_file = 'install_WHAM_bodymodels.bat'

        drive_addon = path_addon.split(':')[0]
        rest_path_addon = path_addon.split(':')[1]

        with open(join(path_addon,batch_file), "wt") as fout:
            fout.write('call \"'+join(path_venv_full,'Scripts','activate.bat')+'\"')

            fout.write('\n'+drive_addon+':')
            fout.write('\ncd "'+rest_path_addon+'"')
            # fout.write('\ncd "WHAM"')
            # fout.write('\npython -mpip install -r requirements_wham.txt')
            # fout.write('\nif not exist "dataset" mkdir dataset')
            # fout.write('\nif not exist "dataset/body_models.tar.gz" gdown "https://drive.google.com/uc?id=1pbmzRbWGgae6noDIyQOnohzaVnX_csUZ&export=download&confirm=t" -O "dataset/body_models.tar.gz"')

            fout.write('\ntartool wham/body_models.tar.gz wham/dataset')
            
            
            fout.write('\n@echo -----------------------------------------------')
            fout.write('\n@echo --------- YOU CAN CLOSE THIS WINDOW  ----------')
            fout.write('\n@echo -----------------------------------------------')

        #Executa oprocesso
        os.system('start cmd /k \""'+join(path_addon,batch_file)+'" \"')
        
        return{'FINISHED'}

class InstallDETECTRONOnVenv(Operator):

    bl_idname = "fdh.install_detectron_venv"
    bl_label = "Install Detectron on Venv"
    bl_description = "Install Detectron"

    def execute(self,context):

        path_addon = os.path.dirname(os.path.abspath(__file__))
        fourd_prop = context.scene.fourd_prop
        path_venv = fourd_prop.str_venv_path
        path_venv_full = join(path_venv,fourd_prop.str_custom_venv_name)
        batch_file = 'install_detectron.bat'
        drive_addon = path_addon.split(':')[0]
        rest_path_addon = path_addon.split(':')[1]

        with open(join(path_addon,batch_file), "wt") as fout:
            fout.write('call \"'+join(path_venv_full,'Scripts','activate.bat')+'\"')
            # fout.write('\npython sdm_unips/main_batch.py --session_name results --target '+fourd_prop.enum_target+' --test_dir "'+path_batch+'" --checkpoint "'+path_ckpt+'" %*')
            # fout.write('\nset python_include="'+path_addon+'\\python_source\\include"')
            # fout.write('\nset python_pc="'+path_addon+'\\python_source\\PC"')
            # fout.write('\nset python_libs="'+path_addon+'\\python_source\\libs"')
            # fout.write('\nset INCLUDE=%python_pc%;%python_include%;%INCLUDE%')
            # fout.write('\nset LIB=%python_libs%;%LIB%')
            # fout.write('\npython -mpip install git+https://github.com/facebookresearch/detectron2.git')
            fout.write('\n'+drive_addon+':')
            fout.write('\ncd "'+rest_path_addon+'"')
            fout.write('\npython -mpip install detectron2-0.6-cp310-cp310-win_amd64.whl')
            fout.write('\npython -mpip install mmcv_full-1.6.0-cp310-cp310-win_amd64.whl')
            # fout.write('\npython -mpip install pytorch-lightning==2.2.5 smplx==0.1.28 pyrender opencv-python yacs scikit-image einops timm webdataset rich dill joblib scenedetect scikit-learn==1.3.0 pytube chumpy numpy==1.23.0')
            fout.write('\npython -mpip install pytorch-lightning==2.2.5 smplx==0.1.28 pyrender==0.1.45 opencv-python==4.10.0.82 yacs==0.1.8 scikit-image==0.23.2 einops==0.8.0 timm==1.0.3 webdataset==0.2.86 rich==13.7.1 dill==0.3.8 joblib==1.4.2 scenedetect==0.6.4 scikit-learn==1.3.0 pytube==15.0.0 chumpy==0.70 numpy==1.23.0')

            fout.write('\n@echo -----------------------------------------------')
            fout.write('\n@echo --------- YOU CAN CLOSE THIS WINDOW  ----------')
            fout.write('\n@echo -----------------------------------------------')


        #Executa oprocesso
        os.system('start cmd /k \""'+join(path_addon,'install_detectron.bat')+'" \"')

        return{'FINISHED'}

class InstallDETECTRONOnVenvSLAHMR(Operator):

    bl_idname = "fdh.install_detectron_venv_slahmr"
    bl_label = "Install Detectron"
    bl_description = "Install Detectron SLAHMR"

    def execute(self,context):

        path_addon = os.path.dirname(os.path.abspath(__file__))
        fourd_prop = context.scene.fourd_prop
        path_venv = fourd_prop.str_venv_path
        path_venv_full = join(path_venv,fourd_prop.str_custom_venv_name_slahmr)
        batch_file = 'install_detectron_slahmr.bat'
        drive_addon = path_addon.split(':')[0]
        rest_path_addon = path_addon.split(':')[1]

        with open(join(path_addon,batch_file), "wt") as fout:
            fout.write('call \"'+join(path_venv_full,'Scripts','activate.bat')+'\"')
            # fout.write('\npython sdm_unips/main_batch.py --session_name results --target '+fourd_prop.enum_target+' --test_dir "'+path_batch+'" --checkpoint "'+path_ckpt+'" %*')
            # fout.write('\nset python_include="'+path_addon+'\\python_source\\include"')
            # fout.write('\nset python_pc="'+path_addon+'\\python_source\\PC"')
            # fout.write('\nset python_libs="'+path_addon+'\\python_source\\libs"')
            # fout.write('\nset INCLUDE=%python_pc%;%python_include%;%INCLUDE%')
            # fout.write('\nset LIB=%python_libs%;%LIB%')
            # fout.write('\npython -mpip install git+https://github.com/facebookresearch/detectron2.git')
            fout.write('\n'+drive_addon+':')
            fout.write('\ncd "'+rest_path_addon+'"')
            fout.write('\ncd "slahmr"')

            fout.write('\npython -mpip install detectron2-0.6-cp310-cp310-win_amd64.whl')
            # fout.write('\npython -mpip install torch_scatter-2.1.1+pt113cu117-cp310-cp310-win_amd64.whl')
            

            fout.write('\n@echo -----------------------------------------------')
            fout.write('\n@echo --------- YOU CAN CLOSE THIS WINDOW  ----------')
            fout.write('\n@echo -----------------------------------------------')


        #Executa oprocesso
        os.system('start cmd /k \""'+join(path_addon,batch_file)+'" \"')

        return{'FINISHED'}

class InstallSLAHMRandRESTOnVenv(Operator):

    bl_idname = "fdh.install_slahmr_and_rest_venv"
    bl_label = "Install SLAHMR and others on Venv"
    bl_description = "Install SLAHMR & Others"

    def execute(self,context):

        path_addon = os.path.dirname(os.path.abspath(__file__))
        fourd_prop = context.scene.fourd_prop
        path_venv = fourd_prop.str_venv_path
        path_venv_full = join(path_venv,fourd_prop.str_custom_venv_name_slahmr)
        batch_file = 'install_slahmr_and_others.bat'
        drive_addon = path_addon.split(':')[0]
        rest_path_addon = path_addon.split(':')[1]

        with open(join(path_addon,batch_file), "wt") as fout:
            fout.write('call \"'+join(path_venv_full,'Scripts','activate.bat')+'\"')
            fout.write('\n'+drive_addon+':')
            fout.write('\ncd "'+rest_path_addon+'"')
            fout.write('\ncd "slahmr"')

            fout.write('\npython -mpip install slahmr-0.0.0-py3-none-any.whl')
            fout.write('\npython -mpip install mmpose-0.24.0-py2.py3-none-any.whl')
            fout.write('\npython -mpip install droid_backends-0.0.0-cp310-cp310-win_amd64.whl')
            fout.write('\npython -mpip install lietorch-0.2-cp310-cp310-win_amd64.whl')
            fout.write('\npython -mpip install phalp-0.1.3-py3-none-any.whl')
            fout.write('\npython -mpip install pandas==1.4.0')
            fout.write('\npython -mpip install pytorch-lightning==2.2.0')
            fout.write('\npython -mpip install webdataset==0.2.86')
            fout.write('\npython -mpip install scikit-image==0.22.0')
            fout.write('\npython -mpip install mmcv==1.3.9')
            fout.write('\npython -mpip install git+https://github.com/nghorbani/configer@8cd1e3e556d9697298907800a743e120be57ac36')
            fout.write('\npython -mpip install torchgeometry==0.1.2')


            fout.write('\n@echo -----------------------------------------------')
            fout.write('\n@echo --------- YOU CAN CLOSE THIS WINDOW  ----------')
            fout.write('\n@echo -----------------------------------------------')


        #Executa oprocesso
        os.system('start cmd /k \""'+join(path_addon,batch_file)+'" \"')

        return{'FINISHED'}

class InstallREQPIXELOnVenv(Operator):

    bl_idname = "fdh.install_reqs_venv"
    bl_label = "Install Requirements on Venv"
    bl_description = "Install Requirements"

    def execute(self,context):

        path_addon = os.path.dirname(os.path.abspath(__file__))
        fourd_prop = context.scene.fourd_prop
        path_venv =join(fourd_prop.str_venv_path,fourd_prop.str_custom_venv_name,'src')

        drive = path_venv.split(':')[0]
        rest_path = path_venv.split(':')[1]

        os.system('start cmd /k \""'+join(path_addon,'install_SDM_reqs.bat')+'" '+drive+' '+rest_path+'\"')

        return{'FINISHED'}



class VenvPathSelect(Operator, ImportHelper):
    bl_idname = "fdh.venv_path_select"
    bl_label = "Venv Path"
    bl_description = "Select Venv Path"

    # filename_ext = ".ckpt"
    filter_glob: StringProperty(
        # default="*.ckpt",
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )
    def execute(self,context):
        
        fourd_prop = context.scene.fourd_prop
        path_venv_path = os.path.dirname(self.filepath)
        fourd_prop.str_venv_path = os.path.dirname(self.filepath)

        path_addon = os.path.dirname(os.path.abspath(__file__))
        path_venv_path_txt = join(path_addon,'venv_path.txt')

        with open(path_venv_path_txt, "wt") as fout:
            fout.write(path_venv_path)

        # simple_gen_exec(context)

        return{'FINISHED'}



class ImportSMPLPKL(Operator, ImportHelper):
    bl_idname = "fdh.import_smpl_pkl"
    bl_label = "Import SMPL PKL"
    bl_description = "Import SMPL PKL"

    # filename_ext = ".ckpt"
    filter_glob: StringProperty(
        # default= ["*.jpg","*.png"],
        # default= "*.png",
        default= "*",
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )

    files: CollectionProperty(name='File paths', type=bpy.types.OperatorFileListElement)
    directory: StringProperty(subtype='DIR_PATH')

    option: IntProperty(name='character',default=0)#0=male, 1=female, 2=neutral

    def execute(self,context):

        fourd_prop = context.scene.fourd_prop
        fourd_prop.str_videopath = self.filepath
        from shutil import rmtree,copyfile
        # # dfnrmvs_prop = context.scene.dfnrmvs_prop
        path_addon = os.path.dirname(os.path.abspath(__file__))
        
        # base_path_img = os.path.join(path_addon,'4D-Humans-main','datasets','TEST_DATA')
        path_file = os.path.join(path_addon,'wham','dataset','body_models','smpl')

        if not os.path.exists(path_file):
            os.makedirs(path_file)

        src = self.filepath
        if self.option == 0:
            dst = os.path.join(path_file,'SMPL_MALE.pkl')
            print('destination:', dst)
            copyfile(src,dst)
        if self.option == 1:
            dst = os.path.join(path_file,'SMPL_FEMALE.pkl')
            print('destination:', dst)
            copyfile(src,dst)
        if self.option == 2:
            dst = os.path.join(path_file,'SMPL_NEUTRAL.pkl')
            print('destination:', dst)
            copyfile(src,dst)
        if self.option == 3: #for 4d humans
            dst = os.path.join(path_addon,'basicModel_neutral_lbs_10_207_0_v1.0.0.pkl')
            dst2 = os.path.join(path_addon,'basicModel_neutral_lbs_10_207_0_v1.0.0_p3.pkl')

            print("destination",dst)
            copyfile(src,dst)
            batch_file = 'convert_smpl_pkl.bat'
            path_venv = fourd_prop.str_venv_path
            path_venv_full = join(path_venv,fourd_prop.str_custom_venv_name)
            with open(join(path_addon,batch_file), "wt") as fout:
                fout.write('@echo off\n')
                fout.write('call \"'+join(path_venv_full,'Scripts','activate.bat')+'\"')
                # fout.write('\nset CUDA_DEVICE_ORDER=PCI_BUS_ID')
                # fout.write('\nset CUDA_VISIBLE_DEVICE='+str(fourd_prop.int_gpu))
                fout.write('\npython convert_smpl_pkl_4dhumans.py')
            

            path_folder = join(path_addon)
            current_folder = os.getcwd()
            os.chdir(path_folder)
            run = [join(path_addon,batch_file)]
        
            print('run: ',run)
            # result_run = subprocess.run(run) #Executa 
            result_run = subprocess.Popen(run,stdout=subprocess.PIPE)
            stdout = result_run.communicate()[0]
            print ('STDOUT:{}'.format(stdout))
            stdout_as_str = stdout.decode("utf-8")
            print('Result of SMPL PKL convertion: ',stdout_as_str)
            os.chdir(current_folder)
            
            CACHE_DIR = os.path.join(os.path.expanduser('~'), ".cache")
            smpl_path = os.path.join(CACHE_DIR, "phalp/3D/models/smpl")
            smpl_path2 = os.path.join(CACHE_DIR, "4DHumans/data/smpl")

            smpl_path_final = os.path.join(smpl_path, "SMPL_NEUTRAL.pkl")
            smpl_path2_final = os.path.join(smpl_path2, "SMPL_NEUTRAL.pkl")

            if not os.path.exists(smpl_path):
                os.makedirs(smpl_path)

            if not os.path.exists(smpl_path2):
                os.makedirs(smpl_path2)

            copyfile(dst2,smpl_path_final)
            copyfile(dst2,smpl_path2_final)


        return{'FINISHED'}



class ImportVideo(Operator, ImportHelper):
    bl_idname = "fdh.add_video"
    bl_label = "Select Video"
    bl_description = "Select Video"

    # filename_ext = ".ckpt"
    filter_glob: StringProperty(
        # default= ["*.jpg","*.png"],
        # default= "*.png",
        default= "*",
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )

    files: CollectionProperty(name='File paths', type=bpy.types.OperatorFileListElement)
    directory: StringProperty(subtype='DIR_PATH')

    def execute(self,context):

        fourd_prop = context.scene.fourd_prop
        fourd_prop.str_videopath = self.filepath
        from shutil import rmtree,copyfile
        # # dfnrmvs_prop = context.scene.dfnrmvs_prop
        path_addon = os.path.dirname(os.path.abspath(__file__))
        
        # base_path_img = os.path.join(path_addon,'4D-Humans-main','datasets','TEST_DATA')
        path_file = os.path.join(path_addon,'4D-Humans-main','example_data','videos')

        if os.path.exists(path_file):
            rmtree(path_file)
            os.makedirs(path_file)
        else:
            os.makedirs(path_file)

        src = self.filepath
        dst = os.path.join(path_file,'video.mp4')

        copyfile(src,dst)

        
        # Apagando os arquivo PKL
        base_output = os.path.join(path_addon,'4D-Humans-main','outputs')
                
        if os.path.exists(base_output):
            shutil.rmtree(base_output)
            os.makedirs(base_output, exist_ok=True)
        else:
            os.makedirs(base_output, exist_ok=True)

        # Limpando caminho pkl, se tiver importado algum dado lipando deve evitar confusão de qual PKL esta disponivel
        fourd_prop.str_pklpath = ''
        # Zerando a quantidade de chracters vai impedir que o botao import Raw apareca
        fourd_prop.int_tot_character=0

        # Alterando propriedades para o valor FPS que esta no painel
        context.scene.render.fps = int(fourd_prop.enum_fps)

        #pegando total de frames do video
        batch_file_qtd = 'qtd_frames.bat'
        path_venv = fourd_prop.str_venv_path
        path_venv_full = join(path_venv,fourd_prop.str_custom_venv_name)
        with open(join(path_addon,batch_file_qtd), "wt") as fout:
            fout.write('@echo off\n')
            fout.write('call \"'+join(path_venv_full,'Scripts','activate.bat')+'\"')
            # fout.write('\nset CUDA_DEVICE_ORDER=PCI_BUS_ID')
            # fout.write('\nset CUDA_VISIBLE_DEVICE='+str(fourd_prop.int_gpu))
            fout.write('\npython qtd_frames_video.py')

        path_folder = join(path_addon)
        current_folder = os.getcwd()
        os.chdir(path_folder)

        run = [join(path_addon,batch_file_qtd)]
        
        print('run: ',run)
        # result_run = subprocess.run(run) #Executa 
        result_run = subprocess.Popen(run,stdout=subprocess.PIPE)
        stdout = result_run.communicate()[0]
        # print ('STDOUT:{}'.format(stdout))
        stdout_as_str = stdout.decode("utf-8")
        
        # print('result_run: ',stdout)
        print('amount of frames: ',stdout_as_str)
        os.chdir(current_folder)
            


        #reescrevendo o base.py para colocar o total de frames do video atual
        path_file = os.path.join(path_addon,'4D-Humans-main','example_data','videos')
        
        # with open('4D-Humans-main/PHALP/phalp/configs/base_ref.py', "rt") as fin:
        #     with open('4D-Humans-main/PHALP/phalp/configs/base.py', "wt") as fout:
        #         for line in fin:
        #             fout.write(line.replace('####QTD_FRAMES####', stdout_as_str))

        with open(os.path.join(path_addon,'4D-Humans-main','PHALP','phalp','configs','base_ref.py'), "rt") as fin:
            with open(os.path.join(path_addon,'4D-Humans-main','PHALP','phalp','configs','base.py'), "wt") as fout:
                for line in fin:
                    fout.write(line.replace('####QTD_FRAMES####', stdout_as_str))

        return{'FINISHED'}
    

class ImportVideoWHAM(Operator, ImportHelper):
    bl_idname = "fdh.add_video_wham"
    bl_label = "Select Video"
    bl_description = "Select Video"

    # filename_ext = ".ckpt"
    filter_glob: StringProperty(
        # default= ["*.jpg","*.png"],
        # default= "*.png",
        default= "*",
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )

    files: CollectionProperty(name='File paths', type=bpy.types.OperatorFileListElement)
    directory: StringProperty(subtype='DIR_PATH')

    def execute(self,context):

        fourd_prop = context.scene.fourd_prop
        fourd_prop.str_videopath = self.filepath
        from shutil import rmtree,copyfile
        # # dfnrmvs_prop = context.scene.dfnrmvs_prop
        path_addon = os.path.dirname(os.path.abspath(__file__))
        
        # base_path_img = os.path.join(path_addon,'4D-Humans-main','datasets','TEST_DATA')
        path_file = os.path.join(path_addon,'wham','example_data')

        if os.path.exists(path_file):
            rmtree(path_file)
            os.makedirs(path_file)
        else:
            os.makedirs(path_file)

        src = self.filepath
        dst = os.path.join(path_file,'video.mp4')

        copyfile(src,dst)

        
        # Apagando os arquivo PKL
        base_output = os.path.join(path_addon,'wham','output')
                
        if os.path.exists(base_output):
            shutil.rmtree(base_output)
            os.makedirs(base_output, exist_ok=True)
        else:
            os.makedirs(base_output, exist_ok=True)

        fourd_prop.int_tot_character = 0
        fourd_prop.int_character = 1


        return{'FINISHED'}



class ImportVideoSLAHMR(Operator, ImportHelper):
    bl_idname = "fdh.add_video_slahmr"
    bl_label = "Select Video"
    bl_description = "Select Video"

    # filename_ext = ".ckpt"
    filter_glob: StringProperty(
        # default= ["*.jpg","*.png"],
        # default= "*.png",
        default= "*",
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )

    files: CollectionProperty(name='File paths', type=bpy.types.OperatorFileListElement)
    directory: StringProperty(subtype='DIR_PATH')

    def execute(self,context):

        fourd_prop = context.scene.fourd_prop
        fourd_prop.str_videopath = self.filepath
        from shutil import rmtree,copyfile
        # # dfnrmvs_prop = context.scene.dfnrmvs_prop
        path_addon = os.path.dirname(os.path.abspath(__file__))
        
        # base_path_img = os.path.join(path_addon,'4D-Humans-main','datasets','TEST_DATA')
        path_file = os.path.join(path_addon,'slahmr','data_input')
        path_file_video = os.path.join(path_addon,'slahmr','data_input','videos')
        

        if os.path.exists(path_file):
            rmtree(path_file)
            os.makedirs(path_file_video)
        else:
            os.makedirs(path_file_video)


        src = self.filepath
        dst = os.path.join(path_file_video,'video_slahmr.mp4')

        copyfile(src,dst)

        
        # Apagando os arquivo output
        base_output = os.path.join(path_addon,'slahmr','outputs')


                
        if os.path.exists(base_output):
            shutil.rmtree(base_output)
        #     os.makedirs(base_output, exist_ok=True)
        # else:
        #     os.makedirs(base_output, exist_ok=True)

        fourd_prop.int_tot_character = 0
        fourd_prop.int_character = 1


        #lendo dados do video importado
        #pegando total de frames do video
        batch_file_qtd = 'data_video_slahmr.bat'
        path_venv = fourd_prop.str_venv_path
        path_venv_full = join(path_venv,fourd_prop.str_custom_venv_name_slahmr)
        with open(join(path_addon,batch_file_qtd), "wt") as fout:
            fout.write('@echo off\n')
            fout.write('call \"'+join(path_venv_full,'Scripts','activate.bat')+'\"')
            # fout.write('\nset CUDA_DEVICE_ORDER=PCI_BUS_ID')
            # fout.write('\nset CUDA_VISIBLE_DEVICE='+str(fourd_prop.int_gpu))
            fout.write('\npython qtd_frames_video_slahmr.py')

        path_folder = join(path_addon)
        current_folder = os.getcwd()
        os.chdir(path_folder)

        run = [join(path_addon,batch_file_qtd)]
        
        print('run: ',run)
        # result_run = subprocess.run(run) #Executa 
        result_run = subprocess.Popen(run,stdout=subprocess.PIPE)
        stdout = result_run.communicate()[0]
        # print ('STDOUT:{}'.format(stdout))
        stdout_as_str = stdout.decode("utf-8")
        
        # print('result_run: ',stdout)
        print('amount of frames: ',stdout_as_str)
        os.chdir(current_folder)
            


        #reescrevendo o base.py para colocar o total de frames do video atual
        # path_file = os.path.join(path_addon,'4D-Humans-main','example_data','videos')
        
        # with open('4D-Humans-main/PHALP/phalp/configs/base_ref.py', "rt") as fin:
        #     with open('4D-Humans-main/PHALP/phalp/configs/base.py', "wt") as fout:
        #         for line in fin:
        #             fout.write(line.replace('####QTD_FRAMES####', stdout_as_str))

        start_video = '0'
        length_video = stdout_as_str.split('|')[0]
        fps_video = stdout_as_str.split('|')[1]

        with open(os.path.join(path_addon,'slahmr','slahmr','confs','data','video_ref.yaml'), "rt") as fin:
            with open(os.path.join(path_addon,'slahmr','slahmr','confs','data','video.yaml'), "wt") as fout:
                for line in fin:
                    if '###FPS###' in line:
                        fout.write(line.replace('###FPS###', fps_video))
                    elif '###INI_FRAME###' in line:
                        fout.write(line.replace('###INI_FRAME###', start_video))
                    elif '###END_FRAME###' in line:
                        fout.write(line.replace('###END_FRAME###', length_video))
                    else:
                        fout.write(line)

        fourd_prop.int_fps_slahmr = int(fps_video)
        fourd_prop.int_ini_frame_slahmr = int(start_video)
        fourd_prop.int_end_frame_slahmr = int(length_video)
        
        context.scene.frame_start = int(start_video)
        context.scene.frame_end = int(length_video)


        return{'FINISHED'}
    
class Update_SLAHMR_Setting(Operator):
    bl_idname = "fdh.update_slahmr_setting"
    bl_label = "Update"
    bl_description = "Update SLAHMR Settings"

    def execute(self,context):
        path_addon = os.path.dirname(os.path.abspath(__file__))
        fourd_prop = context.scene.fourd_prop
        
        fps_video = str(fourd_prop.int_fps_slahmr)

        start_video = str(fourd_prop.int_ini_frame_slahmr)
        length_video = str(fourd_prop.int_end_frame_slahmr)


        with open(os.path.join(path_addon,'slahmr','slahmr','confs','data','video_ref.yaml'), "rt") as fin:
            with open(os.path.join(path_addon,'slahmr','slahmr','confs','data','video.yaml'), "wt") as fout:
                for line in fin:
                    if '###FPS###' in line:
                        fout.write(line.replace('###FPS###', fps_video))
                    elif '###INI_FRAME###' in line:
                        fout.write(line.replace('###INI_FRAME###', start_video))
                    elif '###END_FRAME###' in line:
                        fout.write(line.replace('###END_FRAME###', length_video))
                    else:
                        fout.write(line)

        context.scene.frame_start = int(start_video)
        context.scene.frame_end = int(length_video)

        return{'FINISHED'}


class LoadVideo3dview(Operator):
    bl_idname = "fdh.load_video_3dview"
    bl_label = "Load Video on Screen"
    bl_description = "Load Video on Screen"

    def execute(self,context):
        path_addon = os.path.dirname(os.path.abspath(__file__))
        fourd_prop = context.scene.fourd_prop
        from mathutils import Vector


        vid_path = fourd_prop.str_videopath
        vid_name = os.path.basename(vid_path)
        vid_dir = os.path.dirname(vid_path)

        import addon_utils
        if not addon_utils.check('io_import_images_as_planes')[1]:
            addon_utils.enable('io_import_images_as_planes')

        bpy.ops.import_image.to_plane(files=[{"name":vid_name, "name":vid_name}], directory=vid_dir, relative=False)

        context.selected_objects[0].location = Vector((0,0,0))
        context.selected_objects[0].rotation_euler[2] = 0

        context.selected_objects[0].scale[1] = 3
        context.selected_objects[0].scale[2] = 3
        context.selected_objects[0].scale[0] = 3

        




        ##### mudar a cor para Texture
        win = bpy.context.window
        scr = win.screen
        areas3d  = [area for area in scr.areas if area.type == 'VIEW_3D']
        area = areas3d[0]
        space = area.spaces[0]
        regions   = [region for region in areas3d[0].regions if region.type == 'WINDOW']

        shading = space.shading
        if shading.color_type != 'TEXTURE':
            shading.color_type='TEXTURE'

        return{'FINISHED'}



class Execute(Operator):
    bl_idname = "fdh.execute"
    bl_label = "Execute 4D Human"
    bl_description = "Execute 4D Human"

    option: IntProperty(name='type of mask',default=0)#0=vitdet more vram 14.5gb, 1=maskrcnn less vram about 8.5gb

    def execute(self,context):
        path_addon = os.path.dirname(os.path.abspath(__file__))
        fourd_prop = context.scene.fourd_prop
        path_venv = fourd_prop.str_venv_path
        path_venv_full = join(path_venv,fourd_prop.str_custom_venv_name)
        batch_file = 'execute_4dhumans.bat'


        output_folder = join(path_addon,'4D-Humans-main','outputs')
        if os.path.exists(output_folder):
            shutil.rmtree(output_folder)
            os.makedirs(output_folder, exist_ok=True)
        else:
            os.makedirs(output_folder, exist_ok=True)

        if self.option == 0:
            with open(join(path_addon,batch_file), "wt") as fout:
                fout.write('call \"'+join(path_venv_full,'Scripts','activate.bat')+'\"')
                fout.write('\ncd 4D-Humans-main')
                # fout.write('\nset CUDA_DEVICE_ORDER=PCI_BUS_ID')
                # fout.write('\nset CUDA_VISIBLE_DEVICE='+str(fourd_prop.int_gpu))
                fout.write('\npython track.py video.source="example_data/videos/video.mp4"')
                # fout.write('\ncd ..')
                # fout.write('\npython convert_joblib_pkl.py')

        if self.option ==1:
            with open(join(path_addon,batch_file), "wt") as fout:
                fout.write('call \"'+join(path_venv_full,'Scripts','activate.bat')+'\"')
                fout.write('\ncd 4D-Humans-main')
                # fout.write('\nset CUDA_DEVICE_ORDER=PCI_BUS_ID')
                # fout.write('\nset CUDA_VISIBLE_DEVICE='+str(fourd_prop.int_gpu))
                fout.write('\npython track_maskrcnn.py video.source="example_data/videos/video.mp4"')
                fout.write('\ncd ..')
                fout.write('\npython convert_joblib_pkl.py')

        path_folder = join(path_addon)
        current_folder = os.getcwd()
        os.chdir(path_folder)

        run = [join(path_addon,batch_file)]

        
        print('run: ',run)
        subprocess.run(run) #Executa 
        os.chdir(current_folder)

        base_file = os.path.join(path_addon,'4D-Humans-main','outputs','results')
        file_converted = os.path.join(base_file,'demo_video_converted.pkl')
        file = file_converted
        if os.path.exists(file):
            read_pkl_data(context,0) #0=4d humans, 1=wham
        else:
            self.report({"ERROR"}, "Error, please check the console.")

        fourd_prop.str_pklpath = ''

        # output_folder_origem = join(path_addon,'4D-Humans-main','results','pixelart_vgg19','test_160','images')
        # copy(output_folder_origem,output_folder)
        # shutil.rmtree(join(path_addon,'4D-Humans-main','results','pixelart_vgg19'))
        return{'FINISHED'}



class ExecuteWHAM(Operator):
    bl_idname = "fdh.execute_wham"
    bl_label = "Execute WHAM"
    bl_description = "Execute WHAM"

    # option: IntProperty(name='type of mask',default=0)#0=vitdet more vram 14.5gb, 1=maskrcnn less vram about 8.5gb

    def execute(self,context):
        path_addon = os.path.dirname(os.path.abspath(__file__))
        fourd_prop = context.scene.fourd_prop
        path_venv = fourd_prop.str_venv_path
        path_venv_full = join(path_venv,fourd_prop.str_custom_venv_name_wham)
        batch_file = 'execute_wham.bat'


        output_folder = join(path_addon,'wham','output')
        if os.path.exists(output_folder):
            shutil.rmtree(output_folder)
            os.makedirs(output_folder, exist_ok=True)
        else:
            os.makedirs(output_folder, exist_ok=True)



        
        with open(join(path_addon,batch_file), "wt") as fout:
            fout.write('call \"'+join(path_venv_full,'Scripts','activate.bat')+'\"')
            fout.write('\ncd wham')
            # fout.write('\nset CUDA_DEVICE_ORDER=PCI_BUS_ID')
            # fout.write('\nset CUDA_VISIBLE_DEVICE='+str(fourd_prop.int_gpu))
            if fourd_prop.bool_wham_simplify:
                fout.write('\npython demo.py --video example_data/video.mp4 --save_pkl --run_smplify')
            else:
                fout.write('\npython demo.py --video example_data/video.mp4 --save_pkl')
            # fout.write('\ncd ..')
            # fout.write('\npython convert_joblib_pkl.py')


        path_folder = join(path_addon)
        current_folder = os.getcwd()
        os.chdir(path_folder)

        run = [join(path_addon,batch_file)]

        
        print('run: ',run)
        subprocess.run(run) #Executa 
        os.chdir(current_folder)

        #pegando a quantidade de characters
        # import pickle
        # base_file = os.path.join(path_addon,'4D-Humans-main','outputs','results')
        # file_converted = os.path.join(base_file,'demo_video_converted.pkl')
        # file = file_converted
        # with open(file, 'rb') as handle:
        #     b = pickle.load(handle)
            
        # num_character = 0
        # for fframe, data in enumerate(b.items()):
        #     len_char = len(data[1]['smpl'])
        #     print('len_char: ',len_char)
        #     if num_character < len_char:
        #         num_character = len_char
        #         print('num_char:',num_character)
        # fourd_prop.int_tot_character = num_character

        read_pkl_data(context,1)#0 para 4d humans, 1 para WHAM

        return{'FINISHED'}


class ExecuteSLAHMR(Operator):
    bl_idname = "fdh.execute_slahmr"
    bl_label = "Execute SLAHMR"
    bl_description = "Execute SLAHMR"

    # option: IntProperty(name='type of mask',default=0)#0=vitdet more vram 14.5gb, 1=maskrcnn less vram about 8.5gb

    def execute(self,context):
        path_addon = os.path.dirname(os.path.abspath(__file__))
        fourd_prop = context.scene.fourd_prop
        path_venv = fourd_prop.str_venv_path
        path_venv_full = join(path_venv,fourd_prop.str_custom_venv_name_slahmr)
        batch_file = 'execute_slahmr.bat'


        # output_folder = join(path_addon,'wham','output')
        # if os.path.exists(output_folder):
        #     shutil.rmtree(output_folder)
        #     os.makedirs(output_folder, exist_ok=True)
        # else:
        #     os.makedirs(output_folder, exist_ok=True)

        
        with open(join(path_addon,batch_file), "wt") as fout:
            fout.write('call \"'+join(path_venv_full,'Scripts','activate.bat')+'\"')
            fout.write('\ncd slahmr')
            fout.write('\ncd slahmr')
            # fout.write('\nset CUDA_DEVICE_ORDER=PCI_BUS_ID')
            # fout.write('\nset CUDA_VISIBLE_DEVICE='+str(fourd_prop.int_gpu))
            fout.write('\npython run_opt.py data=video run_opt=True run_vis=False')
            # fout.write('\ncd ..')
            # fout.write('\npython convert_joblib_pkl.py')


        path_folder = join(path_addon)
        current_folder = os.getcwd()
        os.chdir(path_folder)

        run = [join(path_addon,batch_file)]

        
        print('run: ',run)
        subprocess.run(run) #Executa 
        os.chdir(current_folder)

        # read_pkl_data(context,1)#0 para 4d humans, 1 para WHAM

        return{'FINISHED'}



class OpenOutputFolder(Operator):
    bl_idname = "fdh.open_output_folder"
    bl_label = "Open Output Folder"
    bl_description = "Open Output Folder"

    def execute(self,context):
        fourd_prop = context.scene.fourd_prop
        
        path_addon = os.path.dirname(os.path.abspath(__file__))

        
        # output_folder = join(path_addon,'4D-Humans-main','results','pixelart_vgg19')
        output_folder = join(path_addon,'4D-Humans-main','outputs')


        os.system('explorer "'+output_folder+'"')
        return{'FINISHED'}
    

class ImportCharacter(Operator):
    bl_idname = "fdh.import_character"
    bl_label = "Import character"
    bl_description = "Import character"

    option: IntProperty(name='Option',default=0) #0='demo_video_converted.pkl' 1='demo_video_converted_smooth', 2=import wham pickle, 3=import slahmr

    def execute(self,context):

        # from bpy import context

        import os
        # import sys
        # from os.path import join
        import math
        import numpy as np
        from mathutils import Matrix, Vector, Quaternion, Euler
        import json
        import pickle

        path_addon = os.path.dirname(os.path.abspath(__file__))
        fourd_prop = context.scene.fourd_prop
        
        
        # path_code = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        path_code = path_addon

        # file = os.path.join(base_file,'demo_video.pkl')
        if self.option == 0:
            base_file = os.path.join(path_addon,'4D-Humans-main','outputs','results')
            file_converted = os.path.join(base_file,'demo_video_converted.pkl')
        if self.option == 1:
            base_file = os.path.join(path_addon,'4D-Humans-main','outputs','results')
            file_converted = os.path.join(base_file,'demo_video_converted_smooth.pkl')
        if self.option == 2:
            base_file = os.path.join(path_addon,'wham','output','demo','video')
            file_converted = os.path.join(base_file,'wham_output.pickle')
        if self.option == 3: #slahmr
            base_files_npz = os.path.join(path_addon,'slahmr','outputs','video_slahmr','motion_chunks','*_world_results.npz')
            list_slahmr_files= glob.glob(base_files_npz)
            file = list_slahmr_files[-1]


        if self.option in [0,1,2]:
            file = file_converted 
            with open(file, 'rb') as handle:
                results = pickle.load(handle)
        if self.option == 3: #slahmr
            results = np.load(file)


        print('path:',path_addon)

        # file = r"D:\AI\0_mocap\4d-humans\4D-Humans-main\outputs\results\demo_takeover_raymind_walk_sit19636-19951.pkl"
        #file = os.path.join(path_code,'demo_gymnasts.pkl')
        #smpl_model = 'SMPL_MALE.fbx'
        smpl_model = 'basicModel_m_lbs_10_207_0_v1.0.2.fbx'

        # #starts at 0
        # if self.option == 2:
        #     character = 0
        # else:
        #     character = fourd_prop.int_character-1
        character = fourd_prop.int_character-1


        part_match_custom_less2 = {'root': 'root', 'bone_00':  'Pelvis', 'bone_01':  'L_Hip', 'bone_02':  'R_Hip', 
                            'bone_03':  'Spine1', 'bone_04':  'L_Knee', 'bone_05':  'R_Knee', 'bone_06':  'Spine2', 
                            'bone_07':  'L_Ankle', 'bone_08':  'R_Ankle', 'bone_09':  'Spine3', 'bone_10':  'L_Foot', 
                            'bone_11':  'R_Foot', 'bone_12':  'Neck', 'bone_13':  'L_Collar', 'bone_14':  'R_Collar', 
                            'bone_15':  'Head', 'bone_16':  'L_Shoulder', 'bone_17':  'R_Shoulder', 'bone_18':  'L_Elbow', 
                            'bone_19':  'R_Elbow', 'bone_20':  'L_Wrist', 'bone_21':  'R_Wrist',
                            'bone_22':  'L_Hand', 'bone_23':  'R_Hand',
                            }
        
        # part_match_custom_less2 = {'root': 'root', 'bone_00':  'Pelvis', 'bone_01':  'L_Hip', 'bone_02':  'R_Hip', 
        #                     'bone_03':  'Spine1', 'bone_04':  'L_Knee', 'bone_05':  'R_Knee', 'bone_06':  'Spine2', 
        #                     'bone_07':  'L_Ankle', 'bone_08':  'R_Ankle', 'bone_09':  'Spine3', 'bone_10':  'L_Foot', 
        #                     'bone_11':  'R_Foot', 'bone_12':  'Neck', 'bone_13':  'L_Collar', 'bone_14':  'R_Collar', 
        #                     'bone_15':  'Head', 'bone_16':  'L_Shoulder', 'bone_17':  'R_Shoulder', 'bone_18':  'L_Elbow', 
        #                     'bone_19':  'R_Elbow', 'bone_20':  'L_Wrist', 'bone_21':  'R_Wrist',
        #                     }
        # gender = 'n'


        # def rodrigues2bshapes(body_pose):
        #     mat_rots = body_pose
        #     bshapes = np.concatenate([(mat_rot - np.eye(3)).ravel()
        #                             for mat_rot in mat_rots[1:]])
        #     return(mat_rots, bshapes)
        
        ### INICIO --- Inseri para utilizar no WHAM
        def Rodrigues(rotvec):
            theta = np.linalg.norm(rotvec)
            r = (rotvec/theta).reshape(3, 1) if theta > 0. else rotvec
            cost = np.cos(theta)
            mat = np.asarray([[0, -r[2], r[1]],
                            [r[2], 0, -r[0]],
                            [-r[1], r[0], 0]],dtype=object) #adicionei "",dtype=object" por que estava dando erro
            return(cost*np.eye(3) + (1-cost)*r.dot(r.T) + np.sin(theta)*mat)
        
        def rodrigues2bshapes(pose):
            # if pose.shape[0]==24:
            #     rod_rots = np.asarray(pose).reshape(24, 3)
            # else:
            #     rod_rots = np.asarray(pose).reshape(87, 3)
            
            # if pose.shape[0] == 72: Esse aqui é o que estava ativo, mas nao faz muito tentido por tuq eo rod_rota iria passar por cima desse IF
            #     rod_rots = pose.reshape(24, 3)
            # else:
            #     rod_rots = pose.reshape(26, 3)
            rod_rots = np.asarray(pose).reshape(int(pose.shape[0]/3), 3)
            mat_rots = [Rodrigues(rod_rot) for rod_rot in rod_rots]
            bshapes = np.concatenate([(mat_rot - np.eye(3)).ravel()
                                    for mat_rot in mat_rots[1:]])
            return(mat_rots, bshapes)
        ### FIM --- Inseri para utilizar no WHAM
        


        ############
        def get_global_pose(global_pose, arm_ob, frame=None):

            arm_ob.pose.bones['m_avg_root'].rotation_quaternion.w = 0.0
            arm_ob.pose.bones['m_avg_root'].rotation_quaternion.x = -1.0


            bone = arm_ob.pose.bones['m_avg_Pelvis']
            # if frame is not None:
            #     bone.keyframe_insert('rotation_quaternion', frame=frame)

            root_orig = arm_ob.pose.bones['m_avg_root'].rotation_quaternion
            mw_orig = arm_ob.matrix_world.to_quaternion()
            pelvis_quat = Matrix(global_pose[0]).to_quaternion()

            bone.rotation_quaternion = pelvis_quat
            bone.keyframe_insert('rotation_quaternion', frame=frame)

            pelvis_applyied = arm_ob.pose.bones['m_avg_Pelvis'].rotation_quaternion
            bpy.context.view_layer.update()

            # rot_world_orig = root_orig @ pelvis_quat @ mw_orig #pegar a rotacao em relacao ao mundo
            rot_world_orig = root_orig @ pelvis_applyied @ mw_orig #pegar a rotacao em relacao ao mundo

            return rot_world_orig


        ###############

        # apply trans pose and shape to character
        # def apply_trans_pose_shape(trans, body_pose, shape, ob, arm_ob, obname, scene, cam_ob, frame=None):
        def apply_trans_pose_shape(trans, body_pose, arm_ob, obname, frame=None):

            # transform pose into rotation matrices (for pose) and pose blendshapes
            if self.option in [2,3]: #para WHAM ou slahmr
                mrots, bsh = rodrigues2bshapes(body_pose)
            else: #para 4d humans
                mrots = body_pose

            part_bones  = part_match_custom_less2

            if self.option == 2: # pro WHAM
                if fourd_prop.bool_world:
                    trans = Vector((trans[0],trans[1]-0.4,trans[2]))
                else:
                    if fourd_prop.bool_fix_z:
                        trans = Vector((trans[0],trans[1]-2.2,0)) # o -2 é para tentar colocar o personagem no chao ao inves de ficar sob o chao
                    else:
                        trans = Vector((trans[0],trans[1]-2.2,trans[2]))
                    
            if self.option in [0,1]: #pro 4d humans
                if fourd_prop.bool_fix_z:
                    trans = Vector((trans[0],trans[1]-2.2,0)) # o -2 é para tentar colocar o personagem no chao ao inves de ficar sob o chao
                else:
                    trans = Vector((trans[0],trans[1]-2.2,trans[2]))
            
            if self.option == 3: # pro SLAHMR
                trans = Vector((trans[0],trans[1]-2.2,trans[2]))


            # print('frame in apply pose:', frame)
            arm_ob.pose.bones['m_avg_Pelvis'].location = trans
            arm_ob.pose.bones['m_avg_Pelvis'].keyframe_insert('location', frame=frame)
            
            
            arm_ob.pose.bones['m_avg_root'].rotation_quaternion.w = 0.0
            arm_ob.pose.bones['m_avg_root'].rotation_quaternion.x = -1.0
            

            if self.option == 2: #rotaciona para WHAM
                # if fourd_prop.bool_pose_world:
                if fourd_prop.bool_world:
                    arm_ob.pose.bones['m_avg_root'].rotation_quaternion = Vector(( 1.0, 0.0, 0.0, 0.0))
                    arm_ob.pose.bones['m_avg_root'].keyframe_insert('rotation_quaternion', frame=frame)

            
            for ibone, mrot in enumerate(mrots):
                # if ibone < 22: #incui essa parte por que no modelo que eu to usando nao tem bone para a mao
                
                if fourd_prop.bool_use_selected_character:
                    bone = arm_ob.pose.bones['m_avg_'+part_bones['bone_%02d' % ibone]]
                else:
                    bone = arm_ob.pose.bones[obname+'_'+part_bones['bone_%02d' % ibone]]

                bone.rotation_quaternion = Matrix(mrot).to_quaternion()
                
                if frame is not None:
                    bone.keyframe_insert('rotation_quaternion', frame=frame)


        import os
        def init_scene(scene, params, gender='male', angle=0):

            path_addon = os.path.dirname(os.path.abspath(__file__))
            print('path:',path_addon)

            if fourd_prop.bool_use_selected_character:
                # rig = bpy.data.objects['rig']
                # rig = bpy.context.selected_objects[0]
                rig = context.scene.source
                for obj in bpy.data.objects:
                    if obj.parent == rig:
                        obname = obj.name
                        pass
                
                ob = bpy.data.objects[obname]
                arm_obj = rig.name

            else:
                # # fazendo import do FBX
                path_fbx = os.path.join(path_code,smpl_model)
                bpy.ops.import_scene.fbx(filepath=path_fbx, axis_forward='-Y', axis_up='-Z', global_scale=100)#, automatic_bone_orientation=True)
                arm_obj = context.selected_objects[0]
                ###################################

                # # fazendo append arquivo blend character
                # blend_file = os.path.join(path_addon, 'human_base_meshe_male_8.blend')
                # section = "Object"
                # directory = os.path.join(blend_file, section)
                # nome_obj = 'm_avg'
                # file_path = os.path.join(blend_file,section,nome_obj)
                # bpy.ops.wm.append(filepath=file_path,filename=nome_obj, directory=directory)
                # arm_obj = context.selected_objects[0].parent
                # ####################

                obj_gender = 'm'
                obname = '%s_avg' % obj_gender
                ob = bpy.data.objects[obname]
                # arm_obj = 'Armature'
                context.scene.source = arm_obj

            print('success load')
            
            # ob.data.use_auto_smooth = False  # autosmooth creates artifacts
            bpy.ops.object.select_all(action='DESELECT')
            bpy.ops.object.select_all(action='DESELECT')
            cam_ob = ''
            # ob.data.shape_keys.animation_data_clear()
            # arm_ob = bpy.data.objects[arm_obj]
            arm_ob = context.scene.source
            arm_ob.animation_data_clear()
            
            return(ob, obname, arm_ob, cam_ob)





        ## Inicio da parte que roda
        # import joblib


        # results = joblib.load(file)
        params = []
        object_name = 'm_avg'
        obj_gender = 'm'
        scene = bpy.data.scenes['Scene']
        ob, obname, arm_ob, cam_ob= init_scene(scene, params, obj_gender)

        if fourd_prop.bool_use_selected_character:
            obj = bpy.context.window.scene.objects[obname]
        else:
            obj = bpy.context.window.scene.objects[object_name]
        bpy.context.view_layer.objects.active = ob

        # obs = []
        # for ob in bpy.context.scene.objects:
        #     if ob.type == 'ARMATURE':
        #         obs.append(ob)
        # # armature = obs[len(obs)-1].name

        # obs[len(obs)-1].select_set(True)

        # ob.select_set(True)
        arm_ob.select_set(True)
        view_layer = bpy.context.view_layer
        # Armature_obj = obs[len(obs)-1]
        view_layer.objects.active = arm_ob

        fixed_pelvis_quat = []

        # for fframe, data in enumerate(results.items()):
        # print('characters_index max:',len(data[1]['smpl'])-1)
        if self.option == 2: # para importar o WHAM
            list_characters = json.loads(fourd_prop.str_list_characters)


            # qtd_frames = len(results[character]['pose'])
            qtd_frames = len(results[int(list_characters[character])]['pose'])
            # fourd_prop.int_tot_character = len(results)
            fourd_prop.int_tot_character = len(list_characters)
            print('qtd frames: ',qtd_frames)
            # frames_ids = results[character]['frame_ids']
            frames_ids = results[int(list_characters[character])]['frame_ids']
            
            # shape = results[character]['betas'].tolist()
            # for fframe in range(0,qtd_frames-1):
            # if fourd_prop.bool_trans_world:
            #     bool_trans = 'trans_world'
            # else: 
            #     bool_trans = 'trans'

            # if  fourd_prop.bool_pose_world:
            #     bool_pose = 'pose_world'
            # else:
            #     bool_pose = 'pose'

            if fourd_prop.bool_world:
                bool_pose = '_world'
            else:
                bool_pose = ''

            for fframe in range(0,len(frames_ids)):
                if character <= len(results)-1:
                    real_frame = frames_ids[0] + fframe #corrigindo o frame real para poder aparecer corretamento no timeline
                    # print('fframe: ',fframe)
                    # scene.frame_set(real_frame)
                    # trans = results[character]['trans_world'][fframe]
                    # trans = results[int(list_characters[character])][bool_trans][fframe]
                    trans = results[int(list_characters[character])]['trans'+bool_pose][fframe]
                    # shape = data[1]['smpl'][character]['betas']

                    # final_body_pose = results[character]['pose_world'][fframe]
                    # final_body_pose = results[int(list_characters[character])][bool_pose][fframe]
                    final_body_pose = results[int(list_characters[character])]['pose'+bool_pose][fframe]
                    apply_trans_pose_shape(Vector(trans), final_body_pose, arm_ob, obname, real_frame)
                    bpy.context.view_layer.update()
                else:
                    print('skipping to the next')
        # else: # o de baixo é para o 4d humans
        if self.option in [0,1]: #4d humans com e sem smoothnet
            # qtd_frames = len(results[character]['pose'])
            qtd_frames = len(results)
            fourd_prop.int_tot_character = qtd_frames
            print('qtd frames: ',qtd_frames)
            # shape = results[character]['betas'].tolist()
            for fframe, data in enumerate(results.items()):
                if character <= len(data[1]['smpl'])-1:
                    scene.frame_set(fframe)
                    # trans = [0.0, 0.0, 1.521]
                    trans = data[1]['camera'][character]
                    # shape = data[1]['smpl'][character]['betas']

                    global_orient = data[1]['smpl'][character]['global_orient']
                    # pelvis = fixed_pelvis_quat[fframe]
                    # global_orient = np.array(Quaternion(pelvis).to_matrix()).reshape(1,3,3)


                    ##o trtamento abaixo nao deu certo
                    # rotation_x = Matrix.Rotation(math.radians(180.0),3,'X') #rodar ao redor de X
                    # rotation_y = Matrix.Rotation(math.radians(90.0),3,'Y') #rodar ao redor de X
                    # global_orient = global_orient @ rotation_x @rotation_y

                    body_pose = data[1]['smpl'][character]['body_pose']
                    final_body_pose = np.vstack([global_orient, body_pose])
                    # apply_trans_pose_shape(Vector(trans), final_body_pose, shape, obj,arm_ob, obname, scene, cam_ob, fframe)
                    
                    
                    apply_trans_pose_shape(Vector(trans), final_body_pose, arm_ob, obname, fframe)
                    bpy.context.view_layer.update()
                else:
                    print('skipping to the next')

        if self.option == 3: #SLAHMR
            # qtd_frames = len(results[character]['pose'])
            qtd_frames = len(results['root_orient'][character])
            fourd_prop.int_tot_character = qtd_frames
            print('qtd frames: ',qtd_frames)
            # shape = results[character]['betas'].tolist()
            for fframe in range(0,qtd_frames-1):
                if character <= len(results['trans'])-1:
                    scene.frame_set(fframe)
                    # trans = [0.0, 0.0, 1.521]
                    trans = results['trans'][character][fframe].tolist()
                    # shape = data[1]['smpl'][character]['betas']

                    global_orient = results['root_orient'][character][fframe]
                    body_pose = results['pose_body'][character][fframe]
                    final_body_pose = np.hstack([global_orient, body_pose])
                    # apply_trans_pose_shape(Vector(trans), final_body_pose, shape, obj,arm_ob, obname, scene, cam_ob, fframe)
                    
                    
                    apply_trans_pose_shape(Vector(trans), final_body_pose, arm_ob, obname, fframe)
                    bpy.context.view_layer.update()
                else:
                    print('skipping to the next')
            

        print('antes_arm_ob: ',arm_ob.name)
        print('antes_obj: ',obj.name)
        if not fourd_prop.bool_use_selected_character:
            # arm_ob.name = 'Finalized_Armature_CH'+str(fourd_prop.int_character).zfill(2)
            if self.option == 2: # para importar o WHAM
                # if fourd_prop.bool_trans_world:
                #     ttext_amt = 'WT'
                # else:
                #     ttext_amt = 'LT'
                
                # if fourd_prop.bool_pose_world:
                #     ptext_amt = 'WP'
                # else:
                #     ptext_amt = 'LP'
                # ftext = ttext_amt+'_'+ptext_amt

                if fourd_prop.bool_world:
                    txt_amt = 'W'
                else:
                    txt_amt = 'L'

                # arm_ob.name = ftext+'_Amt_C'+str(fourd_prop.int_character).zfill(2)
                arm_ob.name = txt_amt+'_Amt_C'+str(fourd_prop.int_character).zfill(2)
            else:
                arm_ob.name = 'Amt_C'+str(fourd_prop.int_character).zfill(2)
            # obj.name='Finalized_Mesh'
            obj.name='Amt_Mesh'
        print('Depois_arm_ob: ',arm_ob.name)
        print('Depois_obj: ',obj.name)

        if self.option == 2: # para importar o WHAM
            bpy.context.scene.frame_end = real_frame
        else:
            bpy.context.scene.frame_end = fframe

        # Alterando propriedades para o valor FPS que esta no painel
        context.scene.render.fps = int(fourd_prop.enum_fps)

        #Criando copia para usar de referencia, a fazer bake para poder colocar na orientacao correta
        
        bpy.ops.object.duplicate(linked=False)
        armature_ref = bpy.context.selected_objects[0]
        armature_ref.name = 'TEMP_Armature_CH'+str(fourd_prop.int_character).zfill(2)


        #colocando o bone root na forma correta 
        
        
        arm_ob.pose.bones['m_avg_root'].rotation_quaternion.w = 1.0
        arm_ob.pose.bones['m_avg_root'].rotation_quaternion.x = 0.0
        arm_ob.pose.bones['m_avg_root'].rotation_quaternion.y = 0.0
        arm_ob.pose.bones['m_avg_root'].rotation_quaternion.z = 0.0


        arm_ob.pose.bones['m_avg_Pelvis'].constraints.new('COPY_LOCATION')
        # arm_ob.pose.bones["m_avg_Pelvis"].constraints["Copy Location"].target = armature_ref
        arm_ob.pose.bones["m_avg_Pelvis"].constraints[0].target = armature_ref
        arm_ob.pose.bones["m_avg_Pelvis"].constraints[0].subtarget = "m_avg_Pelvis"
        # arm_ob.pose.bones["m_avg_Pelvis"].constraints["Copy Location"].subtarget = "m_avg_Pelvis"

        
        arm_ob.pose.bones['m_avg_Pelvis'].constraints.new('COPY_ROTATION')
        # arm_ob.pose.bones["m_avg_Pelvis"].constraints["Copy Rotation"].target = armature_ref
        arm_ob.pose.bones["m_avg_Pelvis"].constraints[1].target = armature_ref
        # arm_ob.pose.bones["m_avg_Pelvis"].constraints["Copy Rotation"].subtarget = "m_avg_Pelvis"
        arm_ob.pose.bones["m_avg_Pelvis"].constraints[1].subtarget = "m_avg_Pelvis"



        #bake
        # if bpy.context.active_object.mode != 'POSE':
        #     bpy.ops.object.mode_set(mode='POSE')
        # bpy.ops.pose.select_all(action='DESELECT') #clear

        # arm_ob.pose.bones['m_avg_Pelvis'].bone.select = True


        bpy.ops.object.select_all(action='DESELECT')
        arm_ob.select_set(True)



        # start_frame = context.scene.frame_start
        if self.option == 2: # para importar o WHAM
            start_frame = frames_ids[0]
            end_frame = frames_ids[-1]
        else:
            start_frame = 0
            end_frame = context.scene.frame_end
        bpy.ops.nla.bake(frame_start=start_frame, frame_end=end_frame, 
                            only_selected=False, visual_keying=True, clear_constraints=True, 
                            clear_parents=False, use_current_action=True, clean_curves=False, bake_types={'POSE'})

        # bpy.ops.object.mode_set(mode='OBJECT')

        bpy.ops.object.select_all(action='DESELECT')
        armature_ref.select_set(True)
        #remove a acao, que vai estar de cabexa pra baixo
        bpy.data.actions.remove(armature_ref.animation_data.action)
        bpy.ops.object.delete()

        
        arm_ob.select_set(True)
        bpy.context.view_layer.objects.active = arm_ob

        #seta o correto index que vai aparecer na listagem
        print('action: ', arm_ob.animation_data.action.name)
        #procurando index da acao criada
        act_idx = 0
        for i,ac in enumerate(bpy.data.actions):
            if ac.name == arm_ob.animation_data.action.name:
                act_idx = i
        
        context.scene.active_action_index = act_idx

        #colocando nome da acao na caixa de edicao
        fourd_prop.str_nla_name = arm_ob.animation_data.action.name

        # context.scene.source = arm_ob



        return{'FINISHED'}
    

class ImportFBX(Operator, ImportHelper):
    bl_idname = "fdh.import_smpl_fbx"
    bl_label = "Import SMPL FBX"
    bl_description = "Import SMPL FBX"

    # filename_ext = ".ckpt"
    filter_glob: StringProperty(
        # default= ["*.jpg","*.png"],
        default= "*.fbx",
        # default= "*",
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )

    # files: CollectionProperty(name='File paths', type=bpy.types.OperatorFileListElement)
    # directory: StringProperty(subtype='DIR_PATH')

    def execute(self,context):

        # fourd_prop = context.scene.fourd_prop
        # fourd_prop.str_videopath = self.filepath
        from shutil import copyfile
        # # dfnrmvs_prop = context.scene.dfnrmvs_prop
        path_addon = os.path.dirname(os.path.abspath(__file__))
        
        # base_path_img = os.path.join(path_addon,'4D-Humans-main','datasets','TEST_DATA')
        # path_file = os.path.join(path_addon,'4D-Humans-main','example_data','videos')

        src = self.filepath
        dst = os.path.join(path_addon,os.path.basename(src))

        copyfile(src,dst)


        return{'FINISHED'}
    

class Smooth(Operator):
    bl_idname = "fdh.smooth"
    bl_label = "Smooth Animation"
    bl_description = "Smooth Animation"

    pkl_file: StringProperty(name='pkl_file',default='demo_video_converted.pkl') # em geral 'demo_video_converted.pkl' 1='demo_video_converted_smooth.pkl'
    smooth_what: StringProperty(name='smooth_what', default='both')# trans,pose,both


    def execute(self,context):

        path_addon = os.path.dirname(os.path.abspath(__file__))
        fourd_prop = context.scene.fourd_prop
        path_venv = fourd_prop.str_venv_path
        path_venv_full = join(path_venv,fourd_prop.str_custom_venv_name)
        batch_file = 'smooth.bat'

        # path_image = join(path_addon,'image_process.data')
        # path_ckpt = join(path_addon,'checkpoint')
        with open(join(path_addon,batch_file), "wt") as fout:
            fout.write('call \"'+join(path_venv_full,'Scripts','activate.bat')+'\"')
            # fout.write('\npython sdm_unips/main.py --session_name results --target '+fourd_prop.enum_target+' --test_dir "'+path_addon+'" --checkpoint "'+path_ckpt+'" %*')
            # fout.write('\ncd 4D-Humans-main')
            fout.write('\npython smooth.py --tot_characters '+str(fourd_prop.int_tot_character)+' --pkl_file_input '+self.pkl_file+' --smooth_what '+self.smooth_what)
            

        path_folder = join(path_addon)
        current_folder = os.getcwd()
        os.chdir(path_folder)

        run = [join(path_addon,batch_file)]

        
        print('run: ',run)
        subprocess.run(run) #Executa 
        os.chdir(current_folder)
        return{'FINISHED'}


class ExportRAWAnimation(bpy.types.Operator, ExportHelper):
    bl_idname = "fdh.export_animation"
    bl_label = "Export Raw Animation"

    filename_ext = ".pkl"  # ExportHelper mixin class uses this
    option: IntProperty(name='Export PKL',default=0) #0 = CEB 4d Humans PKL  | 1 = WHAM 

    def invoke(self, context, _event):
        fourd_prop = context.scene.fourd_prop
        if fourd_prop.str_videopath != '':
            filename_full = os.path.basename(fourd_prop.str_videopath)
            filename = os.path.splitext(filename_full)[0]
        else:
            if self.option == 0:
                filename = 'ceb_4d_humans_raw_anim'
            if self.option == 1:
                filename = 'WHAM_raw_anim'


        # if not self.filepath:
        #     # blend_filepath = context.blend_data.filepath
        #     blend_filepath = filename # <=== UPDATE
        #     if not blend_filepath:
        #         blend_filepath = filename # <=== UPDATE
        #     else:
        #         blend_filepath = os.path.splitext(blend_filepath)[0]
        #     self.filepath = blend_filepath + self.filename_ext
        ### adapatacao prara quando tiver cometnado acima
        
        blend_filepath = filename
        self.filepath = blend_filepath + self.filename_ext
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}
    
    def execute(self, context):
        filepath = self.filepath

        path_addon = os.path.dirname(os.path.abspath(__file__))
        if self.option == 0:
            base_file = os.path.join(path_addon,'4D-Humans-main','outputs','results')
            file_converted = os.path.join(base_file,'demo_video_converted.pkl')
        if self.option == 1:
            base_file = os.path.join(path_addon,'WHAM','output','demo','video')
            file_converted = os.path.join(base_file,'wham_output.pickle')

        shutil.copy(file_converted,filepath)
        return{'FINISHED'}


#usar o export abaixo para gerar um zip dos arquivos
class ExportSLAHMRRAWAnimation(bpy.types.Operator, ExportHelper): 
    bl_idname = "fdh.export_animation_slahmr"
    bl_label = "Export"

    filename_ext = ""  # ExportHelper mixin class uses this
    option: IntProperty(name='Export PKL',default=0) #0 = SLAHMR

    def invoke(self, context, _event):
        fourd_prop = context.scene.fourd_prop
        if fourd_prop.str_videopath != '':
            filename_full = os.path.basename(fourd_prop.str_videopath)
            filename = os.path.splitext(filename_full)[0]
        else:
            if self.option == 0:
                filename = 'SLAHMR_raw_anim'
            
        
        blend_filepath = filename
        self.filepath = blend_filepath + self.filename_ext
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}
    
    def execute(self, context):
        filepath = self.filepath

        path_addon = os.path.dirname(os.path.abspath(__file__))
        if self.option == 0:
            source_folder = os.path.join(path_addon,'slahmr','outputs','video_slahmr')
            output_path  = filepath
            shutil.make_archive(output_path, 'zip', source_folder)
        

        # shutil.copy(file_converted,filepath)
        return{'FINISHED'}



class ReadPKLData(Operator):
    bl_idname = "fdh.read_pkl_data"
    bl_label = "Read PKL Data"
    bl_description = "Read PKL Data"

    option: IntProperty(name='Chosse 4d humans / WHAM',default=0) #0 = CEB 4d Humans PKL (Pickle) | 1 = 4d Humans PKL (joblib)

    def execute(self,context):
        # path_addon = os.path.dirname(os.path.abspath(__file__))
        # fourd_prop = context.scene.fourd_prop
        # #pegando a quantidade de characters
        # import pickle
        # base_file = os.path.join(path_addon,'4D-Humans-main','outputs','results')
        # file_converted = os.path.join(base_file,'demo_video_converted.pkl')
        # file = file_converted
        # with open(file, 'rb') as handle:
        #     b = pickle.load(handle)
            
        # num_character = 0
        # for fframe, data in enumerate(b.items()):
        #     len_char = len(data[1]['smpl'])
        #     print('len_char: ',len_char)
        #     if num_character < len_char:
        #         num_character = len_char
        #         print('num_char:',num_character)
        # fourd_prop.int_tot_character = num_character

        read_pkl_data(context,self.option) #0=4d humans, 1=wham

        return{'FINISHED'}
    
class ImportPKLAnimation(Operator, ImportHelper):
    bl_idname = "fdh.import_pkl_animation"
    bl_label = "Import RAW Animation"
    bl_description = "Import PKL RAW Animation"

    option: IntProperty(name='Chosse type PKL',default=0) #0 = CEB 4d Humans PKL (Pickle) | 1 = 4d Humans PKL (joblib - google colab)
    #                                                       2 = WHAM (Pickle) | 3 = Wham Google Colab

    filename_ext = ".pkl"
    filter_glob: StringProperty(
        default="*.pkl",
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )
    def execute(self,context):
        path_addon = os.path.dirname(os.path.abspath(__file__))
        fourd_prop = context.scene.fourd_prop
        
        src = self.filepath
        if self.option in [0,1]:
            base_file = os.path.join(path_addon,'4D-Humans-main','outputs','results')
        if self.option in [2,3]:
            base_file = os.path.join(path_addon,'WHAM','output','demo','video')



        if os.path.exists(base_file):
            shutil.rmtree(base_file)
            os.makedirs(base_file, exist_ok=True)
        else:
            os.makedirs(base_file, exist_ok=True)

        if self.option == 0:
            dst = os.path.join(base_file,'demo_video_converted.pkl')
            shutil.copyfile(src,dst)#copia o arquivo
        if self.option == 1: #
            dst = os.path.join(base_file,'demo_video.pkl')
            path_venv = fourd_prop.str_venv_path
            path_venv_full = join(path_venv,fourd_prop.str_custom_venv_name)
            batch_file = 'convert_4dhumans_pkl.bat'

            with open(join(path_addon,batch_file), "wt") as fout:
                fout.write('call \"'+join(path_venv_full,'Scripts','activate.bat')+'\"')
                fout.write('\npython convert_joblib_pkl.py')

            shutil.copyfile(src,dst)  #copia o arquivo
            path_folder = join(path_addon)
            current_folder = os.getcwd()
            os.chdir(path_folder)

            run = [join(path_addon,batch_file)]
            
            print('run: ',run)
            subprocess.run(run) #Executa 
            os.chdir(current_folder)

        if self.option == 2: #wham import
            dst = os.path.join(base_file,'wham_output.pickle')
            shutil.copyfile(src,dst)#copia o arquivo

        if self.option == 3: # WHAM from google Colab
            dst = os.path.join(base_file,'wham_output_google_colab.pkl')
            path_venv = fourd_prop.str_venv_path
            path_venv_full = join(path_venv,fourd_prop.str_custom_venv_name_wham)
            batch_file = 'convert_WHAM_pkl.bat'

            with open(join(path_addon,batch_file), "wt") as fout:
                fout.write('call \"'+join(path_venv_full,'Scripts','activate.bat')+'\"')
                fout.write('\npython convert_joblib_pkl_wham.py')

            shutil.copyfile(src,dst)  #copia o arquivo
            path_folder = join(path_addon)
            current_folder = os.getcwd()
            os.chdir(path_folder)

            run = [join(path_addon,batch_file)]
            
            print('run: ',run)
            subprocess.run(run) #Executa 
            os.chdir(current_folder)

        


        fourd_prop.str_pklpath =src 
        fourd_prop.str_videopath=''


        if self.option in [0,1]:
            read_pkl_data(context,0)#0=4d humans, 1=wham
        if self.option in [2,3]:
            read_pkl_data(context,1)#0=4d humans, 1=wham


        return{'FINISHED'}
    
class ImportZIPAnimation(Operator, ImportHelper):
    bl_idname = "fdh.import_zip_animation"
    bl_label = "Import"
    bl_description = "Import ZIP RAW Animation"

    option: IntProperty(name='Chosse',default=0) #0 = SLAHMR

    filename_ext = ".zip"
    filter_glob: StringProperty(
        default="*.zip",
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )
    def execute(self,context):
        path_addon = os.path.dirname(os.path.abspath(__file__))
        fourd_prop = context.scene.fourd_prop
        
        src = self.filepath
        if self.option == 0: #SLAHMR
            dst_folder = os.path.join(path_addon,'slahmr','outputs','video_slahmr')

        if os.path.exists(dst_folder):
            shutil.rmtree(dst_folder)
            os.makedirs(dst_folder, exist_ok=True)
        else:
            os.makedirs(dst_folder, exist_ok=True)

        if self.option == 0:
            shutil.unpack_archive(src, dst_folder, 'zip') 
            

        # fourd_prop.str_pklpath =src 
        fourd_prop.str_videopath=''


        # read_pkl_data(context,1)


        return{'FINISHED'}


class ImportZIPSLAHMRDependencies(Operator, ImportHelper):
    bl_idname = "fdh.import_zip_slahmr_dependencies"
    bl_label = "Import SLAHMR Deps"
    bl_description = "Import ZIP SLAHMR Dependencies"

    option: IntProperty(name='Chosse',default=0) #0 = SLAHMR

    filename_ext = ".zip"
    filter_glob: StringProperty(
        default="*.zip",
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )
    def execute(self,context):
        path_addon = os.path.dirname(os.path.abspath(__file__))
        # fourd_prop = context.scene.fourd_prop
        
        src = self.filepath
        if self.option == 0: #SLAHMR
            dst_folder = os.path.join(path_addon,'slahmr')
            dst_data_folder = os.path.join(path_addon,'slahmr','_DATA')

        if os.path.exists(dst_data_folder):
            shutil.rmtree(dst_data_folder)
            # os.makedirs(dst_data_folder, exist_ok=True)
        # else:
        #     os.makedirs(dst_data_folder, exist_ok=True)

        if self.option == 0:
            print("...Start SLAHMR Dependencies Unzipping...")
            shutil.unpack_archive(src, dst_folder, 'zip') 
            print("...Finished SLAHMR Dependencies Unzipping...")
            

        return{'FINISHED'}

class SetIniFPS(Operator):
    bl_idname = "fdh.set_ini_fps"
    bl_label = "Set FPS"
    bl_description = "Set FPS"


    def execute(self,context):
        fourd_prop = context.scene.fourd_prop
        fourd_prop.enum_fps="24"
        context.scene.render.fps=24


        return{'FINISHED'}
    


class Smooth2(Operator):
    bl_idname = "fdh.smooth2"
    bl_label = "Smooth2"
    bl_description = "Smooth2"
    bl_options = {"REGISTER", "UNDO"}

    option: IntProperty(name='Type of Smooth',default=0) #0= bake and smooth, 1= only bake,2=only smooth


    def execute(self,context):
        fourd_prop = context.scene.fourd_prop

        # types = {'VIEW_3D', 'TIMELINE', 'GRAPH_EDITOR', 'DOPESHEET_EDITOR', 'NLA_EDITOR', 'IMAGE_EDITOR', 'SEQUENCE_EDITOR', 'CLIP_EDITOR', 'TEXT_EDITOR', 'NODE_EDITOR', 'LOGIC_EDITOR', 'PROPERTIES', 'OUTLINER', 'USER_PREFERENCES', 'INFO', 'FILE_BROWSER', 'CONSOLE'}
        def smooth_curves(o):
            current_area = bpy.context.area.type
            layer = bpy.context.view_layer

            if not fourd_prop.bool_selected_bones:
                # select all (relevant) bones
                for b in o.data.bones:
                    b.select = True
                # o.data.bones[0].select = True
            layer.update()

            # change to graph editor
            bpy.context.area.type = "GRAPH_EDITOR"

            # lock or unlock the respective fcurves
            # for fc in o.animation_data.action.fcurves:
            #     print(fc.data_path)
            #     if "location" in fc.data_path:
            #         fc.lock = False
            #     else:
            #         fc.lock = True

            layer.update()
            # smooth curves of all selected bones
            bpy.ops.graph.smooth()

            # switch back to original area
            bpy.context.area.type = current_area

            # deselect all (relevant) bones
            # for b in o.data.bones:
            #     b.select = False
            # layer.update()


        start_frame = context.scene.frame_start
        end_frame = context.scene.frame_end

        if self.option in  [0,1]:
            bpy.ops.nla.bake(frame_start=start_frame, frame_end=end_frame, 
                            only_selected=fourd_prop.bool_selected_bones, visual_keying=False, clear_constraints=False, 
                            clear_parents=False, use_current_action=True, clean_curves=False, bake_types={'POSE'})
        
        if self.option in [0,2]:
            # currently selected 
            o = bpy.context.object
            smooth_curves(o)
        return{'FINISHED'}


class FootLockMarker(Operator):
    bl_idname = "fdh.foot_lock_marker"
    bl_label = "Foot Lock Marker"
    bl_description = "Foot Lock Marker"
    bl_options = {"REGISTER", "UNDO"}

    option: IntProperty(name='Start/Stop Foot Lock',default=0) #-1=apagra markes; 0=Foot lock start, 1= Foot lock end; 2=set default height


    def execute(self,context):
        # fourd_prop = context.scene.fourd_prop

        cur_frame = context.scene.frame_current
        markers = context.scene.timeline_markers

        if self.option == -1:
            for m in markers:
                markers.remove(m)
        if self.option == 0:
            markers.new('F_start',frame=cur_frame)

        if self.option == 1:
            markers.new('F_end',frame=cur_frame)

        if self.option == 2:
            markers.new('Ini_height',frame=cur_frame)



        return{'FINISHED'}


class FootLock(Operator):
    bl_idname = "fdh.foot_lock"
    bl_label = "Foot Lock"
    bl_description = "Foot Lock"
    bl_options = {"REGISTER", "UNDO"}

    option: IntProperty(name='analyze and execute Foot Lock',default=0) #0=analyze foot lock, 1= place foot locks, 2=original location


    def execute(self,context):
        path_addon = os.path.dirname(os.path.abspath(__file__))
        fourd_prop = context.scene.fourd_prop
        base_file = os.path.join(path_addon,'4D-Humans-main','outputs','results')


        LboneN = 'm_avg_L_Ankle'
        RboneN = 'm_avg_R_Ankle'
        LWristN = 'm_avg_L_Wrist'
        RWristN = 'm_avg_R_Wrist'
        LElbowN = 'm_avg_L_Elbow'
        RElbowN = 'm_avg_R_Elbow'


        scene = context.scene
        

        file_motion = os.path.join(base_file,'root_motion.pkl')

        # armature = bpy.data.objects['Finalized_Armature']
        # armature = context.selected_objects[0]
        armature = context.scene.source
        if self.option == 0:
            marker_ini_height = None
            #pegando o frame que devo usar como ref de altura
            for m in bpy.context.scene.timeline_markers:
                if m.name == 'Ini_height':
                    marker_ini_height=m.frame #espera-se que tnha apenas um ini heigh
                    break
            
            # Pegando a altura de referencia
            if marker_ini_height is not None:
                scene.frame_set(marker_ini_height) #vai para o frame marcado como referencia
            # ref_pelvis_location_y = min(RbonePos[2],LbonePos[2],LWristPos[2],RWristPos[2],LElbowPos[2],RElbowPos[2])

            Lbone = armature.pose.bones[LboneN].head
            Rbone = armature.pose.bones[RboneN].head
            LWrist = armature.pose.bones[LWristN].head
            RWrist = armature.pose.bones[RWristN].head
            LElbow = armature.pose.bones[LElbowN].head
            RElbow = armature.pose.bones[RElbowN].head
            #
            # Since Blender 2.8 you multiply matrices with @ not with *
            LbonePos = armature.matrix_world @ Lbone
            RbonePos = armature.matrix_world @ Rbone
            LWristPos = armature.matrix_world @ LWrist
            RWristPos = armature.matrix_world @ RWrist
            LElbowPos = armature.matrix_world @ LElbow
            RElbowPos = armature.matrix_world @ RElbow
            
            min_height = min(RbonePos[2],LbonePos[2],LWristPos[2],RWristPos[2],LElbowPos[2],RElbowPos[2])
            


            adjust_heigh = []
            for ef, f in enumerate(range(scene.frame_start, scene.frame_end+1)):
                scene.frame_set(f)
                # This can be head, tail, center...
                # More info: https://docs.blender.org/api/current/bpy.types.PoseBone.html?highlight=bpy%20bone#bpy.types.PoseBone.bone
                #bone = armature.pose.bones[boneN].tail
                Lbone = armature.pose.bones[LboneN].head
                Rbone = armature.pose.bones[RboneN].head
                LWrist = armature.pose.bones[LWristN].head
                RWrist = armature.pose.bones[RWristN].head
                LElbow = armature.pose.bones[LElbowN].head
                RElbow = armature.pose.bones[RElbowN].head
                #
                # Since Blender 2.8 you multiply matrices with @ not with *
                LbonePos = armature.matrix_world @ Lbone
                RbonePos = armature.matrix_world @ Rbone
                LWristPos = armature.matrix_world @ LWrist
                RWristPos = armature.matrix_world @ RWrist
                LElbowPos = armature.matrix_world @ LElbow
                RElbowPos = armature.matrix_world @ RElbow
                #print(RbonePos)
                #print(LbonePos)
                #
                # z_change = min(RbonePos[2],LbonePos[2])
                z_change = min(RbonePos[2],LbonePos[2],LWristPos[2],RWristPos[2],LElbowPos[2],RElbowPos[2])
                
                if ef == 0:
                    if marker_ini_height is None:
                        first_heigh = z_change
                    else:
                        # first_heigh = ref_pelvis_location_y
                        first_heigh = min_height
                    dif = z_change
                else:
                    dif = first_heigh - z_change
                pelvis_location_x = armature.pose.bones['m_avg_Pelvis'].location[0]
                pelvis_location_y = armature.pose.bones['m_avg_Pelvis'].location[1]
                adjust_heigh.append([f,pelvis_location_x,pelvis_location_y,z_change,dif,pelvis_location_y+dif])
                #
                #print("Frame " + str(f) + ": pelviz"+str(pelvis_location)+" final: "+str(pelvis_location-dif)+" z_change: "+str(z_change)+" -dif- "+str(dif))
                
            with open(file_motion, 'wb') as handle:
                pickle.dump(adjust_heigh, handle, protocol=pickle.HIGHEST_PROTOCOL)

        if self.option == 1:
            foot_lock =0 #default 0
            with open(file_motion, 'rb') as handle:
                adjust_heigh = pickle.load(handle)
            #
            list_markers_start=[] 
            list_markers_end=[]
            for m in bpy.context.scene.timeline_markers:
                if m.name == 'F_start':
                    list_markers_start.append(m.frame)
                if m.name == 'F_end':
                    list_markers_end.append(m.frame)
            #
            for ef,f in enumerate(range(scene.frame_start, scene.frame_end+1)):
                if f in list_markers_start:
                    foot_lock=1
                if f in list_markers_end:
                    foot_lock=0
                #
                if foot_lock == 1:
                    armature.pose.bones['m_avg_Pelvis'].location[0] = adjust_heigh[ef][1]
                    armature.pose.bones['m_avg_Pelvis'].location[1] = adjust_heigh[ef][5]
                    armature.pose.bones['m_avg_Pelvis'].keyframe_insert('location', frame=f)  

        if self.option == 2:
            with open(file_motion, 'rb') as handle:
                adjust_heigh = pickle.load(handle)
            for ef,f in enumerate(range(scene.frame_start, scene.frame_end+1)):
                armature.pose.bones['m_avg_Pelvis'].location[0] = adjust_heigh[ef][1]
                armature.pose.bones['m_avg_Pelvis'].location[1] = adjust_heigh[ef][2]
                armature.pose.bones['m_avg_Pelvis'].keyframe_insert('location', frame=f)  

        return{'FINISHED'}
    

class ImportOfflineFiles(Operator, ImportHelper):
    bl_idname = "fdh.import_offline_files"
    bl_label = "Import Model Files '4d_humans_optional_offline_model_files.zip'"
    bl_description = "Download first the '4d_humans_optional_offline_model_files.zip' file."

    # option: IntProperty(name='Chosse type PKL',default=0) #0 = CEB 4d Humans PKL (Pickle) | 1 = 4d Humans PKL (joblib)

    filename_ext = ".zip"
    filter_glob: StringProperty(
        default="*.zip",
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )
    def execute(self,context):
        # path_addon = os.path.dirname(os.path.abspath(__file__))
        # fourd_prop = context.scene.fourd_prop
        import shutil
        from os.path import expanduser
        home = expanduser("~") # se nao me engano isso vai jogar pro caminho "usuario" do windows
        
        zip_file = self.filepath
        
        print('...Starting of Unziping 4d Humans Offline Files...')
        shutil.unpack_archive(zip_file, home)
        print('...End of Unzipinf 4d Humans Offline Files...')

        
        return{'FINISHED'}
    
class ImportOfflineCheckpointWham(Operator, ImportHelper):
    bl_idname = "fdh.import_offline_checkpoint_wham"
    bl_label = "Import WHAM Checkpoint Files"
    bl_description = "Use this option having the 'wham_checkpoints.zip' file."

    # option: IntProperty(name='Chosse type PKL',default=0) #0 = CEB 4d Humans PKL (Pickle) | 1 = 4d Humans PKL (joblib)

    filename_ext = ".zip"
    filter_glob: StringProperty(
        default="*.zip",
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )
    def execute(self,context):
        # path_addon = os.path.dirname(os.path.abspath(__file__))
        # fourd_prop = context.scene.fourd_prop
        import shutil
        path_addon = os.path.dirname(os.path.abspath(__file__))
        ckpt_folder = os.path.join(path_addon,'WHAM','checkpoints')

        if not os.path.exists(ckpt_folder):
            os.makedirs(ckpt_folder)
        
        zip_file = self.filepath
        print('...Starting of Unziping WHAM Checkpoints...')
        shutil.unpack_archive(zip_file, ckpt_folder)
        print('...End of Unzip WHAM Checkpoints...')

        
        return{'FINISHED'}


class ZeroFrameTPose(Operator):
    bl_idname = "fdh.zero_frame_t_pose"
    bl_label = "T Pose Frame 0"
    bl_description = "Make the frame 0 to have T Pose"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self,context):
        current_frame = context.scene.frame_current

        context.scene.frame_current = 0
        armature_ref = bpy.context.selected_objects[0]
        if bpy.context.active_object.mode != 'POSE':
            bpy.ops.object.mode_set(mode='POSE')
        bpy.ops.pose.select_all(action='SELECT')

        bpy.ops.pose.rot_clear()
        bpy.ops.pose.loc_clear()

        for b in armature_ref.pose.bones:
            if b.name  in ['m_avg_root','m_avg_Pelvis']:
                b.keyframe_insert('location', frame=0)  
                b.keyframe_insert('rotation_quaternion', frame=0)  
            else:
                b.keyframe_insert('rotation_quaternion', frame=0)  
        
        bpy.ops.object.mode_set(mode='OBJECT')
        context.scene.frame_current = current_frame
        
        return{'FINISHED'}
    

class RemoveLocationAnimation(Operator):
    bl_idname = "fdh.remove_location_animation"
    bl_label = "Remove Loc Anim"
    bl_description = "Remove Location Animation"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self,context):
        # from mathutils import Vector
        # current_frame = context.scene.frame_current

        # start = context.scene.frame_start
        end = context.scene.frame_end
        armature_ref = bpy.context.selected_objects[0]
        # if bpy.context.active_object.mode != 'POSE':
        #     bpy.ops.object.mode_set(mode='POSE')
        # bpy.ops.pose.select_all(action='SELECT')

        # b_pelvis = armature_ref.pose.bones['m_avg_Pelvis']
        action = armature_ref.animation_data.action
        fcurves = [fc for fc in action.fcurves if fc.data_path == 'pose.bones["m_avg_Pelvis"].location']


        for f in range(0,end+1):
            fcurves[0].keyframe_points[f].co.y = 0
        # context.scene.frame_current = current_frame
        
        return{'FINISHED'}

class CopyNameToNLA(Operator):
    bl_idname = "fdh.nla_copy_name_to_nla"
    bl_label = "Copy Name"
    bl_description = "Copy name of the animation to NLA"
    # bl_options = {"REGISTER", "UNDO"}

    def execute(self,context):
        fourd_prop = context.scene.fourd_prop

        if fourd_prop.str_videopath != '':
            fourd_prop.str_nla_name = os.path.splitext(os.path.basename(fourd_prop.str_videopath))[0]
        elif fourd_prop.str_pklpath != '':
            fourd_prop.str_nla_name = os.path.splitext(os.path.basename(fourd_prop.str_pklpath))[0]
        else:
            fourd_prop.str_nla_name = 'Action'
        

        return{'FINISHED'}
    

class CreateNLAStrip(Operator):
    bl_idname = "fdh.nla_create_strip"
    bl_label = "Create"
    bl_description = "Create NLA Strip"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self,context):
        fourd_prop = context.scene.fourd_prop

        armature = bpy.context.selected_objects[0]
        # if armature.animation_data is not None:
        #     action = armature.animation_data.action
        #     if action is not None:
        #         action.name=fourd_prop.str_nla_name
        #         track = armature.animation_data.nla_tracks.new()
        #         track.strips.new(action.name, int(action.frame_range[0]), action)
        #         armature.animation_data.action = None

        if armature.animation_data is not None:
            action = armature.animation_data.action
            if action is not None:
                action.name=fourd_prop.str_nla_name

                #procurando index da acao criada
                act_idx = 0
                for i,ac in enumerate(bpy.data.actions):
                    if ac.name == armature.animation_data.action.name:
                        act_idx = i

                armature.animation_data.action = None

        if len(armature.animation_data.nla_tracks) >0 and len(armature.animation_data.nla_tracks[0].strips)>0:
            frame_end = armature.animation_data.nla_tracks[0].strips[-1].frame_end
            context.scene.frame_end = int(frame_end)

        
        context.scene.active_action_index = act_idx

        fourd_prop.str_nla_name = ''
        
        return{'FINISHED'}
    

class RemoveNLAStrip(Operator):
    bl_idname = "fdh.nla_delete_action"
    bl_label = "Delete Action"
    bl_description = "Delete Action"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        # return context.scene.hair_list
        return bpy.data.actions

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)

    def execute(self,context):
        # fourd_prop = context.scene.fourd_prop
        scn = context.scene
        idx = scn.active_action_index
        # print('idx: ',idx)

        bpy.data.actions.remove(bpy.data.actions[idx])
        # scn.active_object_index=0

        return{'FINISHED'}

class LoadActionToCharFromNLA(Operator):
    bl_idname = "fdh.nla_load_action"
    bl_label = "Load Action"
    bl_description = "Load NLA Action to current Character"
    # bl_options = {"REGISTER", "UNDO"}

    # @classmethod
    # def poll(cls, context):
    #     # return context.scene.hair_list
    #     return bpy.data.actions


    def execute(self,context):
        fourd_prop = context.scene.fourd_prop
        scn = context.scene
        idx = scn.active_action_index
        print('idx: ',idx)

        ob = bpy.context.object
        ob.animation_data.action = bpy.data.actions[idx]
        
        frame_end = bpy.data.actions[idx].frame_range[1]
        context.scene.frame_end = int(frame_end)

        #colocando nome na caixa de edicao
        fourd_prop.str_nla_name = ob.animation_data.action.name

        return{'FINISHED'}
    
class SetNoAction(Operator):
    bl_idname = "fdh.set_no_action"
    bl_label = "No Action"
    bl_description = "Set no Action to Character"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self,context):
        fourd_prop = context.scene.fourd_prop

        armature = bpy.context.selected_objects[0]


        if armature.animation_data is not None:
            armature.animation_data.action = None

        if len(armature.animation_data.nla_tracks) >0 and len(armature.animation_data.nla_tracks[0].strips)>0:
            frame_end = armature.animation_data.nla_tracks[0].strips[-1].frame_end
            context.scene.frame_end = int(frame_end)

        #limpa caixa de edicao de nome
        fourd_prop.str_nla_name = ''
        
        return{'FINISHED'}
    

class AddTrack(Operator):
    bl_idname = "fdh.nla_add_track"
    bl_label = "Add Track"
    bl_description = "Add Track"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self,context):
        fourd_prop = context.scene.fourd_prop

        scn = context.scene
        idx = scn.active_action_index
        print('idx: ',idx)

        ob = bpy.context.object
        ob.animation_data.action = bpy.data.actions[idx]

        armature = bpy.context.selected_objects[0]
        if armature.animation_data is not None:
            action = armature.animation_data.action
            if action is not None:
                # action.name=fourd_prop.str_nla_name
                track = armature.animation_data.nla_tracks.new()
                # track.strips.new(action.name, int(action.frame_range[0]), action)
                track.strips.new('4d_humans', int(action.frame_range[0]), action)
                armature.animation_data.action = None

        context.scene.active_track_index=len(armature.animation_data.nla_tracks[0].strips)-1
        
        return{'FINISHED'}

class AddActionToTrack(Operator):
    bl_idname = "fdh.add_action_to_track"
    bl_label = "Add Action"
    bl_description = "Add Action"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self,context):
        # fourd_prop = context.scene.fourd_prop

        armature = bpy.context.selected_objects[0]
        act_idx = bpy.context.scene.active_action_index
        qtd_actions = len(armature.animation_data.nla_tracks[0].strips)
        if qtd_actions == 0:
            action_end = 1
        else:
            action_end = armature.animation_data.nla_tracks[0].strips[qtd_actions-1].frame_end
        action_to_add = bpy.data.actions[act_idx]

        armature.animation_data.nla_tracks[0].strips.new(action_to_add.name,int(action_end),action_to_add)

        frame_end = armature.animation_data.nla_tracks[0].strips[-1].frame_end
        context.scene.frame_end = int(frame_end)

        context.scene.active_track_index=len(armature.animation_data.nla_tracks[0].strips)-1
        
        return{'FINISHED'}


# add strip
# armature.animation_data.nla_tracks[0].strips.new('prank_derruba',410,bpy.data.actions['prank_derruba'])

class AddActionToTrackWTransition(Operator):
    bl_idname = "fdh.add_action_to_track_w_transition"
    bl_label = "Add Action W/ Transition"
    bl_description = "Add Action with Transition"
    bl_options = {"REGISTER", "UNDO"}

    option: IntProperty(name='Trasition option',default=0) #0= adiciona com uma nova acao, 1 = adiciona com a acao anterior; 2=adiciona com a acao seguinte

    def execute(self,context):
        fourd_prop = context.scene.fourd_prop
        # """
        scr      = bpy.context.window.screen
        nla_window = 0 
        for area in scr.areas:
            if area.type == 'NLA_EDITOR':
                    nla_window = 1

        if nla_window ==0: #criar um pequeno trecho com uma janela do nla editor
            bpy.ops.screen.area_split(direction='HORIZONTAL', factor=0.02)
            new_area = bpy.context.screen.areas[-1]
            new_area.type='NLA_EDITOR'

        win      = bpy.context.window
        scr      = win.screen
        areas3d  = [area for area in scr.areas if area.type == 'NLA_EDITOR']
        with bpy.context.temp_override(area=areas3d[0]):
            bpy.ops.nla.select_all(action='DESELECT')

        armature = bpy.context.selected_objects[0]
        arm_track = armature.animation_data.nla_tracks[0]
        act_idx = bpy.context.scene.active_action_index
        trck_idx = bpy.context.scene.active_track_index
        qtd_actions = len(armature.animation_data.nla_tracks[0].strips)
        f_trans = fourd_prop.int_frames_transition


        if self.option == 0: #adiciona com nova acao apos a ultima acao do nla
            action_end = arm_track.strips[qtd_actions-1].frame_end
            prev_action = arm_track.strips[qtd_actions-1]
            prev_action.select = True
            action_end_w_transition = action_end + fourd_prop.int_frames_transition
            action_to_add = bpy.data.actions[act_idx]
            armature.animation_data.nla_tracks[0].strips.new(action_to_add.name,int(action_end_w_transition),action_to_add)
            with bpy.context.temp_override(area=areas3d[0]):
                bpy.ops.nla.transition_add()

        if self.option == 1: #adiciona transition em cima da acao anterior
            act_in_strip = [] # monta lista para recirar a organizacao
            for f_trk in range(trck_idx-1,qtd_actions):
                print('track_atual: ',f_trk)
                f_start = arm_track.strips[f_trk].frame_start
                f_end = arm_track.strips[f_trk].frame_end 
                act_in_strip.append([f_trk,f_start,f_end,f_start+f_trans,f_end+f_trans])

            for f in reversed(act_in_strip):#preenche de tras pra frente, senao nao funciona
                if f[0] >= trck_idx:
                    arm_track.strips[f[0]].frame_start = f[3]
                    arm_track.strips[f[0]].frame_end = f[4]
                print(f)


            arm_track.strips[trck_idx-1].select = True #seleciona o action anterior
            arm_track.strips[trck_idx].select = True #seleciona o action atual


            with bpy.context.temp_override(area=areas3d[0]):
                bpy.ops.nla.transition_add()

        if self.option == 2: #adiciona transition em cima da acao posterior
            act_in_strip = []
            for f_trk in range(trck_idx+1,qtd_actions):
                print('track_atual: ',f_trk)
                f_start = arm_track.strips[f_trk].frame_start
                f_end = arm_track.strips[f_trk].frame_end 
                act_in_strip.append([f_trk,f_start,f_end,f_start+f_trans,f_end+f_trans])

            for f in reversed(act_in_strip):
                if f[0] >= trck_idx:
                    arm_track.strips[f[0]].frame_start = f[3]
                    arm_track.strips[f[0]].frame_end = f[4]
                print(f)

            arm_track.strips[trck_idx].select = True #seleciona o action atual
            arm_track.strips[trck_idx+1].select = True #seleciona o action seguinte

            with bpy.context.temp_override(area=areas3d[0]):
                bpy.ops.nla.transition_add()

        frame_end = arm_track.strips[-1].frame_end
        context.scene.frame_end = int(frame_end)

        context.scene.active_track_index=len(armature.animation_data.nla_tracks[0].strips)-1

        return{'FINISHED'}

class RemoveActionFromtrack(Operator):
    bl_idname = "fdh.delete_action_from_track"
    bl_label = "Delete Action From Track"
    bl_description = "Delete Action From Track"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        # return context.scene.hair_list

        if len(bpy.context.selected_objects) >0:
            ob = bpy.context.selected_objects[0]
        else:
            ob = None

        if ob is not None and  hasattr(ob.animation_data,'nla_tracks') and len(ob.animation_data.nla_tracks[0].strips)>0:
            var_return = ob.animation_data.nla_tracks[0].strips
        else:
            var_return = None
        return var_return

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)

    def execute(self,context):
        # fourd_prop = context.scene.fourd_prop
        scn = context.scene
        idx = scn.active_track_index
        # print('idx: ',idx)
        armature = bpy.context.selected_objects[0]

        armature.animation_data.nla_tracks[0].strips.remove(armature.animation_data.nla_tracks[0].strips[idx])
        if len(armature.animation_data.nla_tracks[0].strips) == 0:
            scn.active_track_index= -1
        else: 
            scn.active_track_index=0


        return{'FINISHED'}
    
class Open_NLA_VIEW(Operator):
    bl_idname = "fdh.open_nla_view"
    bl_label = "Open NLA_VIEW"
    bl_description = "Open NLA View"
    # bl_options = {"REGISTER", "UNDO"}

    def execute(self,context):
        fourd_prop = context.scene.fourd_prop
        # """
        scr      = bpy.context.window.screen
        nla_window = 0 
        for area in scr.areas:
            if area.type == 'NLA_EDITOR':
                    nla_window = 1

        if nla_window ==0: #criar um pequeno trecho com uma janela do nla editor
            bpy.ops.screen.area_split(direction='HORIZONTAL', factor=0.18)
            new_area = bpy.context.screen.areas[-1]
            new_area.type='NLA_EDITOR'

        return{'FINISHED'}
    
class OrganizeStrip(Operator):
    bl_idname = "fdh.organize_strip"
    bl_label = "Organize Strip"
    bl_description = "Organize Actions on the Strip (remove empty spaces)"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self,context):
        fourd_prop = context.scene.fourd_prop

        armature = bpy.context.selected_objects[0]
        arm_track = armature.animation_data.nla_tracks[0]
        # act_idx = bpy.context.scene.active_action_index
        trck_idx = bpy.context.scene.active_track_index
        qtd_actions = len(armature.animation_data.nla_tracks[0].strips)
        f_trans = fourd_prop.int_frames_transition

        #length da acao
        # track_act_start = arm_track.strips[trck_idx].action_frame_start
        # track_act_end = arm_track.strips[trck_idx].action_frame_end
        # act_length = track_act_end - track_act_start

        def checa_org(arm_track_in,qtd_actions_in):
            organizar = 0
            # checa se estao na sequencia
            strip_test = []
            for f_t in range(0,qtd_actions_in): #coleta ordem dos actions no strip
                f_start_t = arm_track_in.strips[f_t].frame_start
                f_end_t = arm_track_in.strips[f_t].frame_end 
                if f_t == 0:
                    strip_t_append = [f_t,f_start_t,f_end_t,0-f_start_t,0+f_end_t]
                else:
                    prox_start = strip_test[-1][2]-f_start_t
                    prox_end = prox_start+f_end_t
                    strip_t_append = [f_t,f_start_t,f_end_t,prox_start,prox_end]
                    
                strip_test.append(strip_t_append)
                # print(strip_t_append)

            for f_tt in strip_test:
                if f_tt[3] != 0:
                    organizar = organizar +1
            
            print('organizar: ',organizar)
            return organizar
        
        organizar = checa_org(arm_track,qtd_actions)
        # print('org fora: ',organizar)

        while organizar > 0:


            act_in_strip = []
            for f_trk in range(0,qtd_actions):
                # print('track_atual: ',f_trk)
                f_start = arm_track.strips[f_trk].frame_start
                f_end = arm_track.strips[f_trk].frame_end 
                if f_trk == 0:
                    f_start_primeiro = arm_track.strips[f_trk].frame_start
                    act_in_strip.append([f_trk,f_start,f_end,0,f_end-f_start])
                else:
                    last_end = act_in_strip[-1][4]
                    dif = f_start-last_end
                    cur_start = f_start-dif
                    cur_end = f_end-f_start + cur_start

                    # print('dif: ',dif)
                    # act_in_strip.append([f_trk,f_start,f_end,f_start-dif ,f_end-dif,(f_end-dif)-(f_start-dif)])
                    act_in_strip.append([f_trk,f_start,f_end,cur_start ,cur_end,cur_end-cur_start])
                    
            print("2-act in strip")
            for st in act_in_strip:
                print(st)
            print('-------------')

            #somar todos os actions, comparar a soma dos actions com o frame end do ultimo action
            # total = 0
            # for tot in arm_track.strips:
            #     tmp = tot.frame_end - tot.frame_start
            #     total  = total + tmp
            # print('total: ',total)
            # last_act_frame = arm_track.strips[-1].frame_end
            # print('last_act_frame: ',last_act_frame)


            if f_start_primeiro < 0: #primeiro empurra tudo pra frente pra passar do negativo no primeiro action
                for f in reversed(act_in_strip):
                    # arm_track.strips[f[0]].frame_start = f[3]
                    # arm_track.strips[f[0]].frame_end = f[4] 
                    arm_track.strips[f[0]].frame_start = arm_track.strips[f[0]].frame_start + abs(f_start_primeiro)
                    arm_track.strips[f[0]].frame_end = arm_track.strips[f[0]].frame_end  + abs(f_start_primeiro)

                    print(f)
            else:

                for f in act_in_strip:
                    arm_track.strips[f[0]].frame_start = f[3]
                    arm_track.strips[f[0]].frame_end = f[4] 
                    # print(f)

            organizar = checa_org(arm_track,qtd_actions)

        print('######################')
        print('######################')



            

        return{'FINISHED'}
    
class SelectActionOnStrip(Operator):
    bl_idname = "fdh.select_action_on_strip"
    bl_label = "Select Action"
    bl_description = "Select Action on Strip"
    # bl_options = {"REGISTER", "UNDO"}

    option: IntProperty(name='Select on NLA editor',default=0) #0= selectiona uma action, 1=seleciona todas as actions no strip, 2=desmarca todas

    def execute(self,context):
        fourd_prop = context.scene.fourd_prop

        scr      = bpy.context.window.screen
        nla_window = 0 
        for area in scr.areas:
            if area.type == 'NLA_EDITOR':
                    nla_window = 1

        if nla_window ==0: #criar um pequeno trecho com uma janela do nla editor
            bpy.ops.screen.area_split(direction='HORIZONTAL', factor=0.02)
            new_area = bpy.context.screen.areas[-1]
            new_area.type='NLA_EDITOR'

        armature = bpy.context.selected_objects[0]
        arm_track = armature.animation_data.nla_tracks[0]
        # act_idx = bpy.context.scene.active_action_index
        trck_idx = bpy.context.scene.active_track_index

        win      = bpy.context.window
        scr      = win.screen

        if self.option in [0,2]: # se for pra selecionar apenas uma ou desmarcar todas, rodar o desmarc todas
            areas3d  = [area for area in scr.areas if area.type == 'NLA_EDITOR']
            with bpy.context.temp_override(area=areas3d[0]):
                bpy.ops.nla.select_all(action='DESELECT')

        if self.option == 0: # Seleciona apenas uma (ates desmarca todas no if anterior)
            arm_track.strips[trck_idx].select = True #seleciona o action atual

        if self.option ==1:
            areas3d  = [area for area in scr.areas if area.type == 'NLA_EDITOR']
            with bpy.context.temp_override(area=areas3d[0]):
                bpy.ops.nla.select_all(action='SELECT')


        

        return{'FINISHED'}


class MatchToPrevAction(Operator):
    bl_idname = "fdh.match_to_prev_action"
    bl_label = "Match to Previous"
    bl_description = "Match to Previous Action"
    bl_options = {"REGISTER", "UNDO"}

    # option: IntProperty(name='',default=0) #

    def execute(self,context):

        #primeiro duplicar o action
        idx = bpy.context.scene.active_track_index


        armature = bpy.context.selected_objects[0]
        arm_track = armature.animation_data.nla_tracks[0]


        action = arm_track.strips[idx].action
        #criar copia para poder alterar
        action_copy = action.copy()
        new_name = action.name+'_altered'
        action_copy.name = new_name
        arm_track.strips[idx].action = action_copy


        # pegar localização e rotacao do ultimo frame ada acao anterior
        #pegar dado do action anterior
        if arm_track.strips[idx-1].type == 'CLIP':
            get_last_action = arm_track.strips[idx-1].action
        else:#o else deve ser caso o anteior seja transition
            get_last_action = arm_track.strips[idx-2].action

        fcurves = [fc for fc in get_last_action.fcurves if fc.data_path == 'pose.bones["m_avg_Pelvis"].location']
        print('start')
        x = fcurves[0].keyframe_points[-1].co.y
        y = fcurves[1].keyframe_points[-1].co.y
        z = fcurves[2].keyframe_points[-1].co.y

        fcurves_quat = [fc for fc in get_last_action.fcurves if fc.data_path == 'pose.bones["m_avg_Pelvis"].rotation_quaternion']

        q_w = fcurves_quat[0].keyframe_points[-1].co.y
        q_x = fcurves_quat[1].keyframe_points[-1].co.y
        q_y = fcurves_quat[2].keyframe_points[-1].co.y
        q_z = fcurves_quat[3].keyframe_points[-1].co.y


        # pegando dados da acao atual
        fcurves = [fc for fc in action_copy.fcurves if fc.data_path == 'pose.bones["m_avg_Pelvis"].location']

        cur_x = fcurves[0].keyframe_points[0].co.y # da acao atual tenho que pegar o primeiro frame
        cur_y = fcurves[1].keyframe_points[0].co.y
        cur_z = fcurves[2].keyframe_points[0].co.y

        fcurves_quat = [fc for fc in action_copy.fcurves if fc.data_path == 'pose.bones["m_avg_Pelvis"].rotation_quaternion']

        cur_q_w = fcurves_quat[0].keyframe_points[0].co.y
        cur_q_x = fcurves_quat[1].keyframe_points[0].co.y
        cur_q_y = fcurves_quat[2].keyframe_points[0].co.y
        cur_q_z = fcurves_quat[3].keyframe_points[0].co.y

        #calcular a diferenca entre a acao anteior e a atual (localização e rotação)

        dif_x = x - cur_x
        dif_y = y - cur_y
        dif_z = z - cur_z

        dif_q_w = q_w - cur_q_w
        dif_q_x = q_x - cur_q_x
        dif_q_y = q_y - cur_q_y
        dif_q_z = q_z - cur_q_z


        ### replicando a diferenca na acao atual
        #pegando primeiro e ultimo frame da acao atual
        for f in range(int(action_copy.frame_range[0]), int(action_copy.frame_range[1])):
            fcurves[0].keyframe_points[f].co.y = fcurves[0].keyframe_points[f].co.y + dif_x
            fcurves[1].keyframe_points[f].co.y = fcurves[1].keyframe_points[f].co.y + dif_y
            fcurves[2].keyframe_points[f].co.y = fcurves[2].keyframe_points[f].co.y + dif_z

            fcurves_quat[0].keyframe_points[f].co.y = fcurves_quat[0].keyframe_points[f].co.y + dif_q_w
            fcurves_quat[1].keyframe_points[f].co.y = fcurves_quat[1].keyframe_points[f].co.y + dif_q_x
            fcurves_quat[2].keyframe_points[f].co.y = fcurves_quat[2].keyframe_points[f].co.y + dif_q_y
            fcurves_quat[3].keyframe_points[f].co.y = fcurves_quat[3].keyframe_points[f].co.y + dif_q_z

        #aplicar essa diferenca para toda a curva do loc e rot do pelvis da acao atual


        #trocando nome da strip para identificar facilmente que ele foi alterado
        arm_track.strips[idx].name=new_name


        return{'FINISHED'}


class CreateReferenceAction(Operator):
    bl_idname = "fdh.create_ref"
    bl_label = "Create Ref Action"
    bl_description = "Create Reference Action"
    bl_options = {"REGISTER", "UNDO"}

    # option: IntProperty(name='',default=0) #

    def execute(self,context):
        ob = bpy.context.object
        ob.animation_data.action = None

        from mathutils import Matrix

        ob.pose.bones

        #reseta a orientacao de todos os bones
        for pb in ob.pose.bones:
            pb.matrix_basis = Matrix() #  == Matrix.Identity(4)

        bone_pelvis = ob.pose.bones['m_avg_Pelvis']

        bone_pelvis.keyframe_insert('rotation_quaternion', frame=0)
        bone_pelvis.keyframe_insert('location', frame=0)

        ob.animation_data.action.name = '0_ref'

        return{'FINISHED'}


class Retarget(Operator):
    bl_idname = "fdh.retarget"
    bl_label = "Retarget"
    bl_description = "Retarget"
    bl_options = {"REGISTER", "UNDO"}

    option: IntProperty(name='',default=0) #0=bind; 1 = unbind

    def execute(self,context):
        # bind(context)
        fourd_prop = context.scene.fourd_prop
        # aplicar copy location para pelvis

        #aplicar copy rotation para os outros bones

        # rig = [
        #     ['m_avg_root',''],
        #     ['m_avg_Pelvis','mixamorig1:Hips'],
        #     ['m_avg_L_Hip','mixamorig1:LeftUpLeg'],
        #     ['m_avg_L_Knee','mixamorig1:LeftLeg'],
        #     ['m_avg_L_Ankle','mixamorig1:LeftFoot'],
        #     ['m_avg_L_Foot','mixamorig1:LeftToeBase'],
        #     ['m_avg_R_Hip','mixamorig1:RightUpLeg'],
        #     ['m_avg_R_Knee','mixamorig1:RightLeg'],
        #     ['m_avg_R_Ankle','mixamorig1:RightFoot'],
        #     ['m_avg_R_Foot','mixamorig1:RightToeBase'],
        #     ['m_avg_Spine1','mixamorig1:Spine'],
        #     ['m_avg_Spine2','mixamorig1:Spine1'],
        #     ['m_avg_Spine3','mixamorig1:Spine2'],
        #     ['m_avg_Neck','mixamorig1:Neck'],
        #     ['m_avg_Head','mixamorig1:Head'],
        #     ['m_avg_L_Collar','mixamorig1:LeftShoulder'],
        #     ['m_avg_L_Shoulder','mixamorig1:LeftArm'],
        #     ['m_avg_L_Elbow','mixamorig1:LeftForeArm'],
        #     ['m_avg_L_Wrist','mixamorig1:LeftHand'],
        #     ['m_avg_L_Hand',''],
        #     ['m_avg_R_Collar','mixamorig1:RightShoulder'],
        #     ['m_avg_R_Shoulder','mixamorig1:RightArm'],
        #     ['m_avg_R_Elbow','mixamorig1:RightForeArm'],
        #     ['m_avg_R_Wrist','mixamorig1:RightHand'],
        #     ['m_avg_R_Hand',''],
        # ]

        path_addon = os.path.dirname(os.path.abspath(__file__))
        rig_file = os.path.join(path_addon,'rig',fourd_prop.enum_list_rig+'.json')
        with open(rig_file,'r') as op_file:
            rig = json.load(op_file)

        scn = context.scene
        if fourd_prop.enum_list_rig.startswith('mixamo'):
            bone_prefix = scn.target.data.bones[0].name.split(':')[0]
            upt_rig = []
            for r in rig:
                if r[1] != '':
                    # u_rig = [r[0],fourd_prop.str_retarget_prefix+r[1]]
                    u_rig = [r[0],bone_prefix + ':' +r[1]]
                else:
                    u_rig = [r[0],'']
                upt_rig.append(u_rig)
            rig = upt_rig


        # path= r'D:\0_Programs\CEB_4D_Human_prj\mixamo_rig.json'
        # json_object = json.dumps(rig, indent=4)
        # with open(path, "w") as outfile:
        #     json.dump(json_object, outfile)


        if self.option == 0:#bind
            target = 'target'
            bind(context,rig,target)
            # if bpy.context.active_object.mode != 'OBJECT':
            #     bpy.ops.object.mode_set(mode='OBJECT')

            # #etapa 1 - duplica armature origem, e criar constraint de "copy transforms" mix: before original(aligned); target: local; owner: local

            # scn.source.select_set(True)
            # bpy.context.view_layer.objects.active = scn.source

            # bpy.ops.object.transform_apply(location=False, rotation=True, scale=True) # aplica transform no source



                
            # #duplicando armature para apply scale
            # bpy.ops.object.select_all(action='DESELECT')
            # scn.target.select_set(True)
            # bpy.ops.object.duplicate(linked=False)

            # target_duplicate = bpy.context.selected_objects[0]

            # #com a armture destino duplicada, apply scale
            # # bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
            # bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)


            # scn.source.select_set(True)

            # if bpy.context.active_object.mode != 'EDIT':
            #     bpy.ops.object.mode_set(mode='EDIT')

            # #copiando bones, e suas informacoes
            # for b in rig:
            #     bone = scn.source.data.edit_bones[b[0]]
            #     copy_bone = scn.source.data.edit_bones.new(bone.name+'_CEB4D')
            #     copy_bone.length = bone.length
            #     if bone.parent:
            #         copy_bone.parent = scn.source.data.edit_bones[bone.parent.name+'_CEB4D']
            #     copy_bone.matrix = bone.matrix.copy()
            #     #colocar copia do destino nesse rig
            #     if b[1] != '':
            #         bone_dest = target_duplicate.data.edit_bones[b[1]]
            #         copy_bone_dest = scn.source.data.edit_bones.new(bone_dest.name+'_CP_CEB4D')
            #         copy_bone_dest.length = bone_dest.length
            #         copy_bone_dest.parent = scn.source.data.edit_bones[b[0]+'_CEB4D']
            #         copy_bone_dest.matrix = bone_dest.matrix.copy()

            # #"""
            # bpy.ops.object.mode_set(mode='OBJECT')

            # for b in rig:
            #     scn.source.pose.bones[b[0]+'_CEB4D'].constraints.new('COPY_TRANSFORMS')
            #     scn.source.pose.bones[b[0]+'_CEB4D'].constraints[0].target = scn.source
            #     scn.source.pose.bones[b[0]+'_CEB4D'].constraints[0].subtarget = b[0]
            #     scn.source.pose.bones[b[0]+'_CEB4D'].constraints[0].mix_mode = 'BEFORE'
            #     scn.source.pose.bones[b[0]+'_CEB4D'].constraints[0].target_space = 'LOCAL'
            #     scn.source.pose.bones[b[0]+'_CEB4D'].constraints[0].owner_space = 'LOCAL'
    
    


            # # fazr a copia do transform do armature clonado
            # for b in rig:
            #     if b[1] != '':
            #         cp_rot = scn.target.pose.bones[b[1]].constraints.new('COPY_ROTATION')
            #         cp_rot.name = cp_rot.name + '_CEB4D'
            #         cp_rot.target = scn.source
            #         cp_rot.subtarget = b[1]+'_CP_CEB4D'
            #         # scn.target.pose.bones[b[1]].constraints[0].target = scn.source
            #         # scn.target.pose.bones[b[1]].constraints[0].subtarget = b[1]+'_CP_CEB4D'
            #     if b[0] == 'm_avg_Pelvis':
            #         # cp_loc = scn.target.pose.bones[b[1]].constraints.new('COPY_LOCATION')
            #         # cp_loc.name = cp_loc.name + '_CEB4D'
            #         # cp_loc.target = scn.source
            #         # cp_loc.subtarget = b[0] #pegar o location original, deferente do ARP nao estou copiando o bone
            #         # # scn.target.pose.bones[b[1]].constraints[1].target = scn.source
            #         # # scn.target.pose.bones[b[1]].constraints[1].subtarget = b[0] #pegar o location original, deferente do ARP nao estou copiando o bone
            #         if context.scene.target.name.startswith('STG2_'):
            #             cp_loc = scn.target.pose.bones['Ctrl_Hips'].constraints.new('COPY_LOCATION')
            #         else:
            #             cp_loc = scn.target.pose.bones[b[1]].constraints.new('COPY_LOCATION')
            #         cp_loc.name = cp_loc.name + '_CEB4D'
            #         cp_loc.target = scn.source
            #         cp_loc.subtarget = b[0] 

            
            
            
            # # bpy.ops.object.mode_set(mode='OBJECT')

            # #apagar a copia do armature que fiz para "apply scale"
            # bpy.ops.object.select_all(action='DESELECT')
            # target_duplicate.select_set(True)
            # bpy.context.view_layer.objects.active = target_duplicate
            # bpy.ops.object.delete() #apaga duplicata que fiz "apply transforms"

            # # fourd_prop = context.scene.fourd_prop

            # # scn.target.select_set(True)
            # # start_frame = context.scene.frame_start
            # # end_frame = context.scene.frame_end
            # # bpy.context.view_layer.objects.active = scn.target
            # # bpy.ops.nla.bake(frame_start=start_frame, frame_end=end_frame, 
            # #                 only_selected=fourd_prop.bool_selected_bones, visual_keying=True, clear_constraints=True, 
            # #                 clear_parents=False, use_current_action=True, clean_curves=False, bake_types={'POSE'})
            # #"""
            # scn.target['bind']=1



        if self.option == 1: #unbind

            # armature = context.scene.source
            # armature.select_set(True)
            # bpy.context.view_layer.objects.active = armature #estou selecionando o armature aqui para poder fazer o mode abaixo funcionar, caso o personagem nao esteja selecionado


            # if bpy.context.active_object.mode != 'OBJECT':
            #     bpy.ops.object.mode_set(mode='OBJECT')

            # bpy.ops.object.select_all(action='DESELECT')

            # armature.select_set(True)
            # bpy.context.view_layer.objects.active = armature



            # for b in scn.target.pose.bones:
            #     # while len(b.constraints) > 0:
            #     #     b.constraints.remove(b.constraints[0])

            #     for b_c in b.constraints:
            #         if b_c.name.endswith('_CEB4D'):
            #             b.constraints.remove(b_c)

            # scn.target['bind']=0



            # ## apagando bones criados
            # bpy.ops.object.mode_set(mode='EDIT')
            # for bone in armature.data.edit_bones:
            #     # print(bone.name)
            #     if bone.name.find("_CEB4D")> 0: 
            #         # print('apagar: ',bone.name)
            #         armature.data.edit_bones.remove(bone)

            # bpy.ops.object.mode_set(mode='OBJECT')
            target = 'target'
            unbind(context,target)

        if self.option ==2: #Apply retarget
            target = 'target'
            retarget(context,target)
            # fourd_prop = context.scene.fourd_prop

            # scn.target.select_set(True)
            # start_frame = context.scene.frame_start
            # end_frame = context.scene.frame_end
            # bpy.context.view_layer.objects.active = scn.target
            # if context.scene.target.name.startswith('STG2_'):
            #     bpy.ops.nla.bake(frame_start=start_frame, frame_end=end_frame, 
            #                 only_selected=fourd_prop.bool_selected_bones, visual_keying=True, clear_constraints=False, 
            #                 clear_parents=False, use_current_action=True, clean_curves=False, bake_types={'POSE'})
            # else:
            #     bpy.ops.nla.bake(frame_start=start_frame, frame_end=end_frame, 
            #                 only_selected=fourd_prop.bool_selected_bones, visual_keying=True, clear_constraints=True, 
            #                 clear_parents=False, use_current_action=True, clean_curves=False, bake_types={'POSE'})
            
            # #removendo bones criados no bind
            # unbind(context)
            
            # if fourd_prop.bool_retarget_hide_source:
            #     scn.source.hide_render = True
            #     scn.source.hide_viewport = True

            #     for ob in bpy.data.objects:
            #         if ob.parent == scn.source:
            #             src_mesh = ob
            #             print('found mesh')
            #     src_mesh.hide_viewport = True
            #     src_mesh.hide_render = True    

            # scn.target['bind']=0    




        return{'FINISHED'}
    

class Stage2(Operator):
    bl_idname = "fdh.stage2"
    bl_label = "Apply"
    bl_description = "Move the animation to a more complete armature for editing"
    bl_options = {"REGISTER", "UNDO"}

    option: IntProperty(name='',default=0) #0=bind; 1 = unbind

    def execute(self,context):
        fourd_prop = context.scene.fourd_prop

        return{'FINISHED'}
    

class ExtractMarkedFrames(Operator):
    bl_idname = "fdh.extract_marked_frames"
    bl_label = "Extract Marked frames"
    bl_description = "Extract Marked frames"
    bl_options = {"REGISTER", "UNDO"}

    # option: IntProperty(name='',default=0) 

    def execute(self,context):
        fourd_prop = context.scene.fourd_prop

        # Pegar frames onde tem marcador
        markers = []
        for m in bpy.context.scene.timeline_markers:
            markers.append(m.frame)

        #pegar bones selecionados


        # apagar keyframes exceto dos que estao no "markers"
        # armature = context.scene.source
        armature = context.active_object

        frame_start = int(armature.animation_data.action.fcurves[0].range()[0])
        frame_end = int(armature.animation_data.action.fcurves[0].range()[1])

        

        #nome do bone
        # bpy.data.objects['Amt_C01'].animation_data.action.fcurves[0].data_path.split('"')[1]
        fcurves = armature.animation_data.action.fcurves

        for f in range(frame_start,frame_end+1):
            for bone in armature.pose.bones:
                if f not in markers:
                    bone.keyframe_delete(data_path='rotation_quaternion',frame=f)
                    bone.keyframe_delete(data_path='location',frame=f)
                    bone.keyframe_delete(data_path='rotation_euler',frame=f)
                    bone.keyframe_delete(data_path='scale',frame=f)
            for fc in fcurves:
                if fc.data_path.endswith('["ik_fk_switch"]'):
                    kpoints = fc.keyframe_points.values()
                    for kp in kpoints:
                        if f not in markers and f == int(kp.co[0]):
                            fc.keyframe_points.remove(kp)
                    

        #convertendo a interpolação para bezier
        for fc in armature.animation_data.action.fcurves:
            for kp in fc.keyframe_points:
                kp.interpolation = 'BEZIER'

        ## Apagando custom fcurve
        # # C.active_object.animation_data.action.fcurves[-1].keyframe_points.remove(C.active_object.animation_data.action.fcurves[-1].keyframe_points.values()[0])
        # fcurves = armature.animation_data.action.fcurves
        # for fc in fcurves:
        #     if fc.data_path.endswith('["ik_fk_switch"]'):
        #         kpoints = fc.keyframe_points.values()
        #         for kp in kpoints:
        #             if f not in markers and f != int(kp.co[0]):
        #                 fc.keyframe_points.remove(kp)



        
        # [0].keyframe_points[0].interpolation

        # bpy.data.objects['Amt_C01'].pose.bones[1].keyframe_delete(data_path='rotation_quaternion',frame=10)
        # bpy.data.objects['Amt_C01'].pose.bones[1].keyframe_delete(data_path='location',frame=10)
        # bpy.data.objects['Amt_C01'].pose.bones[1].keyframe_delete(data_path='rotation_euler',frame=10)

        return{'FINISHED'}
    

class ExtractMarkedFramesForSelectedBones(Operator):
    bl_idname = "fdh.extract_marked_frames_for_selected_bones"
    bl_label = "Selected Bones"
    bl_description = "Extract Marked frames for Selected Bones"
    bl_options = {"REGISTER", "UNDO"}

    # option: IntProperty(name='',default=0) 

    def execute(self,context):
        fourd_prop = context.scene.fourd_prop

        # Pegar frames onde tem marcador
        markers = []
        for m in bpy.context.scene.timeline_markers:
            markers.append(m.frame)

        #pegar bones selecionados


        # apagar keyframes exceto dos que estao no "markers"
        # armature = context.scene.source
        armature = context.active_object

        frame_start = int(armature.animation_data.action.fcurves[0].range()[0])
        frame_end = int(armature.animation_data.action.fcurves[0].range()[1])

        slcted_bones = []
        for sb in context.selected_pose_bones:
            slcted_bones.append(sb.name)



        #nome do bone
        # bpy.data.objects['Amt_C01'].animation_data.action.fcurves[0].data_path.split('"')[1]
        fcurves = armature.animation_data.action.fcurves
        for f in range(frame_start,frame_end+1):
            for bone in context.selected_pose_bones:
                if f not in markers:
                    bone.keyframe_delete(data_path='rotation_quaternion',frame=f)
                    bone.keyframe_delete(data_path='location',frame=f)
                    bone.keyframe_delete(data_path='rotation_euler',frame=f)
                    bone.keyframe_delete(data_path='scale',frame=f)
                for fc in fcurves:
                    if bone.name == fc.data_path.split('"')[1]: #verifica se o nome do bone é o mesmo, para poder limpar o ik_switch
                        if fc.data_path.endswith('["ik_fk_switch"]'):
                            kpoints = fc.keyframe_points.values()
                            for kp in kpoints:
                                if f not in markers and f == int(kp.co[0]):
                                    fc.keyframe_points.remove(kp)


        #convertendo a interpolação para bezier
        for fc in armature.animation_data.action.fcurves:
            if fc.data_path.split('"')[1] in slcted_bones:
                print('bone to make bezier:',fc.data_path.split('"')[1])
                for kp in fc.keyframe_points:
                    kp.interpolation = 'BEZIER'
        
        # [0].keyframe_points[0].interpolation

        # bpy.data.objects['Amt_C01'].pose.bones[1].keyframe_delete(data_path='rotation_quaternion',frame=10)
        # bpy.data.objects['Amt_C01'].pose.bones[1].keyframe_delete(data_path='location',frame=10)
        # bpy.data.objects['Amt_C01'].pose.bones[1].keyframe_delete(data_path='rotation_euler',frame=10)

        return{'FINISHED'}


class ClearMarkers(Operator):
    bl_idname = "fdh.clear_markers"
    bl_label = "Clear Markers"
    bl_description = "Clear Markers"
    bl_options = {"REGISTER", "UNDO"}

    # option: IntProperty(name='',default=0) 

    def execute(self,context):
        # fourd_prop = context.scene.fourd_prop
        bpy.context.scene.timeline_markers.clear()

        return{'FINISHED'}

class OptimizeMarkerView(Operator):
    bl_idname = "fdh.optimize_marker_view"
    bl_label = "Optimize View"
    bl_description = "Optimize Marker View"
    bl_options = {"REGISTER", "UNDO"}

    # option: IntProperty(name='',default=0) 

    def execute(self,context):
        # fourd_prop = context.scene.fourd_prop
        context.active_object.data.display_type = 'STICK'
        context.active_object.show_in_front=True

        return{'FINISHED'}
    
class QuickSaveMarkers(Operator):
    bl_idname = "fdh.quick_save_markers"
    bl_label = "Quick Save Markers"
    bl_description = "Quick Save Markers"
    bl_options = {"REGISTER", "UNDO"}

    option: IntProperty(name='',default=1) #escolher qual "bank" salvar

    def execute(self,context):
        fourd_prop = context.scene.fourd_prop

        markers = []
        for m in bpy.context.scene.timeline_markers:
            markers.append([m.name,m.frame])
        if self.option == 1:
            fourd_prop.str_quick_save_marker1 = json.dumps(markers)
        elif self.option == 2:
            fourd_prop.str_quick_save_marker2 = json.dumps(markers)
        elif self.option == 3:
            fourd_prop.str_quick_save_marker3 = json.dumps(markers)
        elif self.option == 4:
            fourd_prop.str_quick_save_marker4 = json.dumps(markers)
        else:
            print('Bank limit')


        return{'FINISHED'}
    
class QuickLoadMarkers(Operator):
    bl_idname = "fdh.quick_load_markers"
    bl_label = "Quick Load Markers"
    bl_description = "Quick Load Markers"
    bl_options = {"REGISTER", "UNDO"}

    option: IntProperty(name='',default=1) #escolher qual "bank" salvar

    def execute(self,context):
        fourd_prop = context.scene.fourd_prop

        if self.option == 1:
            quick_load = json.loads(fourd_prop.str_quick_save_marker1)
        elif self.option == 2:
            quick_load = json.loads(fourd_prop.str_quick_save_marker2)
        elif self.option == 3:
            quick_load = json.loads(fourd_prop.str_quick_save_marker3)
        elif self.option == 4:
            quick_load = json.loads(fourd_prop.str_quick_save_marker4)
        else:
            print("No more banks")

        if fourd_prop.bool_clear_before_load_quickload:
            bpy.context.scene.timeline_markers.clear()

        for ql in quick_load:
            context.scene.timeline_markers.new(ql[0], frame=ql[1])
        
        return{'FINISHED'}
    
class QuickSaveMarkersClear(Operator):
    bl_idname = "fdh.quick_save_markers_clear"
    bl_label = "Clear Quick Save Markers"
    bl_description = "Clear Quick Save Markers"
    bl_options = {"REGISTER", "UNDO"}

    option: IntProperty(name='',default=0) #0 limpa todos

    def execute(self,context):
        fourd_prop = context.scene.fourd_prop

        if self.option == 0:
            fourd_prop.str_quick_save_marker1 = ''
            fourd_prop.str_quick_save_marker2 = ''
            fourd_prop.str_quick_save_marker3 = ''
            fourd_prop.str_quick_save_marker4 = ''

        elif self.option == 1:
            fourd_prop.str_quick_save_marker1 = ''
        elif self.option == 2:
            fourd_prop.str_quick_save_marker2 = ''
        elif self.option == 3:
            fourd_prop.str_quick_save_marker3 = ''
        elif self.option == 4:
            fourd_prop.str_quick_save_marker4 = ''
        else:
            print("No more banks")
        
        return{'FINISHED'}





class ChangeTargetRestPose(Operator):
    bl_idname = "fdh.change_target_rest_pose"
    bl_label = "Change target Rest Pose"
    bl_description = "Change target Rest Pose"
    bl_options = {"REGISTER", "UNDO"}

    # option: IntProperty(name='',default=0) 

    def execute(self,context):
        # fourd_prop = context.scene.fourd_prop
        armature = context.scene.target
        armature_mesh = context.scene.target_mesh
        

        return{'FINISHED'}
    
class ClearTgtMeshShapekeys(Operator):
    bl_idname = "fdh.clear_tgt_mesh_shapekeys"
    bl_label = "Clear Tgt Mesh Shapekeys"
    bl_description = "Clear Target Mesh Shapekeys"
    bl_options = {"REGISTER", "UNDO"}

    # option: IntProperty(name='',default=0) 

    def execute(self,context):
        # fourd_prop = context.scene.fourd_prop
        armature_mesh = context.scene.target_mesh
        armature_mesh.shape_key_clear()
        
        return{'FINISHED'}
    
class StartChangeRestTgtPose(Operator):
    bl_idname = "fdh.start_change_tgt_rest_pose"
    bl_label = "Start Change Pose"
    bl_description = "Start Chaging target Rest Pose"
    bl_options = {"REGISTER", "UNDO"}

    # option: IntProperty(name='',default=0) 

    def execute(self,context):
        # fourd_prop = context.scene.fourd_prop
        
        #forcando a ficar como objeto para poder escolher o target e colocar ele em pose mode
        if bpy.context.active_object.mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')

        bpy.ops.object.select_all(action='DESELECT')
        

        armature_source = context.scene.source
        armature_target = context.scene.target
        armature_source.data.pose_position = 'REST'
        armature_target.data.pose_position = 'POSE' #nao e possivel mudar a pose se POSE estiver como REST

        bpy.context.view_layer.objects.active = armature_target #estou selecionando o armature aqui para poder fazer o mode abaixo funcionar, caso o personagem nao esteja selecionado

        armature_target.show_in_front = True
        bpy.ops.object.mode_set(mode='POSE')

        armature_mesh = context.scene.target_mesh
        armature_mesh.shape_key_clear()
        return{'FINISHED'}
    
class EndChangeRestTgtPose(Operator):
    bl_idname = "fdh.end_change_tgt_rest_pose"
    bl_label = "End Change Pose"
    bl_description = "End Chaging target Rest Pose"
    bl_options = {"REGISTER", "UNDO"}

    # option: IntProperty(name='',default=0) 

    def execute(self,context):
        # fourd_prop = context.scene.fourd_prop
        armature_target = context.scene.target
        bpy.context.view_layer.objects.active = armature_target #estou selecionando o armature aqui para poder fazer o mode abaixo funcionar, caso o personagem nao esteja selecionado

        if bpy.context.active_object.mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')

        armature_mesh = context.scene.target_mesh
        mod_pos = None #colocando uma variavbel vasia para poder testar se houve a insercao de algo no loop do modifier
        for m,mod in enumerate(armature_mesh.modifiers):
            if mod.type == 'ARMATURE':
                mod_pos = m

        if mod_pos == None:
            mod_pos = 0
        mod_name = armature_mesh.modifiers[mod_pos].name
        mod_type = armature_mesh.modifiers[mod_pos].type
        mod_obj = armature_mesh.modifiers[mod_pos].object

        #aplicar modifier
        bpy.context.view_layer.objects.active = armature_mesh #estou selecionando o armature aqui para poder fazer o mode abaixo funcionar, caso o personagem nao esteja selecionado
        armature_mesh.select_set(1)
        bpy.ops.object.modifier_apply(modifier=mod_name)


        # aplicar bone rest position
        bpy.context.view_layer.objects.active = armature_target #estou selecionando o armature aqui para poder fazer o mode abaixo funcionar, caso o personagem nao esteja selecionado
        bpy.ops.object.mode_set(mode='POSE')
        bpy.ops.pose.armature_apply(selected=False) #transforma em rest pose


        #focar novamente no mesh
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.context.view_layer.objects.active = armature_mesh #estou selecionando o armature aqui para poder fazer o mode abaixo funcionar, caso o personagem nao esteja selecionado

        #criar novamente o modifier armature
        armature_mesh.modifiers.new(type=mod_type,name=mod_name)
        
        
        # mudar posicao a que ele estava anteriorment, posicao definida  pela variavel "mod_pos"
        #tenho que achar novamente onde o 
        for m,mod in enumerate(armature_mesh.modifiers):
            if mod.type == 'ARMATURE':
                mod_pos_new = m
                
        move_mod_up = mod_pos_new - mod_pos
        print('move_mod_up: ',move_mod_up)

        for i in range(move_mod_up):
            bpy.ops.object.modifier_move_up(modifier=mod_name)
            print('Modifier moved up')



        armature_mesh.modifiers[mod_pos].object = mod_obj

        bpy.ops.object.mode_set(mode='OBJECT')

        armature_source = context.scene.source
        armature_source.data.pose_position = 'POSE'

        armature_target.show_in_front = False

        return{'FINISHED'}

    
class StartChangeRestSourcePose(Operator):
    bl_idname = "fdh.start_change_source_rest_pose"
    bl_label = "Start Change Pose"
    bl_description = "Start Chaging Source Rest Pose"
    bl_options = {"REGISTER", "UNDO"}

    # option: IntProperty(name='',default=0) 

    def execute(self,context):
        

        # a ideia:
        # resetar a pose e deixar o usuario trocar a pose
        # adicionar um botão que vai guardar o dado da diferenca pra pose movida, para a rest pose
        # pegar essa diferenca e aplicar em todos os frames do source

        #identity matrix
        # identity = mathutils.Matrix()

        # # resetar para rest position:
        # l_knee = armature_source.pose.bones[3].rotation_quaternion.to_matrix()
        # armature_source.pose.bones[3].matrix_basis.identity()
        # identity = armature_source.pose.bones[3].rotation_quaternion.to_matrix()

        # id_lknee = identity - l_knee
        # armature_source.pose.bones[3].rotation_quaternion = id_lknee.to_quaternion()


        # armature_source.pose.bones['m_avg_L_Shoulder'].rotation_quaternion.to_matrix()

        armature_source = context.scene.source


        #colocando o esqueleto todo em rest pose
        for ap in armature_source.pose.bones:
            ap.matrix_basis.identity()

        # #guardando as rotacoes dos que foram modificados
        # new_rest_pose = []
        # for ap in armature_source.pose.bones:
        #     ap_name = ap.name
        #     ap_rotquat = ap.rotation_quaternion
        #     if ap.rotation_quaternion != mathutils.Quaternion():
        #         new_rest_pose.append([ap_name,ap_rotquat])


        


        # # fourd_prop = context.scene.fourd_prop
        
        # #forcando a ficar como objeto para poder escolher o target e colocar ele em pose mode
        # if bpy.context.active_object.mode != 'OBJECT':
        #     bpy.ops.object.mode_set(mode='OBJECT')

        # bpy.ops.object.select_all(action='DESELECT')
        

        # armature_source = context.scene.source
        # armature_target = context.scene.target
        # armature_source.data.pose_position = 'REST'
        # armature_target.data.pose_position = 'POSE' #nao e possivel mudar a pose se POSE estiver como REST

        # bpy.context.view_layer.objects.active = armature_target #estou selecionando o armature aqui para poder fazer o mode abaixo funcionar, caso o personagem nao esteja selecionado

        # armature_target.show_in_front = True
        # bpy.ops.object.mode_set(mode='POSE')

        bpy.context.view_layer.objects.active = armature_source #estou selecionando o armature aqui para poder fazer o mode abaixo funcionar, caso o personagem nao esteja selecionado
        if bpy.context.active_object.mode != 'POSE':
            bpy.ops.object.mode_set(mode='POSE')


        # armature_mesh = context.scene.target_mesh
        armature_mesh = armature_source.children[0]

        armature_mesh.shape_key_clear()
        return{'FINISHED'}
    
    
class EndChangeRestSourcePose(Operator):
    bl_idname = "fdh.end_change_source_rest_pose"
    bl_label = "End Change Pose"
    bl_description = "End Chaging Source Rest Pose"
    bl_options = {"REGISTER", "UNDO"}

    # option: IntProperty(name='',default=0) 

    def execute(self,context):
        # fourd_prop = context.scene.fourd_prop

        armature_source = context.scene.source



        #guardando as rotacoes dos que foram modificados
        new_rest_pose = []
        # new_rest_bones = []

        for ap in armature_source.pose.bones:
            ap_name = ap.name
            ap_rotquat = ap.rotation_quaternion
            if ap.rotation_quaternion != mathutils.Quaternion():
                new_rest_pose.append([ap_name,ap_rotquat])
                # new_rest_bones.append(ap_name)


        ##########################
        # f_start = context.scene.frame_start
        # f_end = context.scene.frame_end
        # for f in range(f_start,f_end+1):
        #     context.scene.frame_current = f
        #     bpy.context.view_layer.update()
        #     for ap in armature_source.pose.bones:
        #         for nb in new_rest_pose:
        #             if ap.name == nb[0]:
        #                 ap.rotation_quaternion = ap.rotation_quaternion + nb[1]
        #                 ap.keyframe_insert(data_path="rotation_quaternion" ,frame=f)
        #                 print(f,' 0-',ap.name,'-',nb[0])
        #                 # print(f,' 1-',ap.rotation_quaternion)
        #                 # print(f,' 2-',nb[1])

        #                 # rot_dif = ap.rotation_quaternion.rotation_difference(nb[1])
                        
        #                 # ap.rotation_quaternion = rot_dif
        #                 # print(f,' 3-',rot_dif)


        ##########################


        # armature_target = context.scene.target
        bpy.context.view_layer.objects.active = armature_source #estou selecionando o armature aqui para poder fazer o mode abaixo funcionar, caso o personagem nao esteja selecionado

        if bpy.context.active_object.mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')

        # armature_mesh = context.scene.target_mesh
        armature_mesh = armature_source.children[0]
        mod_pos = None #colocando uma variavbel vasia para poder testar se houve a insercao de algo no loop do modifier
        for m,mod in enumerate(armature_mesh.modifiers):
            if mod.type == 'ARMATURE':
                mod_pos = m

        if mod_pos == None:
            mod_pos = 0
        mod_name = armature_mesh.modifiers[mod_pos].name
        mod_type = armature_mesh.modifiers[mod_pos].type
        mod_obj = armature_mesh.modifiers[mod_pos].object

        #aplicar modifier
        bpy.context.view_layer.objects.active = armature_mesh #estou selecionando o armature aqui para poder fazer o mode abaixo funcionar, caso o personagem nao esteja selecionado
        armature_mesh.select_set(1)
        bpy.ops.object.modifier_apply(modifier=mod_name)


        # aplicar bone rest position
        bpy.context.view_layer.objects.active = armature_source #estou selecionando o armature aqui para poder fazer o mode abaixo funcionar, caso o personagem nao esteja selecionado
        bpy.ops.object.mode_set(mode='POSE')
        bpy.ops.pose.armature_apply(selected=False) #transforma em rest pose


        #focar novamente no mesh
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.context.view_layer.objects.active = armature_mesh #estou selecionando o armature aqui para poder fazer o mode abaixo funcionar, caso o personagem nao esteja selecionado

        #criar novamente o modifier armature
        armature_mesh.modifiers.new(type=mod_type,name=mod_name)
        
        
        # mudar posicao a que ele estava anteriorment, posicao definida  pela variavel "mod_pos"
        #tenho que achar novamente onde o 
        for m,mod in enumerate(armature_mesh.modifiers):
            if mod.type == 'ARMATURE':
                mod_pos_new = m
                
        move_mod_up = mod_pos_new - mod_pos
        print('move_mod_up: ',move_mod_up)

        for i in range(move_mod_up):
            bpy.ops.object.modifier_move_up(modifier=mod_name)
            print('Modifier moved up')

        armature_mesh.modifiers[mod_pos].object = mod_obj

        bpy.ops.object.mode_set(mode='OBJECT')

        # armature_source = context.scene.source
        # armature_source.data.pose_position = 'POSE'

        # armature_target.show_in_front = False

        return{'FINISHED'}
    
class Stg2Append(Operator):
    bl_idname = "fdh.append_stg2"
    bl_label = "Append STG2"
    bl_description = "Append STG2"
    bl_options = {"REGISTER", "UNDO"}

    # option: IntProperty(name='',default=0) 

    def execute(self,context):
        path_addon = os.path.dirname(os.path.abspath(__file__))

        tmp_obj = []

        for ob in bpy.data.objects:
            tmp_obj.append(ob.name)

        file_path = os.path.join(path_addon,'0_stg2_mixamo_rig.blend')
        inner_path = 'Collection'
        object_name = 'STG2'

        bpy.ops.wm.append(
            filepath=os.path.join(file_path, inner_path, object_name),
            directory=os.path.join(file_path, inner_path),
            filename=object_name
            )
        
        for ob in bpy.data.objects:
            if ob not in tmp_obj and ob.type == 'ARMATURE':
                stg2_armature = ob


        # bpy.ops.object.select_all(action='DESELECT')

        # stg2_armature.select_set(True)
        # bpy.context.view_layer.objects.active = stg2_armature
        
        context.scene.target_stg2 = stg2_armature





        return{'FINISHED'}



## Mixamo Rig Borrowed functions #########################
################## FUNCTIONS ##################

def set_pose_rotation(pose_bone, mat):
    q = mat.to_quaternion()

    if pose_bone.rotation_mode == 'QUATERNION':
        pose_bone.rotation_quaternion = q
    elif pose_bone.rotation_mode == 'AXIS_ANGLE':
        pose_bone.rotation_axis_angle[0] = q.angle
        pose_bone.rotation_axis_angle[1] = q.axis[0]
        pose_bone.rotation_axis_angle[2] = q.axis[1]
        pose_bone.rotation_axis_angle[3] = q.axis[2]
    else:
        pose_bone.rotation_euler = q.to_euler(pose_bone.rotation_mode)


def snap_pos(pose_bone, target_bone):
    # Snap a bone to another bone. Supports child of constraints and parent.

    # if the pose_bone has direct parent
    if pose_bone.parent:
        # apply double time because of dependecy lag
        pose_bone.matrix = target_bone.matrix
        update_transform()
        # second apply
        pose_bone.matrix = target_bone.matrix
    else:
        # is there a child of constraint attached?
        child_of_cns = None
        if len(pose_bone.constraints) > 0:
            all_child_of_cns = [i for i in pose_bone.constraints if i.type == "CHILD_OF" and i.influence == 1.0 and i.mute == False and i.target]
            if len(all_child_of_cns) > 0:
                child_of_cns = all_child_of_cns[0]# in case of multiple child of constraints enabled, use only the first for now

        if child_of_cns != None:
            if child_of_cns.subtarget != "" and get_pose_bone(child_of_cns.subtarget):
                # apply double time because of dependecy lag
                pose_bone.matrix = get_pose_bone(child_of_cns.subtarget).matrix_channel.inverted() @ target_bone.matrix
                update_transform()
                pose_bone.matrix = get_pose_bone(child_of_cns.subtarget).matrix_channel.inverted() @ target_bone.matrix
            else:
                pose_bone.matrix = target_bone.matrix

        else:
            pose_bone.matrix = target_bone.matrix


def snap_pos_matrix(pose_bone, target_bone_matrix):
    # Snap a bone to another bone. Supports child of constraints and parent.

    # if the pose_bone has direct parent
    if pose_bone.parent:
        pose_bone.matrix = target_bone_matrix.copy()
        update_transform()
    else:
        # is there a child of constraint attached?
        child_of_cns = None
        if len(pose_bone.constraints) > 0:
            all_child_of_cns = [i for i in pose_bone.constraints if i.type == "CHILD_OF" and i.influence == 1.0 and i.mute == False and i.target]
            if len(all_child_of_cns) > 0:
                child_of_cns = all_child_of_cns[0]# in case of multiple child of constraints enabled, use only the first for now

        if child_of_cns != None:
            if child_of_cns.subtarget != "" and get_pose_bone(child_of_cns.subtarget):
                pose_bone.matrix = get_pose_bone(child_of_cns.subtarget).matrix_channel.inverted() @ target_bone_matrix
                update_transform()
            else:
                pose_bone.matrix = target_bone_matrix.copy()

        else:
            pose_bone.matrix = target_bone_matrix.copy()


def snap_rot(pose_bone, target_bone):
    method = 1

    if method == 1:
        mat = get_pose_matrix_in_other_space(target_bone.matrix, pose_bone)
        set_pose_rotation(pose_bone, mat)
        #bpy.ops.object.mode_set(mode='OBJECT')
        #bpy.ops.object.mode_set(mode='POSE')
        bpy.context.view_layer.update()
    elif method == 2:
        loc, scale = pose_bone.location.copy(), pose_bone.scale.copy()
        pose_bone.matrix = target_bone.matrix
        pose_bone.location, pose_bone.scale = loc, scale
        bpy.context.view_layer.update()


def bake_fk_to_ik_arm(self):
    for f in range(self.frame_start, self.frame_end +1):
        bpy.context.scene.frame_set(f)
        print("baking frame", f)
        fk_to_ik_arm(self)


def fk_to_ik_arm(self):
    rig = self.rig
    side = self.side
    _side = self._side
    prefix = self.prefix

    arm_fk  = rig.pose.bones[fk_arm[0] + _side]
    forearm_fk  = rig.pose.bones[fk_arm[1] + _side]
    hand_fk  = rig.pose.bones[fk_arm[2] + _side]

    arm_ik = rig.pose.bones[ik_arm[0] + _side]
    forearm_ik = rig.pose.bones[ik_arm[1] + _side]
    hand_ik = rig.pose.bones[ik_arm[2] + _side]
    pole = rig.pose.bones[ik_arm[3] + _side]

    #Snap rot
    snap_rot(arm_fk, arm_ik)
    snap_rot(forearm_fk, forearm_ik)
    snap_rot(hand_fk, hand_ik)

    #Snap scale
    hand_fk.scale =hand_ik.scale

    #rot debug
    forearm_fk.rotation_euler[0]=0
    forearm_fk.rotation_euler[1]=0

    #switch
    #base_hand = get_pose_bone(prefix+side+'Hand')
    c_hand_ik = get_pose_bone(c_prefix+arm_rig_names["hand_ik"]+_side)
    c_hand_ik['ik_fk_switch'] = 1.0

    #udpate view    
    bpy.context.view_layer.update()

    #insert key if autokey enable
    if bpy.context.scene.tool_settings.use_keyframe_insert_auto:
        #fk chain
        c_hand_ik.keyframe_insert(data_path='["ik_fk_switch"]')
        hand_fk.keyframe_insert(data_path="scale")
        hand_fk.keyframe_insert(data_path="rotation_euler")
        arm_fk.keyframe_insert(data_path="rotation_euler")
        forearm_fk.keyframe_insert(data_path="rotation_euler")

        #ik chain
        hand_ik.keyframe_insert(data_path="location")
        hand_ik.keyframe_insert(data_path="rotation_euler")
        hand_ik.keyframe_insert(data_path="scale")
        pole.keyframe_insert(data_path="location")

    # change FK to IK hand selection, if selected
    if hand_ik.bone.select:
        hand_fk.bone.select = True
        hand_ik.bone.select = False


def bake_ik_to_fk_arm(self):
    for f in range(self.frame_start, self.frame_end +1):
        bpy.context.scene.frame_set(f)
        print("baking frame", f)

        ik_to_fk_arm(self)


def ik_to_fk_arm(self):
    rig = self.rig
    side = self.side
    _side = self._side
    prefix = self.prefix

    arm_fk  = rig.pose.bones[fk_arm[0] + _side]
    forearm_fk  = rig.pose.bones[fk_arm[1] + _side]
    hand_fk  = rig.pose.bones[fk_arm[2] + _side]

    arm_ik = rig.pose.bones[ik_arm[0] + _side]
    forearm_ik = rig.pose.bones[ik_arm[1] + _side]
    hand_ik = rig.pose.bones[ik_arm[2] + _side]
    pole_ik  = rig.pose.bones[ik_arm[3] + _side]

    # Snap
        # constraint support
    constraint = None
    bparent_name = ""
    parent_type = ""
    valid_constraint = True

    # Snap Hand
    if len(hand_ik.constraints) > 0:
        for c in hand_ik.constraints:
            if not c.mute and c.influence > 0.5 and c.type == 'CHILD_OF':
                if c.target:
                    #if bone
                    if c.target.type == 'ARMATURE':
                        bparent_name = c.subtarget
                        parent_type = "bone"
                        constraint = c
                    #if object
                    else:
                        bparent_name = c.target.name
                        parent_type = "object"
                        constraint = c


    if constraint != None:
        if parent_type == "bone":
            if bparent_name == "":
                valid_constraint = False

    if constraint and valid_constraint:
        if parent_type == "bone":
            bone_parent = get_pose_bone(bparent_name)
            hand_ik.matrix = bone_parent.matrix_channel.inverted() @ hand_fk.matrix
        if parent_type == "object":
            bone_parent = bpy.data.objects[bparent_name]
            obj_par = bpy.data.objects[bparent_name]
            hand_ik.matrix = constraint.inverse_matrix.inverted() @ obj_par.matrix_world.inverted() @ hand_fk.matrix
    else:
        hand_ik.matrix = hand_fk.matrix

    # Snap Pole
    _axis = forearm_fk.x_axis if side == "Left" else -forearm_fk.x_axis
    pole_pos = get_ik_pole_pos(arm_fk, forearm_fk, method=2, axis=_axis)
    pole_mat = Matrix.Translation(pole_pos)
    snap_pos_matrix(pole_ik, pole_mat)

    # Switch
    c_hand_ik = get_pose_bone(c_prefix+arm_rig_names["hand_ik"]+_side)
    #base_hand = get_pose_bone(prefix+side+'Hand')
    c_hand_ik['ik_fk_switch'] = 0.0

    # update
    update_transform()

     #insert key if autokey enable
    if bpy.context.scene.tool_settings.use_keyframe_insert_auto:
        #ik chain
        c_hand_ik.keyframe_insert(data_path='["ik_fk_switch"]')
        hand_ik.keyframe_insert(data_path="location")
        hand_ik.keyframe_insert(data_path="rotation_euler")
        hand_ik.keyframe_insert(data_path="scale")
        pole_ik.keyframe_insert(data_path="location")

        #fk chain
        hand_fk.keyframe_insert(data_path="location")
        hand_fk.keyframe_insert(data_path="rotation_euler")
        hand_fk.keyframe_insert(data_path="scale")
        arm_fk.keyframe_insert(data_path="rotation_euler")
        forearm_fk.keyframe_insert(data_path="rotation_euler")

    # change FK to IK hand selection, if selected
    if hand_fk.bone.select:
        hand_fk.bone.select = False
        hand_ik.bone.select = True


def bake_fk_to_ik_leg(self):
    for f in range(self.frame_start, self.frame_end +1):
        bpy.context.scene.frame_set(f)
        print("baking frame", f)

        fk_to_ik_leg(self)


def fk_to_ik_leg(self):
    rig = self.rig
    side = self.side
    _side = self._side
    prefix = self.prefix

    thigh_fk = rig.pose.bones[fk_leg[0] + _side]
    leg_fk = rig.pose.bones[fk_leg[1] + _side]
    foot_fk = rig.pose.bones[fk_leg[2] + _side]
    toes_fk = rig.pose.bones[fk_leg[3] + _side]

    thigh_ik = rig.pose.bones[ik_leg[0] + _side]
    leg_ik = rig.pose.bones[ik_leg[1] + _side]
    foot_ik = rig.pose.bones[ik_leg[2] + _side]
    pole_ik = rig.pose.bones[ik_leg[3] + _side]
    toes_ik = rig.pose.bones[ik_leg[4] + _side]
    foot_01_ik = rig.pose.bones[ik_leg[5] + _side]
    foot_roll_ik = rig.pose.bones[ik_leg[6] + _side]
    foot_snap_ik = rig.pose.bones[ik_leg[7] + _side]

    # Thigh snap
    snap_rot(thigh_fk, thigh_ik)
    #thigh_fk.matrix = thigh_ik.matrix.copy()

    # Leg snap
    snap_rot(leg_fk, leg_ik)

    # Foot snap
    snap_rot(foot_fk, foot_snap_ik)
    foot_fk.scale =foot_ik.scale

    # Toes snap
    snap_rot(toes_fk, toes_ik)
    toes_fk.scale = toes_ik.scale

    # rotation fix
    leg_fk.rotation_euler[1] = 0.0
    leg_fk.rotation_euler[2] = 0.0

    # switch prop value
    c_foot_ik = get_pose_bone(c_prefix+leg_rig_names["foot_ik"]+_side)
    #base_foot = get_pose_bone(prefix+side+'Foot')
    c_foot_ik['ik_fk_switch'] = 1.0

    # udpate hack  
    bpy.context.view_layer.update()

    #if bpy.context.scene.frame_current == 2:
    #    print(br)

    #insert key if autokey enable
    if bpy.context.scene.tool_settings.use_keyframe_insert_auto:
        #fk chain
        c_foot_ik.keyframe_insert(data_path='["ik_fk_switch"]')
        thigh_fk.keyframe_insert(data_path="rotation_euler")
        leg_fk.keyframe_insert(data_path="rotation_euler")
        foot_fk.keyframe_insert(data_path="rotation_euler")
        foot_fk.keyframe_insert(data_path="scale")
        toes_fk.keyframe_insert(data_path="rotation_euler")
        toes_fk.keyframe_insert(data_path="scale")

        #ik chain
        foot_ik.keyframe_insert(data_path="location")
        foot_ik.keyframe_insert(data_path="rotation_euler")
        foot_ik.keyframe_insert(data_path="scale")
        foot_01_ik.keyframe_insert(data_path="rotation_euler")
        foot_roll_ik.keyframe_insert(data_path="location")
        toes_ik.keyframe_insert(data_path="rotation_euler")
        toes_ik.keyframe_insert(data_path="scale")
        pole_ik.keyframe_insert(data_path="location")

    # change IK to FK foot selection, if selected
    if foot_ik.bone.select:
        foot_fk.bone.select = True
        foot_ik.bone.select = False


def bake_ik_to_fk_leg(self):
    for f in range(self.frame_start, self.frame_end +1):
        bpy.context.scene.frame_set(f)
        print("baking frame", f)

        ik_to_fk_leg(self)


def ik_to_fk_leg(self):
    rig = self.rig
    side = self.side
    _side = self._side
    prefix = self.prefix

    thigh_fk = rig.pose.bones[fk_leg[0] + _side]
    leg_fk = rig.pose.bones[fk_leg[1] + _side]
    foot_fk = rig.pose.bones[fk_leg[2] + _side]
    toes_fk = rig.pose.bones[fk_leg[3] + _side]

    thigh_ik = rig.pose.bones[ik_leg[0] + _side]
    calf_ik = rig.pose.bones[ik_leg[1] + _side]
    foot_ik = rig.pose.bones[ik_leg[2] + _side]
    pole_ik = rig.pose.bones[ik_leg[3] + _side]
    toes_ik = rig.pose.bones[ik_leg[4] + _side]
    foot_01_ik = rig.pose.bones[ik_leg[5] + _side]
    foot_roll_ik = rig.pose.bones[ik_leg[6] + _side]


    # reset IK foot_01 and foot_roll
    foot_01_ik.rotation_euler = [0,0,0]
    foot_roll_ik.location[0] = 0.0
    foot_roll_ik.location[2] = 0.0

    # Snap toes
    toes_ik.rotation_euler = toes_fk.rotation_euler.copy()
    toes_ik.scale = toes_fk.scale.copy()

    # Child Of constraint or parent cases
    constraint = None
    bparent_name = ""
    parent_type = ""
    valid_constraint = True

    if len(foot_ik.constraints) > 0:
        for c in foot_ik.constraints:
            if not c.mute and c.influence > 0.5 and c.type == 'CHILD_OF':
                if c.target:
                    #if bone
                    if c.target.type == 'ARMATURE':
                        bparent_name = c.subtarget
                        parent_type = "bone"
                        constraint = c
                    #if object
                    else:
                        bparent_name = c.target.name
                        parent_type = "object"
                        constraint = c

    if constraint != None:
        if parent_type == "bone":
            if bparent_name == "":
                valid_constraint = False

    # Snap Foot
    if constraint and valid_constraint:
        if parent_type == "bone":
            bone_parent = rig.pose.bones[bparent_name]
            foot_ik.matrix = bone_parent.matrix_channel.inverted() @ foot_fk.matrix
        if parent_type == "object":
            ob = bpy.data.objects[bparent_name]
            foot_ik.matrix = constraint.inverse_matrix.inverted() @ ob.matrix_world.inverted() @ foot_fk.matrix

    else:
        foot_ik.matrix = foot_fk.matrix

    # update
    bpy.context.view_layer.update()

    # Snap Pole
    pole_pos = get_ik_pole_pos(thigh_fk, leg_fk, method=2, axis=leg_fk.z_axis)
    pole_mat = Matrix.Translation(pole_pos)
    snap_pos_matrix(pole_ik, pole_mat)

    update_transform()

    # switch
    c_foot_ik = get_pose_bone(c_prefix+leg_rig_names["foot_ik"]+_side)
    #base_foot = get_pose_bone(prefix+side+'Foot')
    c_foot_ik['ik_fk_switch'] = 0.0

    update_transform()

    #insert key if autokey enable
    if bpy.context.scene.tool_settings.use_keyframe_insert_auto:
        #ik chain
        c_foot_ik.keyframe_insert(data_path='["ik_fk_switch"]')
        foot_01_ik.keyframe_insert(data_path="rotation_euler")
        foot_roll_ik.keyframe_insert(data_path="location")
        foot_ik.keyframe_insert(data_path="location")
        foot_ik.keyframe_insert(data_path="rotation_euler")
        foot_ik.keyframe_insert(data_path="scale")
        toes_ik.keyframe_insert(data_path="rotation_euler")
        toes_ik.keyframe_insert(data_path="scale")
        pole_ik.keyframe_insert(data_path="location")

        #fk chain
        thigh_fk.keyframe_insert(data_path="rotation_euler")
        leg_fk.keyframe_insert(data_path="rotation_euler")
        foot_fk.keyframe_insert(data_path="rotation_euler")
        foot_fk.keyframe_insert(data_path="scale")
        toes_fk.keyframe_insert(data_path="rotation_euler")
        toes_fk.keyframe_insert(data_path="scale")

    # change IK to FK foot selection, if selected
    if foot_fk.bone.select:
        foot_fk.bone.select = False
        foot_ik.bone.select = True


def get_active_child_of_cns(bone):
    constraint = None
    bparent_name = ""
    parent_type = ""
    valid_constraint = True

    if len(bone.constraints) > 0:
        for c in bone.constraints:
            if not c.mute and c.influence > 0.5 and c.type == 'CHILD_OF':
                if c.target:
                    if c.target.type == 'ARMATURE':# bone
                        bparent_name = c.subtarget
                        parent_type = "bone"
                        constraint = c
                    else:# object
                        bparent_name = c.target.name
                        parent_type = "object"
                        constraint = c

    if constraint:
        if parent_type == "bone":
            if bparent_name == "":
                valid_constraint = False

    return constraint, bparent_name, parent_type, valid_constraint


def is_selected(names, selected_bone_name, startswith=False):
    side = ""
    if get_bone_side(selected_bone_name) != None:
       side = get_bone_side(selected_bone_name)

    _side = "_"+side

    if startswith == False:
        if type(names) == list:
            for name in names:
                if not "." in name[-2:]:
                    if name + _side == selected_bone_name:
                        return True
                else:
                    if name[-2:] == ".x":
                        if name[:-2] + _side == selected_bone_name:
                            return True
        elif names == selected_bone_name:
            return True
    else:#startswith
        if type(names) == list:
            for name in names:
                if selected_bone_name.startswith(name):
                    return True
        else:
            return selected_bone_name.startswith(names)
    return False


def is_selected_prop(pbone, prop_name):
    if pbone.bone.keys():
        if prop_name in pbone.bone.keys():
            return True




#### Bones Pose ###############

def get_custom_shape_scale(pbone, uniform=True):    
    if blender_version._float >= 300:
        if uniform:       
            # uniform scale
            val = 0
            for i in range(0,3):
                val += pbone.custom_shape_scale_xyz[i]
            return val/3     
        # array scale
        else:
            return pbone.custom_shape_scale_xyz
    # pre-Blender 3.0
    else:        
        return pbone.custom_shape_scale
        

def get_selected_pbone_name():
    try:
        return bpy.context.selected_pose_bones[0].name#.active_pose_bone.name
    except:
        return
        
        
def get_pose_bone(name):
    return bpy.context.active_object.pose.bones.get(name)
    
    
def lock_pbone_transform(pbone, type, list):    
    for i in list:
        if type == "location":
            pbone.lock_location[i] = True
        elif type == "rotation":     
            pbone.lock_rotation[i] = True
        elif type == "scale":      
            pbone.lock_scale[i] = True


def set_bone_custom_shape(pbone, cs_name):
    cs = get_object(cs_name)
    if cs == None:
        append_cs(cs_name)
        cs = get_object(cs_name)

    pbone.custom_shape = cs


def set_bone_color_group(obj, pb, grp_name):
    # mixamo required color
    orange = (0.969, 0.565, 0.208)
    orange_light = (0.957, 0.659, 0.416)
    blue_dark = (0.447, 0.682, 1.0)
    blue_light = (0.365, 0.851, 1.0)
    
    # base color
    green = (0.0, 1.0, 0.0)
    red = (1.0, 0.0, 0.0)
    blue = (0.0, 0.9, 1.0)
    
    grp_color_master = orange_light
    grp_color_neck = orange_light
    grp_color_root_master = orange
    grp_color_head = orange
    grp_color_body_mid = green
    grp_color_body_left = blue_dark
    grp_color_body_right = blue_light

    grp = obj.pose.bone_groups.get(grp_name)
    if grp == None:
        grp = obj.pose.bone_groups.new(name=grp_name)
        grp.color_set = 'CUSTOM'

        grp_color = None
        if grp_name == "body_mid":
            grp_color = grp_color_body_mid
        elif grp_name == "body_left":
            grp_color = grp_color_body_left
        elif grp_name == "body_right":
            grp_color = grp_color_body_right
        elif grp_name == "master":
            grp_color = grp_color_master
        elif grp_name == "neck":
            grp_color = grp_color_head
        elif grp_name == "head":
            grp_color = grp_color_neck
        elif grp_name == "root_master":
            grp_color = grp_color_root_master

        # set normal color
        grp.colors.normal = grp_color
        
        # set select color/active color
        for col_idx in range(0,3):
            grp.colors.select[col_idx] = grp_color[col_idx] + 0.2
            grp.colors.active[col_idx] = grp_color[col_idx] + 0.4

    pb.bone_group = grp
    
    
def update_transform():
    bpy.ops.transform.rotate(value=0, orient_axis='Z', orient_type='VIEW', orient_matrix=((0.0, 0.0, 0), (0, 0.0, 0.0), (0.0, 0.0, 0.0)), orient_matrix_type='VIEW', mirror=False)

######################

############### mixamo.py ##################

def get_mixamo_prefix():    
    p = ""
    rig = bpy.context.active_object    
    
    if 'mixamo_prefix' in rig.data.keys():
        p = rig.data["mixamo_prefix"]
        
    else:     
        for dbone in rig.data.bones:
            if dbone.name.startswith("mixamorig") and ':' in dbone.name:
                p = dbone.name.split(':')[0]+':'
                break
        
        try:
            rig.data["mixamo_prefix"] = p
        except:# context error
            pass
    
    return p
    
    
def get_mix_name(name, use_prefix):
    if not use_prefix:
        return name
    else:        
        p = get_mixamo_prefix()
        return p+name
            
            
def get_bone_side(bone_name):
    if bone_name.endswith("_Left"):
        return "Left"
    elif bone_name.endswith("_Right"):
        return "Right"
############################

################ Naming.py
# control rig
c_prefix = "Ctrl_"
master_rig_names = {"master":"Master"}
spine_rig_names = {"pelvis":"Hips", "spine1":"Spine", "spine2":"Spine1", "spine3":"Spine2", "hips_free":"Hips_Free", "hips_free_helper":"Hips_Free_Helper"}
head_rig_names = {"neck":"Neck", "head":"Head"}
leg_rig_names = {"thigh_ik":"UpLeg_IK", "thigh_fk":"UpLeg_FK", "calf_ik":"Leg_IK", "calf_fk":"Leg_FK", "foot_fk":"Foot_FK", "foot_ik":"Foot_IK", "foot_snap":"Foot_Snap", "foot_ik_target":"Foot_IK_target", "foot_01":"Foot_01", "foot_01_pole":"Foot_01_Pole", "heel_out":"FootHeelOut", "heel_in":"FootHeelIn", "heel_mid":"FootHeelMid", "toes_end":"ToeEnd", "toes_end_01":"ToeEnd_01", "toes_ik":"Toe_IK", "toes_track":"ToeTrack", "toes_01_ik":"Toe01_IK", "toes_02":"Toe02", "toes_fk":"Toe_FK", "foot_roll_cursor":"FootRoll_Cursor", "pole_ik":"LegPole_IK"}
arm_rig_names = {"shoulder":"Shoulder", "arm_ik":"Arm_IK", "arm_fk":"Arm_FK", "forearm_ik":"ForeArm_IK", "forearm_fk":"ForeArm_FK", "pole_ik":"ArmPole_IK", "hand_ik":"Hand_IK", "hand_fk":"Hand_FK"}

# mixamo bone names
spine_names = {"pelvis":"Hips", "spine1":"Spine", "spine2":"Spine1", "spine3":"Spine2"}
head_names = {"neck":"Neck", "head":"Head", "head_end":"HeadTop_End"}
leg_names = {"thigh":"UpLeg", "calf":"Leg", "foot":"Foot", "toes":"ToeBase", "toes_end":"Toe_End"}
arm_names = {"shoulder":"Shoulder", "arm":"Arm", "forearm":"ForeArm", "hand":"Hand"}
fingers_type = ["Thumb", "Index", "Middle", "Ring", "Pinky"]

####################

##### Maths_geo.py

def mat3_to_vec_roll(mat):
    vec = mat.col[1]
    vecmat = vec_roll_to_mat3(mat.col[1], 0)
    vecmatinv = vecmat.inverted()
    rollmat = vecmatinv @ mat
    roll = atan2(rollmat[0][2], rollmat[2][2])
    return roll


def vec_roll_to_mat3(vec, roll):
    target = Vector((0, 0.1, 0))
    nor = vec.normalized()
    axis = target.cross(nor)
    if axis.dot(axis) > 0.0000000001: # this seems to be the problem for some bones, no idea how to fix
        axis.normalize()
        theta = target.angle(nor)
        bMatrix = Matrix.Rotation(theta, 3, axis)
    else:
        updown = 1 if target.dot(nor) > 0 else -1
        bMatrix = Matrix.Scale(updown, 3)
        bMatrix[2][2] = 1.0

    rMatrix = Matrix.Rotation(roll, 3, nor)
    mat = rMatrix @ bMatrix
    return mat


def align_bone_x_axis(edit_bone, new_x_axis):
    new_x_axis = new_x_axis.cross(edit_bone.y_axis)
    new_x_axis.normalize()
    dot = max(-1.0, min(1.0, edit_bone.z_axis.dot(new_x_axis)))
    angle = acos(dot)
    edit_bone.roll += angle
    dot1 = edit_bone.z_axis.dot(new_x_axis)
    edit_bone.roll -= angle * 2.0
    dot2 = edit_bone.z_axis.dot(new_x_axis)
    if dot1 > dot2:
        edit_bone.roll += angle * 2.0


def align_bone_z_axis(edit_bone, new_z_axis):
    new_z_axis = -(new_z_axis.cross(edit_bone.y_axis))
    new_z_axis.normalize()
    dot = max(-1.0, min(1.0, edit_bone.x_axis.dot(new_z_axis)))
    angle = acos(dot)
    edit_bone.roll += angle
    dot1 = edit_bone.x_axis.dot(new_z_axis)
    edit_bone.roll -= angle * 2.0
    dot2 = edit_bone.x_axis.dot(new_z_axis)
    if dot1 > dot2:
        edit_bone.roll += angle * 2.0


def signed_angle(u, v, normal):
    nor = normal.normalized()
    a = u.angle(v)    
    
    c = u.cross(v)
    
    if c.magnitude == 0.0:
        c = u.normalized().cross(v)
    if c.magnitude == 0.0:
        return 0.0
        
    if c.angle(nor) < 1:
        a = -a
    return a


def project_point_onto_plane(q, p, n):
    n = n.normalized()
    return q - ((q - p).dot(n)) * n


def get_pole_angle(base_bone, ik_bone, pole_location):
    pole_normal = (ik_bone.tail - base_bone.head).cross(pole_location - base_bone.head)
    projected_pole_axis = pole_normal.cross(base_bone.tail - base_bone.head)
    return signed_angle(base_bone.x_axis, projected_pole_axis, base_bone.tail - base_bone.head)
    
    
def get_pose_matrix_in_other_space(mat, pose_bone):
    rest = pose_bone.bone.matrix_local.copy()
    rest_inv = rest.inverted()

    if pose_bone.parent and pose_bone.bone.use_inherit_rotation:
        par_mat = pose_bone.parent.matrix.copy()
        par_inv = par_mat.inverted()
        par_rest = pose_bone.parent.bone.matrix_local.copy()

    else:
        par_mat = Matrix()
        par_inv = Matrix()
        par_rest = Matrix()

    smat = rest_inv @ (par_rest @ (par_inv @ mat))

    return smat


def get_ik_pole_pos(b1, b2, method=1, axis=None): 
   
    if method == 1:
        # IK pole position based on real IK bones vector
        plane_normal = (b1.head - b2.tail)
        midpoint = (b1.head + b2.tail) * 0.5
        prepole_dir = b2.head - midpoint#prepole_fk.tail - prepole_fk.head
        pole_pos = b2.head + prepole_dir.normalized()# * 4
        pole_pos = project_point_onto_plane(pole_pos, b2.head, plane_normal)
        pole_pos = b2.head + ((pole_pos - b2.head).normalized() * (b2.head - b1.head).magnitude * 1.7)
        
    elif method == 2:    
        # IK pole position based on bone2 Z axis vector      
        pole_pos = b2.head + (axis.normalized() * (b2.tail-b2.head).magnitude)
    
    return pole_pos
    
    
def rotate_point(point, angle, origin, axis):
    rot_mat = Matrix.Rotation(angle, 4, axis.normalized())
    # rotate in world origin space
    offset_vec = -origin
    offset_knee = point + offset_vec
    # rotate
    rotated_point = rot_mat @ offset_knee
    # bring back to original space
    rotated_point = rotated_point -offset_vec
    return rotated_point
    
    
def dot_product(x, y):
    return sum([x[i] * y[i] for i in range(len(x))])

    
def norm(x):
    return sqrt(dot_product(x, x))

    
def normalize(x):
    return [x[i] / norm(x) for i in range(len(x))]

    
def project_vector_onto_plane(x, n):
    d = dot_product(x, n) / norm(n)
    p = [d * normalize(n)[i] for i in range(len(n))]
    vec_list = [x[i] - p[i] for i in range(len(x))]
    return Vector((vec_list[0], vec_list[1], vec_list[2]))
    
#############################

fk_leg = [c_prefix+leg_rig_names["thigh_fk"], c_prefix+leg_rig_names["calf_fk"], c_prefix+leg_rig_names["foot_fk"], c_prefix+leg_rig_names["toes_fk"]]
ik_leg = [leg_rig_names["thigh_ik"], leg_rig_names["calf_ik"], c_prefix+leg_rig_names["foot_ik"], c_prefix+leg_rig_names["pole_ik"], c_prefix+leg_rig_names["toes_ik"], c_prefix+leg_rig_names["foot_01"], c_prefix+leg_rig_names["foot_roll_cursor"], leg_rig_names["foot_snap"]]
fk_arm = [c_prefix+arm_rig_names["arm_fk"], c_prefix+arm_rig_names["forearm_fk"], c_prefix+arm_rig_names["hand_fk"]]
ik_arm = [arm_rig_names["arm_ik"], arm_rig_names["forearm_ik"], c_prefix+arm_rig_names["hand_ik"], c_prefix+arm_rig_names["pole_ik"]]


def switch_ik_fk_anim(self,context,bones):

    armature = context.scene.target_stg2
    armature.select_set(True)
    bpy.context.view_layer.objects.active = armature

    if bpy.context.active_object.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')
    
    bpy.ops.object.select_all(action='DESELECT')

    # armature.select_set(True)
    # bpy.context.view_layer.objects.active = armature
    if bpy.context.active_object.mode != 'POSE':
        bpy.ops.object.mode_set(mode='POSE')


    action = context.active_object.animation_data.action
    self.frame_start, self.frame_end = int(action.frame_range[0]), int(action.frame_range[1])

    try:
        scn = context.scene
        # save current autokey state
        auto_key_state = scn.tool_settings.use_keyframe_insert_auto
        # set auto key to True
        scn.tool_settings.use_keyframe_insert_auto = True
        # save current frame
        cur_frame = scn.frame_current

        # self.rig = context.active_object
        self.rig = armature
        # bones = ['Ctrl_Hand_FK_Left','Ctrl_Hand_FK_Right','Ctrl_Foot_FK_Left','Ctrl_Foot_FK_Right']



        for bname in bones:
            # bname = get_selected_pbone_name()
            self.side = get_bone_side(bname)
            self._side = '_'+self.side
            self.prefix = get_mixamo_prefix()


            if is_selected(fk_leg, bname) or is_selected(ik_leg, bname):
                self.type = "LEG"
            elif is_selected(fk_arm, bname) or is_selected(ik_arm, bname):
                self.type = "ARM"

            if self.type == "ARM":
                c_hand_ik = get_pose_bone(c_prefix+arm_rig_names["hand_ik"]+self._side)#self.prefix+self.side+'Hand')
                if c_hand_ik['ik_fk_switch'] < 0.5:
                    bake_fk_to_ik_arm(self)
                else:
                    bake_ik_to_fk_arm(self)

            elif self.type == "LEG":
                c_foot_ik = get_pose_bone(c_prefix+leg_rig_names["foot_ik"]+self._side)#get_pose_bone(self.prefix+self.side+'Foot')
                if c_foot_ik['ik_fk_switch'] < 0.5:
                    bake_fk_to_ik_leg(self)
                else:
                    print("Bake IK to FK leg")
                    bake_ik_to_fk_leg(self)


    finally:
        # restore autokey state
        scn.tool_settings.use_keyframe_insert_auto = auto_key_state
        # restore frame
        scn.frame_set(cur_frame)

class MR_switch_snap_anim(bpy.types.Operator):
    """Switch and snap IK-FK over multiple frames"""

    bl_idname = "fdh.mr_switch_snap_anim"
    bl_label = "Switch and Snap IK FK anim"
    bl_options = {'UNDO'}

    rig = None
    side : bpy.props.StringProperty(name="bone side", default="")
    _side = ""
    prefix: bpy.props.StringProperty(name="", default="")
    type : bpy.props.StringProperty(name="type", default="")

    frame_start : bpy.props.IntProperty(name="Frame start", default=0)
    frame_end : bpy.props.IntProperty(name="Frame end", default=10)
    has_action = False
    
    
    # @classmethod
    # def poll(cls, context): #faz com que o botao fiue ativo apena quando estiver na condicao abaixo
    #     return (context.active_object != None and context.mode == 'POSE')
        

    # def draw(self, context):
    #     layout = self.layout
    #     if self.has_action:
    #         layout.prop(self, 'frame_start', text='Frame Start')
    #         layout.prop(self, 'frame_end', text='Frame End')
    #     else:
    #         layout.label(text="This rig is not animated!")
        

    # def invoke(self, context, event):
    #     try:
    #         action = context.active_object.animation_data.action
    #         if action:
    #             self.has_action = True
    #     except:
    #         pass
            
    #     if self.has_action:
    #         self.frame_start, self.frame_end = int(action.frame_range[0]), int(action.frame_range[1])
            
    #     wm = context.window_manager        
    #     return wm.invoke_props_dialog(self, width=400)
        

    def execute(self, context):
        bones = ['Ctrl_Hand_FK_Left','Ctrl_Hand_FK_Right','Ctrl_Foot_FK_Left','Ctrl_Foot_FK_Right']

        switch_ik_fk_anim(self,context,bones)

        # # if self.has_action == False:
        # #     return {'FINISHED'}

        # armature = context.scene.target
        # bpy.ops.object.select_all(action='DESELECT')

        # armature.select_set(True)
        # bpy.context.view_layer.objects.active = armature
        # if bpy.context.active_object.mode != 'POSE':
        #     bpy.ops.object.mode_set(mode='POSE')


        # action = context.active_object.animation_data.action
        # self.frame_start, self.frame_end = int(action.frame_range[0]), int(action.frame_range[1])
    
        # try:
        #     scn = context.scene
        #     # save current autokey state
        #     auto_key_state = scn.tool_settings.use_keyframe_insert_auto
        #     # set auto key to True
        #     scn.tool_settings.use_keyframe_insert_auto = True
        #     # save current frame
        #     cur_frame = scn.frame_current

        #     # self.rig = context.active_object
        #     self.rig = armature
        #     bones = ['Ctrl_Hand_FK_Left','Ctrl_Hand_FK_Right','Ctrl_Foot_FK_Left','Ctrl_Foot_FK_Right']



        #     for bname in bones:
        #         # bname = get_selected_pbone_name()
        #         self.side = get_bone_side(bname)
        #         self._side = '_'+self.side
        #         self.prefix = get_mixamo_prefix()


        #         if is_selected(fk_leg, bname) or is_selected(ik_leg, bname):
        #             self.type = "LEG"
        #         elif is_selected(fk_arm, bname) or is_selected(ik_arm, bname):
        #             self.type = "ARM"

        #         if self.type == "ARM":
        #             c_hand_ik = get_pose_bone(c_prefix+arm_rig_names["hand_ik"]+self._side)#self.prefix+self.side+'Hand')
        #             if c_hand_ik['ik_fk_switch'] < 0.5:
        #                 bake_fk_to_ik_arm(self)
        #             else:
        #                 bake_ik_to_fk_arm(self)

        #         elif self.type == "LEG":
        #             c_foot_ik = get_pose_bone(c_prefix+leg_rig_names["foot_ik"]+self._side)#get_pose_bone(self.prefix+self.side+'Foot')
        #             if c_foot_ik['ik_fk_switch'] < 0.5:
        #                 bake_fk_to_ik_leg(self)
        #             else:
        #                 print("Bake IK to FK leg")
        #                 bake_ik_to_fk_leg(self)


        # finally:
        #     # restore autokey state
        #     scn.tool_settings.use_keyframe_insert_auto = auto_key_state
        #     # restore frame
        #     scn.frame_set(cur_frame)

        return {'FINISHED'}


class Stg2retarget(Operator):
    bl_idname = "fdh.stg2_retarget"
    bl_label = "STG2 retarget"
    bl_description = "STG2 Retarget"
    bl_options = {"REGISTER", "UNDO"}

    # option: IntProperty(name='',default=0) 

    def execute(self,context):
        # path_addon = os.path.dirname(os.path.abspath(__file__))
        rig = [
                ["m_avg_root",""],
                ["m_avg_Pelvis","Ctrl_Hips"],
                ["m_avg_L_Hip","Ctrl_UpLeg_FK_Left"],
                ["m_avg_L_Knee","Ctrl_Leg_FK_Left"],
                ["m_avg_L_Ankle","Ctrl_Foot_FK_Left"],
                ["m_avg_L_Foot","Ctrl_Toe_FK_Left"],
                ["m_avg_R_Hip","Ctrl_UpLeg_FK_Right"],
                ["m_avg_R_Knee","Ctrl_Leg_FK_Right"],
                ["m_avg_R_Ankle","Ctrl_Foot_FK_Right"],
                ["m_avg_R_Foot","Ctrl_Toe_FK_Right"],
                ["m_avg_Spine1","Ctrl_Spine"],
                ["m_avg_Spine2","Ctrl_Spine1"],
                ["m_avg_Spine3","Ctrl_Spine2"],
                ["m_avg_Neck","Ctrl_Neck"],
                ["m_avg_Head","Ctrl_Head"],
                ["m_avg_L_Collar","Ctrl_Shoulder_Left"],
                ["m_avg_L_Shoulder","Ctrl_Arm_FK_Left"],
                ["m_avg_L_Elbow","Ctrl_ForeArm_FK_Left"],
                ["m_avg_L_Wrist","Ctrl_Hand_FK_Left"],
                ["m_avg_L_Hand",""],
                ["m_avg_R_Collar","Ctrl_Shoulder_Right"],
                ["m_avg_R_Shoulder","Ctrl_Arm_FK_Right"],
                ["m_avg_R_Elbow","Ctrl_ForeArm_FK_Right"],
                ["m_avg_R_Wrist","Ctrl_Hand_FK_Right"],
                ["m_avg_R_Hand",""]
                ]
        target = 'stg2'
        
        bind(context,rig,target)
        retarget(context,target)
        return{'FINISHED'}
    

class Stg2Full(Operator):
    bl_idname = "fdh.stg2_full"
    bl_label = "IK Control"
    bl_description = "STG2 IK Control"
    bl_options = {"REGISTER", "UNDO"}

    # option: IntProperty(name='',default=0) 
    rig = None
    side : bpy.props.StringProperty(name="bone side", default="")
    _side = ""
    prefix: bpy.props.StringProperty(name="", default="")
    type : bpy.props.StringProperty(name="type", default="")

    frame_start : bpy.props.IntProperty(name="Frame start", default=0)
    frame_end : bpy.props.IntProperty(name="Frame end", default=10)
    has_action = False

    def execute(self,context):
        #### Append ####
        path_addon = os.path.dirname(os.path.abspath(__file__))

        tmp_obj = []

        for ob in bpy.data.objects:
            tmp_obj.append(ob.name)

        file_path = os.path.join(path_addon,'0_stg2_mixamo_rig.blend')
        inner_path = 'Collection'
        object_name = 'STG2'

        bpy.ops.wm.append(
            filepath=os.path.join(file_path, inner_path, object_name),
            directory=os.path.join(file_path, inner_path),
            filename=object_name
            )
        
        for ob in bpy.data.objects:
            if ob not in tmp_obj and ob.type == 'ARMATURE' and ob.name.startswith('STG2_Armature'):
                stg2_armature = ob
        
        context.scene.target_stg2 = stg2_armature
        


        ###### Retarget ########
        rig = [
                ["m_avg_root",""],
                ["m_avg_Pelvis","Ctrl_Hips"],
                ["m_avg_L_Hip","Ctrl_UpLeg_FK_Left"],
                ["m_avg_L_Knee","Ctrl_Leg_FK_Left"],
                ["m_avg_L_Ankle","Ctrl_Foot_FK_Left"],
                ["m_avg_L_Foot","Ctrl_Toe_FK_Left"],
                ["m_avg_R_Hip","Ctrl_UpLeg_FK_Right"],
                ["m_avg_R_Knee","Ctrl_Leg_FK_Right"],
                ["m_avg_R_Ankle","Ctrl_Foot_FK_Right"],
                ["m_avg_R_Foot","Ctrl_Toe_FK_Right"],
                ["m_avg_Spine1","Ctrl_Spine"],
                ["m_avg_Spine2","Ctrl_Spine1"],
                ["m_avg_Spine3","Ctrl_Spine2"],
                ["m_avg_Neck","Ctrl_Neck"],
                ["m_avg_Head","Ctrl_Head"],
                ["m_avg_L_Collar","Ctrl_Shoulder_Left"],
                ["m_avg_L_Shoulder","Ctrl_Arm_FK_Left"],
                ["m_avg_L_Elbow","Ctrl_ForeArm_FK_Left"],
                ["m_avg_L_Wrist","Ctrl_Hand_FK_Left"],
                ["m_avg_L_Hand",""],
                ["m_avg_R_Collar","Ctrl_Shoulder_Right"],
                ["m_avg_R_Shoulder","Ctrl_Arm_FK_Right"],
                ["m_avg_R_Elbow","Ctrl_ForeArm_FK_Right"],
                ["m_avg_R_Wrist","Ctrl_Hand_FK_Right"],
                ["m_avg_R_Hand",""]
                ]
        target = 'stg2'
        
        bind(context,rig,target)
        retarget(context,target)



        # stg2_armature.select_set(True)
        # bpy.context.view_layer.objects.active = stg2_armature
        # bpy.context.view_layer.update()


        ############## Bake to IK ##################
        bones = ['Ctrl_Hand_FK_Left','Ctrl_Hand_FK_Right','Ctrl_Foot_FK_Left','Ctrl_Foot_FK_Right']
        switch_ik_fk_anim(self,context,bones)

        context.scene.source = stg2_armature #colocar Ik control Armature como Source



        return{'FINISHED'}


class SwitchFKIKPart(Operator):
    bl_idname = "fdh.switch_ik_fk_part"
    bl_label = "Swith FK IK"
    bl_description = "Swith FK IK"
    bl_options = {"REGISTER", "UNDO"}

    option: IntProperty(name='',default=0) #0- hands 1-legs
    def execute(self,context):
        
        if self.option == 0:
            bones = ['Ctrl_Hand_FK_Left','Ctrl_Hand_FK_Right']

        if self.option == 1:
            bones = ['Ctrl_Foot_FK_Left','Ctrl_Foot_FK_Right']

        switch_ik_fk_anim(self,context,bones)

        return{'FINISHED'}

class Setupfloor(Operator):
    bl_idname = "fdh.setup_floor"
    bl_label = "Setup Floor"
    bl_description = "Setup Floor"
    bl_options = {"REGISTER", "UNDO"}

    # option: IntProperty(name='',default=0) #0- hands 1-legs
    def execute(self,context):
        fourd_prop = context.scene.fourd_prop
        scn = context.scene
        # obj = context.active_object
        obj = context.scene.floor

        mat = obj.matrix_local
        obj.data.transform(mat)
        obj.matrix_local = mathutils.Matrix()

        obj_copy = obj.copy()
        bpy.context.collection.objects.link(obj_copy)
        obj_copy.parent = obj

        obj_copy.hide_select = True
        # obj_copy.hide_viewport = False
        obj_copy.hide_viewport = True
        obj_copy.hide_render = True

        obj_copy.display_type = 'WIRE'

        default_distance = 0.061255

        obj_copy.location[2] = default_distance
        fourd_prop.fl_floor_distance_fine_tune = default_distance

        parent_collision = [
                        'Ctrl_FootRoll_LeftBorder_Left',
                        'Ctrl_FootRoll_LeftBorder_Right',
                        'Ctrl_FRONT_Left',
                        'Ctrl_FootRoll_RightBorder_Left',
                        'Ctrl_FootRoll_RightBorder_Right',
                        'Ctrl_FRONT_Right',
                        ]



        child_collision = [
                        'Ctrl_Foot_IK_Left',
                        'Ctrl_Foot_IK_Right'
                        ]

        for pc in parent_collision:
            print('pc: ',pc)
            scn.target_stg2.pose.bones[pc].constraints[0].target = scn.floor

        for cc in child_collision:
            scn.target_stg2.pose.bones[cc].constraints[1].target = scn.floor.children[0]

        return{'FINISHED'}

class SetupFootLock(Operator):
    bl_idname = "fdh.setup_foot_lock"
    bl_label = "Setup Foot Lock"
    bl_description = "Setup Foot Lock"
    bl_options = {"REGISTER", "UNDO"}

    # option: IntProperty(name='',default=0) #0- hands 1-legs
    def execute(self,context):
        scn = context.scene

        o_r = bpy.data.objects.new( "empty", None )
        bpy.context.collection.objects.link( o_r )
        o_r.empty_display_size = 0.05
        o_r.empty_display_type = 'CUBE' 
        o_r.rotation_mode = 'QUATERNION'

        o_l = bpy.data.objects.new( "empty", None )
        bpy.context.collection.objects.link( o_l )
        o_l.empty_display_size = 0.05
        o_l.empty_display_type = 'CUBE' 
        o_l.rotation_mode = 'QUATERNION'

        o_r_loc = scn.target_stg2.pose.bones['Ctrl_Foot_IK_Right'].matrix.to_translation()
        o_l_loc = scn.target_stg2.pose.bones['Ctrl_Foot_IK_Left'].matrix.to_translation()

        o_r_rot = scn.target_stg2.pose.bones['Ctrl_Foot_IK_Right'].matrix.to_quaternion()
        o_l_rot = scn.target_stg2.pose.bones['Ctrl_Foot_IK_Left'].matrix.to_quaternion()

        o_r.location = o_r_loc
        o_l.location = o_l_loc
        o_r.rotation_quaternion = o_r_rot
        o_l.rotation_quaternion = o_l_rot
        

        scn.foot_lock_right = o_r
        scn.foot_lock_left = o_l

        scn.target_stg2.pose.bones['Ctrl_Foot_IK_Right'].constraints[2].target = o_r
        scn.target_stg2.pose.bones['Ctrl_Foot_IK_Left'].constraints[2].target = o_l

        return{'FINISHED'}

class StartEndFootLock(Operator):
    bl_idname = "fdh.start_end__foot_lock"
    bl_label = "Start End Foot Lock"
    bl_description = "Start End Foot Lock"
    bl_options = {"REGISTER", "UNDO"}

    option: IntProperty(name='',default=0)  #0- start_left; 1-end_left; 2-start_right; 3-end_right; 4=Copy left bone 2 empty loc/rot to empty; 5=Copy right bone 2 empty loc/rot to empty

    
    def execute(self,context):
        scn = context.scene
        fourd_prop = context.scene.fourd_prop

        if self.option == 0: #0- start_left
            o_l = scn.foot_lock_left
            o_l_loc = scn.target_stg2.pose.bones['Ctrl_Foot_IK_Left'].matrix.to_translation()
            
            o_l_rot_euler = scn.target_stg2.pose.bones['Ctrl_Foot_IK_Left'].matrix.to_euler()
            o_l_rot_euler.x=0
            o_l_rot_euler.y=0
            o_l_rot = o_l_rot_euler.to_quaternion()


            o_l.location = o_l_loc
            o_l.rotation_quaternion = o_l_rot

            ## left
            scn.foot_lock_left.keyframe_insert(data_path='location',frame=scn.frame_current-fourd_prop.int_fadein_foot_lock_frames)
            scn.foot_lock_left.keyframe_insert(data_path='rotation_quaternion',frame=scn.frame_current-fourd_prop.int_fadein_foot_lock_frames)
            scn.foot_lock_left.keyframe_insert(data_path='location',frame=scn.frame_current)
            scn.foot_lock_left.keyframe_insert(data_path='rotation_quaternion',frame=scn.frame_current)
            scn.target_stg2.pose.bones['Ctrl_Foot_IK_Left'].constraints[2].influence = 0.0
            scn.target_stg2.pose.bones['Ctrl_Foot_IK_Left'].constraints[2].keyframe_insert(data_path='influence',frame=scn.frame_current-fourd_prop.int_fadein_foot_lock_frames)
            scn.target_stg2.pose.bones['Ctrl_Foot_IK_Left'].constraints[2].influence = 1.0
            scn.target_stg2.pose.bones['Ctrl_Foot_IK_Left'].constraints[2].keyframe_insert(data_path='influence',frame=scn.frame_current)




        if self.option == 2: #2-start_right;
            o_r = scn.foot_lock_right
            o_r_loc = scn.target_stg2.pose.bones['Ctrl_Foot_IK_Right'].matrix.to_translation()
            o_r_rot_euler = scn.target_stg2.pose.bones['Ctrl_Foot_IK_Right'].matrix.to_euler()
            o_r_rot_euler.x=0
            o_r_rot_euler.y=0
            
            o_r_rot = o_r_rot_euler.to_quaternion()
            o_r.location = o_r_loc
            o_r.rotation_quaternion = o_r_rot

            ## right
            scn.foot_lock_right.keyframe_insert(data_path='location',frame=scn.frame_current-fourd_prop.int_fadein_foot_lock_frames)
            scn.foot_lock_right.keyframe_insert(data_path='rotation_quaternion',frame=scn.frame_current-fourd_prop.int_fadein_foot_lock_frames)
            scn.foot_lock_right.keyframe_insert(data_path='location',frame=scn.frame_current)
            scn.foot_lock_right.keyframe_insert(data_path='rotation_quaternion',frame=scn.frame_current)
            scn.target_stg2.pose.bones['Ctrl_Foot_IK_Right'].constraints[2].influence = 0.0
            scn.target_stg2.pose.bones['Ctrl_Foot_IK_Right'].constraints[2].keyframe_insert(data_path='influence',frame=scn.frame_current-fourd_prop.int_fadein_foot_lock_frames)
            scn.target_stg2.pose.bones['Ctrl_Foot_IK_Right'].constraints[2].influence = 1.0
            scn.target_stg2.pose.bones['Ctrl_Foot_IK_Right'].constraints[2].keyframe_insert(data_path='influence',frame=scn.frame_current)


        if self.option == 1:# 1-end_left
            ## left
            scn.foot_lock_left.keyframe_insert(data_path='location',frame=scn.frame_current)
            scn.foot_lock_left.keyframe_insert(data_path='rotation_quaternion',frame=scn.frame_current)
            scn.target_stg2.pose.bones['Ctrl_Foot_IK_Left'].constraints[2].influence = 1.0
            scn.target_stg2.pose.bones['Ctrl_Foot_IK_Left'].constraints[2].keyframe_insert(data_path='influence',frame=scn.frame_current-fourd_prop.int_fadeout_foot_lock_frames)
            scn.target_stg2.pose.bones['Ctrl_Foot_IK_Left'].constraints[2].influence = 0.0
            scn.target_stg2.pose.bones['Ctrl_Foot_IK_Left'].constraints[2].keyframe_insert(data_path='influence',frame=scn.frame_current)

        

        if self.option == 3: #3-end_right
            ## right
            scn.foot_lock_right.keyframe_insert(data_path='location',frame=scn.frame_current)
            scn.foot_lock_right.keyframe_insert(data_path='rotation_quaternion',frame=scn.frame_current)
            scn.target_stg2.pose.bones['Ctrl_Foot_IK_Right'].constraints[2].influence = 1.0
            scn.target_stg2.pose.bones['Ctrl_Foot_IK_Right'].constraints[2].keyframe_insert(data_path='influence',frame=scn.frame_current-fourd_prop.int_fadeout_foot_lock_frames)
            scn.target_stg2.pose.bones['Ctrl_Foot_IK_Right'].constraints[2].influence = 0.0
            scn.target_stg2.pose.bones['Ctrl_Foot_IK_Right'].constraints[2].keyframe_insert(data_path='influence',frame=scn.frame_current)


        if self.option == 4: #4- copy bone loc/rot left
            o_l = scn.foot_lock_left
            o_l_loc = scn.target_stg2.pose.bones['Ctrl_Foot_IK_Left'].matrix.to_translation()
            
            o_l_rot_euler = scn.target_stg2.pose.bones['Ctrl_Foot_IK_Left'].matrix.to_euler()
            o_l_rot = o_l_rot_euler.to_quaternion()

            o_l.location = o_l_loc
            o_l.rotation_quaternion = o_l_rot

            ## left
            scn.foot_lock_left.keyframe_insert(data_path='location',frame=scn.frame_current)
            scn.foot_lock_left.keyframe_insert(data_path='rotation_quaternion',frame=scn.frame_current)



        if self.option == 5: #5-Copy loc/rot bone right;
            o_r = scn.foot_lock_right
            o_r_loc = scn.target_stg2.pose.bones['Ctrl_Foot_IK_Right'].matrix.to_translation()
            o_r_rot_euler = scn.target_stg2.pose.bones['Ctrl_Foot_IK_Right'].matrix.to_euler()
            
            o_r_rot = o_r_rot_euler.to_quaternion()
            o_r.location = o_r_loc
            o_r.rotation_quaternion = o_r_rot

            ## right
            scn.foot_lock_right.keyframe_insert(data_path='location',frame=scn.frame_current)
            scn.foot_lock_right.keyframe_insert(data_path='rotation_quaternion',frame=scn.frame_current)

        return{'FINISHED'}


class ClearFootLock(Operator):
    bl_idname = "fdh.clear_foot_lock"
    bl_label = "Clear Foor Lock"
    bl_description = "Clear Foot Lock"
    bl_options = {"REGISTER", "UNDO"}

    option: IntProperty(name='',default=0) #0- left; 1-right
    
    def execute(self,context):
        scn = context.scene

        start_frame = scn.frame_start
        end_frame = scn.frame_end


        if self.option == 0: #left 
            scn.foot_lock_left.animation_data_clear()
            for f in range(start_frame,end_frame+1):
                # print('f: ',f)
                # scn.foot_lock_left.keyframe_delete(data_path='location',frame=f)
                # scn.foot_lock_left.keyframe_delete(data_path='rotation_quaternion',frame=f)
                scn.target_stg2.pose.bones['Ctrl_Foot_IK_Left'].constraints[2].keyframe_delete(data_path='influence',frame=f)
                scn.target_stg2.pose.bones['Ctrl_Foot_IK_Left'].constraints[2].influence = 0.0


        if self.option == 1: #right
            scn.foot_lock_right.animation_data_clear()
            for f in range(start_frame,end_frame+1):
                # print('f: ',f)
                # scn.foot_lock_right.keyframe_delete(data_path='location',frame=f)
                # scn.foot_lock_right.keyframe_delete(data_path='rotation_quaternion',frame=f)
                scn.target_stg2.pose.bones['Ctrl_Foot_IK_Right'].constraints[2].keyframe_delete(data_path='influence',frame=f)
                scn.target_stg2.pose.bones['Ctrl_Foot_IK_Right'].constraints[2].influence = 0.0

        return{'FINISHED'}


class FixFootFCurve(Operator):
    bl_idname = "fdh.fix_foot_fcurve"
    bl_label = "Fix Foot Fcurve"
    bl_description = "Fix Foot Fcurve"
    bl_options = {"REGISTER", "UNDO"}

    option: IntProperty(name='',default=0)
    def execute(self,context):
        scn = context.scene
        try:
            fcurves_left = scn.foot_lock_left.animation_data.action.fcurves
            for fcl in fcurves_left:
                for ptl in fcl.keyframe_points:
                    ptl.interpolation = 'CONSTANT'
        except:
            print('couldnt fix left foot')

        try:
            fcurves_right = scn.foot_lock_right.animation_data.action.fcurves
            for fcr in fcurves_right:
                for ptr in fcr.keyframe_points:
                    ptr.interpolation = 'CONSTANT'
        except:
            print('couldnt fix right foot')

        return{'FINISHED'}
