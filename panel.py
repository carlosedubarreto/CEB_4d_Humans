# from typing import Text
# from ctypes import alignment
# from unittest.mock import DEFAULT
import bpy,os,glob
from os.path import join
import sys
import textwrap
from bpy.types import Operator, Panel, UIList, PropertyGroup, Menu
from bpy.props import EnumProperty, CollectionProperty, IntProperty
global DEFAULT_NAME
DEFAULT_NAME = 'py310_torch1.13.0_cu117_env'
DEFAULT_NAME_WHAM = 'py39_torch1.11.0_cu113_env'
DEFAULT_NAME_SLAHMR = 'py310_torch1.13.0_cu117_env_SLAHMR'



# def updt_bool_imgs(self,context):
#     fourd_prop = context.scene.fourd_prop
#     if fourd_prop.bool_custom_imgs:
#         fourd_prop.bool_batch_execution = False
#         # print('1-1')


# def updt_bool_batch(self,context):
#     fourd_prop = context.scene.fourd_prop
#     if fourd_prop.bool_batch_execution:
#         fourd_prop.bool_custom_imgs = False
#         # print('2-1')




# def updt_bool_max_img(self,context):
#     fourd_prop = context.scene.fourd_prop
#     if fourd_prop.bool_max_img:
#         fourd_prop.bool_enable_max_img = True
#     else: 
#         fourd_prop.bool_enable_max_img = False
#         fourd_prop.int_max_img = 10

# def updt_bool_max_res(self,context):
#     fourd_prop = context.scene.fourd_prop
#     if fourd_prop.bool_max_res:
#         fourd_prop.bool_enable_max_res = True
#     else: 
#         fourd_prop.bool_enable_max_res = False
#         fourd_prop.int_max_res = 4096

def select_action_strip(self,context):
    armature = bpy.context.selected_objects[0]
    a_strips = armature.animation_data.nla_tracks[0].strips
    for i,ast in enumerate(a_strips):
        if i == self.active_track_index:
            ast.select = True
        else:
            ast.select = False
    # armature.animation_data.nla_tracks[0].strips[self.active_track_index].select = True

def update_fps(self,context):
    bpy.context.scene.render.fps=int(self.enum_fps)

def update_venv_name_from_list(self,context):
    global DEFAULT_NAME
    fourd_prop = context.scene.fourd_prop
    # folder = fourd_prop.str_sd_prompt.strip().replace(' ','_')
    folder = fourd_prop.enum_custom_venv_list

    if folder == '-1':
        # fourd_prop.str_custom_venv_name = 'text2light_39_env'
        fourd_prop.str_custom_venv_name = DEFAULT_NAME
    if folder > '0': #0 é o que chamo the Nothing no panel
        fourd_prop.str_custom_venv_name = folder

def _label_multiline(context, text, parent):
    chars = int(context.region.width / 7)   # 7 pix on 1 character
    wrapper = textwrap.TextWrapper(width=chars)
    text_lines = wrapper.wrap(text=text)
    for text_line in text_lines:
        parent.label(text=text_line)

def updt_custom_venv_name(self,context):
    fourd_prop = context.scene.fourd_prop
    custom_venv_name = fourd_prop.str_custom_venv_name
    path_addon = os.path.dirname(os.path.abspath(__file__))
    custom_path_txt = join(path_addon,'custom_path.txt')
    with open(custom_path_txt, "wt") as fout_custom:
        fout_custom.write(custom_venv_name)

def updt_bool_custom_venv(self,context):
    global DEFAULT_NAME
    fourd_prop = context.scene.fourd_prop
    # wm = context.window_manager
    if not self.bool_custom_venv:
        fourd_prop.str_custom_venv_name = DEFAULT_NAME

def updt_bool_venv_custom_name(self,context):
    fourd_prop = context.scene.fourd_prop
    # wm = context.window_manager
    if self.bool_custom_venv_name:
        fourd_prop.bool_custom_venv_name_from_list = False   
def updt_bool_venv_custom_name_from_list(self,context):
    fourd_prop = context.scene.fourd_prop
    # wm = context.window_manager
    if self.bool_custom_venv_name_from_list:
        fourd_prop.bool_custom_venv_name= False  

def folder_venv_callback(scene, context):
    fourd_prop = context.scene.fourd_prop
    directory = fourd_prop.str_venv_path
    
    if os.path.exists(directory):
        folders = []
        # for root, dirs, files in os.walk(directory):
        for name_file_dir in os.listdir(directory):
            if os.path.isdir(join(directory,name_file_dir)) and name_file_dir.endswith('_39_env'):
                folders.append(name_file_dir)

        # list_folder = folders[0]
        list_folder = folders
        # print(list_folder)
        
        items = []
        i=0

        ####
        #generate the custom size to search for Constraint name (to be able to use "startswith")
        # len_name_start_ctr = len(name+'-{:03}'.format(0))
        items.append(("-1","Choose a Folder","Choose a Folder"))
        for x in range(len(list_folder)):
            i=i+1
            items.append((list_folder[x],"%s" % list_folder[x],"Data: %s" % list_folder[x]))
        if len(items) == 0:
            items.append((str(0),"Nothing","No Data available"))
    else:
        items = [(str(0),"Nothing","No Data available")]
        
    return items


def rig_list_callback(scene, context):
    # fourd_prop = context.scene.fourd_prop
    path_addon = os.path.dirname(os.path.abspath(__file__))
    rig_files = os.path.join(path_addon,'rig','*.json')

    list_files_json = glob.glob(rig_files)
    items= []
    items.append(("-1","-----Choose a Rig-----","Choose a RIG"))
    for f in list_files_json:
        file = os.path.splitext(os.path.basename(f))[0]
        
        items.append((file,"%s" % file,"Data: %s" % file))
        if len(items) == 0:
            items.append((str(0),"Nothing","No Data available"))
    return items

def floor_distance_fine_tune(self,context):
    floor = context.scene.floor
    floor.children[0].location[2] = self.fl_floor_distance_fine_tune


class ACTION_UL_list(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        scene = data
        ob = item
        # print('data: ',data,'\n','item: ', item,'\n','icon: ',icon,'\n','active_date: ',  active_data,'\n','active_propname: ', active_propname,'\n')
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            layout.prop(ob, "name", text="", emboss=False, icon_value=layout.icon(ob))


class ACTION_STRIP_UL_list(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        scene = data
        ob = item
        # print('data: ',data,'\n','item: ', item,'\n','icon: ',icon,'\n','active_date: ',  active_data,'\n','active_propname: ', active_propname,'\n')
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            if ob.name.startswith('Transition'):
                layout.prop(ob, "name", text="------", emboss=False, icon_value=layout.icon(ob))
            else:
                layout.prop(ob, "name", text="", emboss=False, icon_value=layout.icon(ob))


def ik_control_panel(context,layout,row,path_venv,file_fbx):
    scene = context.scene
    fourd_prop = context.scene.fourd_prop
    row.separator()
    row.separator()
    row.prop(scene,'source')
    # row.separator()
    row.operator('fdh.stg2_full')
    row.operator('fdh.switch_ik_fk_part',text='Switch FK-IK Hands').option=0
    row.operator('fdh.switch_ik_fk_part',text='Switch FK-IK Foot').option=1
    rowb = layout.row(align=True).box()
    rowb = rowb.column(align=True)
    row = rowb.row(align=True)
    # row.enabled = enable_ctr
    row.enabled = True
    row.prop(scene, "ik_advanced",
    icon="TRIA_DOWN" if scene.ik_advanced else "TRIA_RIGHT",
    icon_only=True, emboss=False
    )
    row_alert_create_venv = row.column(align=True)
    if os.path.exists(path_venv) and os.path.exists(file_fbx):
        row_alert_create_venv.alert = False
    else:
        row_alert_create_venv.alert = True
    row_alert_create_venv.label(text='IK Adv Options') 


    if scene.ik_advanced:
        scn = context.scene
        row = rowb.column(align=True)

        row_ik_adv = row.column(align=True)
        # row_path2 = row.row(align=True)
        
        # row_path.label(text='Select a valid Path')
        row_ik_adv.operator('fdh.append_stg2')
        row_ik_adv.prop(scn,'target_stg2')
        row_ik_adv.operator('fdh.stg2_retarget')
        row_ik_adv.operator('fdh.mr_switch_snap_anim')
        row_ik_adv.label(text='Floor setup')
        row_ik_adv.prop(scn,'floor')
        row_ik_adv_setup = row_ik_adv.column(align=1)
        if scn.floor == None:
            row_ik_adv_setup.enabled = False
        else:
            row_ik_adv_setup.enabled = True
        row_ik_adv_setup.operator('fdh.setup_floor')
        row_ik_adv_setup.prop(fourd_prop,'fl_floor_distance_fine_tune')
        
        row_ik_adv.label(text='Foot Lock')
        row_ik_adv.prop(scn,'foot_lock_left',text='Left')
        row_ik_adv.prop(scn,'foot_lock_right',text='Right')
        row_ik_adv.operator('fdh.setup_foot_lock')
        
        row_ik_adv.separator()
        row_ik_adv_row = row_ik_adv.row(align=1)
        row_ik_adv_row.operator('fdh.start_end__foot_lock',text='L Copy B2E').option=4
        row_ik_adv_row.operator('fdh.start_end__foot_lock',text='R Copy B2E').option=5
        row_ik_adv.separator()
        row_ik_adv_row = row_ik_adv.row(align=1)
        row_ik_adv_row.operator('fdh.start_end__foot_lock',text='L Start').option=0
        row_ik_adv_row.operator('fdh.start_end__foot_lock',text='R Start').option=2
        row_ik_adv_row = row_ik_adv.row(align=1)
        row_ik_adv_row.operator('fdh.start_end__foot_lock',text='L End').option=1
        row_ik_adv_row.operator('fdh.start_end__foot_lock',text='R End').option=3

        row_ik_adv.separator()
        row_ik_adv_row = row_ik_adv.row(align=1)
        row_ik_adv_row.operator('fdh.clear_foot_lock',text='L Clear').option=0
        row_ik_adv_row.operator('fdh.clear_foot_lock',text='R Clear').option=1
        row_ik_adv.separator()
        row_ik_adv.operator('fdh.fix_foot_fcurve')




        row_ik_adv.label(text='Transition Frames')
        row_ik_adv_row = row_ik_adv.row(align=1)
        row_ik_adv_row.prop(fourd_prop,'int_fadein_foot_lock_frames',text="In")
        row_ik_adv_row.prop(fourd_prop,'int_fadeout_foot_lock_frames',text="Out")



class FOURDHUMANS_PT_Panel(bpy.types.Panel):
    # bl_idname = "CEB_PT_TA"
    bl_label = "4D Humans"
    bl_category = "CEB"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        scene = context.scene
        fourd_prop = context.scene.fourd_prop

        layout = self.layout
        scene = context.scene
        fourd_prop = context.scene.fourd_prop
        path_addon = os.path.dirname(os.path.abspath(__file__))
        pkl_folder = os.path.join(path_addon,'4D-Humans-main','outputs','results')
        

        path_venv = join(fourd_prop.str_venv_path,fourd_prop.str_custom_venv_name)
        path_venv_wham = join(fourd_prop.str_venv_path,fourd_prop.str_custom_venv_name_wham)
        path_venv_slahmr = join(fourd_prop.str_venv_path,fourd_prop.str_custom_venv_name_slahmr)
        flag_installed = join(fourd_prop.str_venv_path,fourd_prop.str_custom_venv_name,'Lib','site-packages','torch')
        flag_installed_wham = join(fourd_prop.str_venv_path,fourd_prop.str_custom_venv_name_wham,'Lib','site-packages','torch')
        flag_installed_wham_reqs = join(fourd_prop.str_venv_path,fourd_prop.str_custom_venv_name_wham,'Lib','site-packages','mmcv')
        flag_installed_pre_detectron2 = join(fourd_prop.str_venv_path,fourd_prop.str_custom_venv_name,'Lib','site-packages','pycocotools')
        flag_installed_detectron2 = join(fourd_prop.str_venv_path,fourd_prop.str_custom_venv_name,'Lib','site-packages','detectron2')
        
        flag_installed_slahmr_torch = join(fourd_prop.str_venv_path,fourd_prop.str_custom_venv_name_slahmr,'Lib','site-packages','torch')
        flag_installed_slahmr_reqs = join(fourd_prop.str_venv_path,fourd_prop.str_custom_venv_name_slahmr,'Lib','site-packages','torchgeometry')
        flag_installed_slahmr_detectron2 = join(fourd_prop.str_venv_path,fourd_prop.str_custom_venv_name_slahmr,'Lib','site-packages','detectron2')
        # flag_installed_slahmr_torch_scatter = join(fourd_prop.str_venv_path,fourd_prop.str_custom_venv_name_slahmr,'Lib','site-packages','torch_scatter')
        flag_installed_slahmr_lietorch = join(fourd_prop.str_venv_path,fourd_prop.str_custom_venv_name_slahmr,'Lib','site-packages','lietorch')
        
        
        flag_installed_cv2 = join(fourd_prop.str_venv_path,fourd_prop.str_custom_venv_name,'Lib','site-packages','scipy')
        flag_installed_smpl_male = join(path_addon,'wham','dataset','body_models','smpl','SMPL_MALE.pkl')
        flag_installed_smpl_female = join(path_addon,'wham','dataset','body_models','smpl','SMPL_FEMALE.pkl')
        flag_installed_smpl_neutral = join(path_addon,'wham','dataset','body_models','smpl','SMPL_NEUTRAL.pkl')
        flag_ckp_dpvo_pth = join(path_addon,'wham','checkpoints','dpvo.pth')
        flag_ckp_hmr2a_ckpt = join(path_addon,'wham','checkpoints','hmr2a.ckpt')
        flag_ckp_vitpose = join(path_addon,'wham','checkpoints','vitpose-h-multi-coco.pth')
        flag_ckp_wham_vit_w = join(path_addon,'wham','checkpoints','wham_vit_w_3dpw.pth.tar')
        flag_ckp_wha_vit_bedlam = join(path_addon,'wham','checkpoints','wham_vit_bedlam_w_3dpw.pth.tar')
        flag_ckp_yolov8x = join(path_addon,'wham','checkpoints','yolov8x.pt')
        flag_wham_body_models = join(path_addon,'wham','dataset','body_models','smplx2smpl.pkl')
        flag_video_wham = join(path_addon,'wham','example_data','video.mp4')
        flag_wham_pickle = join(path_addon,'wham','output','demo','video','wham_output.pickle')


        file_fbx = os.path.join(path_addon,'basicModel_m_lbs_10_207_0_v1.0.2.fbx')
        
        CACHE_DIR = os.path.join(os.path.expanduser('~'), ".cache")
        smpl_path = os.path.join(CACHE_DIR, "phalp/3D/models/smpl/SMPL_NEUTRAL.pkl")
        smpl_path2 = os.path.join(CACHE_DIR, "4DHumans/data/smpl/SMPL_NEUTRAL.pkl")

        file_pkl = os.path.join(pkl_folder,'demo_video_converted.pkl')
        file_smooth = os.path.join(pkl_folder,'demo_video_converted_smooth.pkl')

        # flag_installed_einops = join(fourd_prop.str_venv_path,fourd_prop.str_custom_venv_name,'Lib','site-packages','einops')
        row = layout.column(align=True).box()
        row = row.column(align=True)

        row_col = row.row(align=1)
        row_col.prop(fourd_prop,'bool_4dhumans',toggle=True,text='4D Humans')
        row_col.prop(fourd_prop,'bool_wham',toggle=True,text='WHAM')
        row_col.prop(fourd_prop,'bool_slahmr',toggle=True,text='SLAHMR')

        row_col = row.row(align=True)
        row_col.prop(fourd_prop,'bool_retarget_panel',toggle=True,text='Retarget')
        row_col.prop(fourd_prop,'bool_extract_marked_frames_panel',toggle=True,text='Extract Marked Frames')
        row_col = row.row(align=True)
        row_col.prop(fourd_prop,'bool_ik_control_panel',toggle=True,text='IK Control')
        if fourd_prop.bool_4dhumans:
            row_col = row.row(align=True)
            row_col.label(text='Panels')
            row_col.prop(fourd_prop,'bool_core_panel',toggle=True,text='Core')
            row_col.prop(fourd_prop,'bool_core_exe_panel',toggle=True,text='Exe')
            row_col.prop(fourd_prop,'bool_core_imp_exp_panel',toggle=True,text='I/E')
            row_col.prop(fourd_prop,'bool_core_smooth_panel',toggle=True,text='S')
            row_col.prop(fourd_prop,'bool_core_load_panel',toggle=True,text='L')
            row_col = row.row(align=True)
            row_col.prop(fourd_prop,'bool_smooth_panel',toggle=True,text='Smooth')
            row_col.prop(fourd_prop,'bool_footlock_panel',toggle=True,text='Foot')
            row_col.prop(fourd_prop,'bool_export_panel',toggle=True,text='Export Tools')
            row_col = row.row(align=True)
            row_col.prop(fourd_prop,'bool_nla_action_panel',toggle=True,text='NLA Action')
            row_col.prop(fourd_prop,'bool_nla_track_panel',toggle=True,text='NLA Track')
            





            if fourd_prop.bool_core_panel:
                if fourd_prop.bool_core_exe_panel:
                    row = layout.row(align=True).box()
                    row = row.column(align=True)
                    row.label(text='Video:')
                    row.operator('fdh.add_video')
                    row.separator()
                    row_text = row.column()
                    row_load_video = row.column()

                    if fourd_prop.str_videopath == '':
                        row_text.alert = True
                        text_path = 'Please choose a path'
                        row_load_video.enabled = False
                    else:
                        text_path = 'Video Path: '+fourd_prop.str_videopath
                        row_text.alert = False
                        row_load_video.enabled = True

                    _label_multiline(
                        context=context,
                        text=text_path,
                        parent=row_text
                        )
                    # row.operator('wm.url_open',text='Instructions',icon='URL').url = 'https://github.com/satoshi-ikehata/SDM-UniPS-CVPR2023#step-2-image-acquisition'
                    row_load_video.separator()
                    row_load_video.operator('fdh.load_video_3dview')

                    
                    row_exe = layout.box()
                    row_exe_run = row_exe.column(align=True)
                    row_fps = row_exe.column(align=True)


                    if fourd_prop.str_videopath == '':
                        row_exe_run.enabled = False
                    else:
                        row_exe_run.enabled = True
                    if os.path.exists(path_venv):
                        row_exe_run.alert = False
                        row_exe_run.enabled = True

                    else:
                        row_exe_run.alert = True
                        row_exe_run.enabled = False
                    # row_exe_run.label(text='Part 1 - Generate PKL')
                    row_exe_run.operator('fdh.execute').option = 0
                    row_exe_run.operator('fdh.execute',text='Execute w/ Less VRAM').option = 1
                    row_exe_run.separator()
                    # row_exe_run.label(text='Part 2 - Convert PKL')
                    # row_exe_run
                    if fourd_prop.enum_fps == str(context.scene.render.fps):
                        row_fps.prop(fourd_prop,'enum_fps')
                    else:
                        row_fps.operator('fdh.set_ini_fps')
                



                if fourd_prop.bool_core_imp_exp_panel:
                    # row_exe_resmooth = row_exe
                    # if os.path.exists(file_smooth):
                    #     row_exe_resmooth.enabled = True
                    # else:
                    #     row_exe_resmooth.enabled = False
                    # row_exe_resmooth.operator('fdh.smooth',text='ReSmooth').pkl_file='demo_video_converted_smooth.pkl'

                    row_anim_exp = layout.box()
                    row_anim_exp.label(text='Import/Export Animation')
                    row_anim_exp.operator('wm.url_open',text='Animation Library',icon='URL').url = 'https://www.patreon.com/cebstudios/posts?filters%5Btag%5D=4d-humans-animation'
                    row_anim_exp = row_anim_exp.column(align=True)
                    row_anim_exp_buttom = row_anim_exp.column(align=True)
                    row_anim_exp_text = row_anim_exp.column(align=True)
                    
                    row_anim_exp_buttom_col = row_anim_exp_buttom.column(align=True)
                    row_anim_exp_buttom = row_anim_exp_buttom.row(align=True)
                    if os.path.exists(file_pkl):
                        row_anim_exp_buttom.operator('fdh.export_animation',text='Export')
                    row_anim_exp_buttom.operator('fdh.import_pkl_animation',text='Import').option=0
                    row_anim_exp_buttom_col.operator('fdh.import_pkl_animation',text='Import PKL Google Colab').option=1


                    
                    if fourd_prop.str_pklpath != '':
                        text_pkl_path = "Loaded PKL: "+fourd_prop.str_pklpath
                        _label_multiline(
                            context=context,
                            text=text_pkl_path,
                            parent=row_anim_exp_text
                            )

                if fourd_prop.bool_core_smooth_panel:
                    if os.path.exists(file_pkl):
                        row_smooth = layout.box()
                        row_smooth = row_smooth.column(align=True)
                        row_smooth.label(text='Smooth PKL')
                        row_smooth_col = row_smooth.row(align=True)
                        # row_smooth.operator('fdh.smooth').pkl_file='demo_video_converted.pkl'
                        smooth_both = row_smooth_col.operator('fdh.smooth',text='Both')
                        smooth_both.pkl_file='demo_video_converted.pkl'
                        smooth_both.smooth_what='both'
                        
                        smooth_pose = row_smooth_col.operator('fdh.smooth',text='Pose')
                        smooth_pose.pkl_file='demo_video_converted.pkl'
                        smooth_pose.smooth_what='pose'
                        
                        smooth_trans = row_smooth_col.operator('fdh.smooth',text='Translation')
                        smooth_trans.pkl_file='demo_video_converted.pkl'
                        smooth_trans.smooth_what='trans'


                if fourd_prop.bool_core_load_panel:
                    row = layout.box()
                    row = row.column(align=True)
                    
                    if fourd_prop.int_tot_character == 0 and os.path.exists(file_pkl):
                        row_column_pre_alert = row.row(align=True)
                        row_column_pre_alert.alert = True
                        row_column_pre_alert.operator('fdh.read_pkl_data').option=0

                    row_column_pre = row.row(align=True)
                    row_column_pre.label(text='Characters : '+str(fourd_prop.int_tot_character))
                    row_column_pre.prop(fourd_prop,'bool_fix_z',toggle=True)
                    row.prop(fourd_prop,'int_character',text='Number')
                    row.prop(fourd_prop,'bool_use_selected_character')
                    row_chr = row.column(align=True)
                    if fourd_prop.bool_use_selected_character:
                        row_chr.enabled = True
                    else:
                        row_chr.enabled = False

                    row_chr.prop(context.scene,'source',text='Character')
                    row_column = row.row(align=True)
                    row_column_import = row_column.row(align=True)


                    # if (fourd_prop.int_character <= fourd_prop.int_tot_character and os.path.exists(file_fbx) and not fourd_prop.bool_use_selected_character) or (fourd_prop.bool_use_selected_character and len(bpy.context.selected_objects)>0 and bpy.context.selected_objects[0].type == 'ARMATURE'):
                    if (fourd_prop.int_character <= fourd_prop.int_tot_character and os.path.exists(file_fbx) and not fourd_prop.bool_use_selected_character) or (fourd_prop.bool_use_selected_character and context.scene.source != None and context.scene.source.type == 'ARMATURE'):
                        row_column_import.enabled = True
                    else:
                        row_column_import.enabled = False
                    row_column_import.operator('fdh.import_character',text='Import Raw').option=0
                    row_column_import2 = row_column_import.column(align=True)
                    if os.path.exists(file_smooth):
                        row_column_import2.enabled = True
                    else:
                        row_column_import2.enabled = False
                    row_column_import2.operator('fdh.import_character',text='Import Smooth').option=1

                    
                        # row.separator()
                        # row.operator('fdh.stg2_full')
                        # row.operator('fdh.switch_ik_fk_part',text='Switch FK-IK Hands').option=0
                        # row.operator('fdh.switch_ik_fk_part',text='Switch FK-IK Foot').option=1
                        # rowb = layout.row(align=True).box()
                        # rowb = rowb.column(align=True)
                        # row = rowb.row(align=True)
                        # # row.enabled = enable_ctr
                        # row.enabled = True
                        # row.prop(scene, "ik_advanced",
                        # icon="TRIA_DOWN" if scene.ik_advanced else "TRIA_RIGHT",
                        # icon_only=True, emboss=False
                        # )
                        # row_alert_create_venv = row.column(align=True)
                        # if os.path.exists(path_venv) and os.path.exists(file_fbx):
                        #     row_alert_create_venv.alert = False
                        # else:
                        #     row_alert_create_venv.alert = True
                        # row_alert_create_venv.label(text='IK Adv Options') 


                        # if scene.ik_advanced:
                        #     scn = context.scene
                        #     row = rowb.column(align=True)

                        #     row_ik_adv = row.column(align=True)
                        #     # row_path2 = row.row(align=True)
                            
                        #     # row_path.label(text='Select a valid Path')
                        #     row_ik_adv.operator('fdh.append_stg2')
                        #     row_ik_adv.prop(scn,'target_stg2')
                        #     row_ik_adv.operator('fdh.stg2_retarget')
                        #     row_ik_adv.operator('fdh.mr_switch_snap_anim')
                        #     row_ik_adv.label(text='Floor setup')
                        #     row_ik_adv.prop(scn,'floor')
                        #     row_ik_adv_setup = row_ik_adv.column(align=1)
                        #     if scn.floor == None:
                        #         row_ik_adv_setup.enabled = False
                        #     else:
                        #         row_ik_adv_setup.enabled = True
                        #     row_ik_adv_setup.operator('fdh.setup_floor')
                        #     row_ik_adv_setup.prop(fourd_prop,'fl_floor_distance_fine_tune')
                            
                        #     row_ik_adv.label(text='Foot Lock')
                        #     row_ik_adv.prop(scn,'foot_lock_left',text='Left')
                        #     row_ik_adv.prop(scn,'foot_lock_right',text='Right')
                        #     row_ik_adv.operator('fdh.setup_foot_lock')
                            
                        #     row_ik_adv_row = row_ik_adv.row(align=1)
                        #     row_ik_adv_row.operator('fdh.start_end__foot_lock',text='L Start').option=0
                        #     row_ik_adv_row.operator('fdh.start_end__foot_lock',text='R Start').option=2
                        #     row_ik_adv_row = row_ik_adv.row(align=1)
                        #     row_ik_adv_row.operator('fdh.start_end__foot_lock',text='L End').option=1
                        #     row_ik_adv_row.operator('fdh.start_end__foot_lock',text='R End').option=3

                        #     row_ik_adv.separator()
                        #     row_ik_adv_row = row_ik_adv.row(align=1)
                        #     row_ik_adv_row.operator('fdh.clear_foot_lock',text='L Clear').option=0
                        #     row_ik_adv_row.operator('fdh.clear_foot_lock',text='R Clear').option=1
                        #     row_ik_adv.separator()
                        #     row_ik_adv.operator('fdh.fix_foot_fcurve')




                        #     row_ik_adv.label(text='Transition Frames')
                        #     row_ik_adv_row = row_ik_adv.row(align=1)
                        #     row_ik_adv_row.prop(fourd_prop,'int_fadein_foot_lock_frames',text="In")
                        #     row_ik_adv_row.prop(fourd_prop,'int_fadeout_foot_lock_frames',text="Out")





                    row.separator()

                    row = layout.box()
                    row_output_folder = row.column()
                    if os.path.exists(pkl_folder):
                        row_output_folder.enabled = True
                    else:
                        row_output_folder.enabled = False
                    
                    row_output_folder.operator('fdh.open_output_folder')

            if fourd_prop.bool_ik_control_panel:
                row = layout.box()
                row = row.column(align=True)
                ik_control_panel(context,layout,row,path_venv,file_fbx)

            if fourd_prop.bool_smooth_panel:
                row_smooth2 = layout.box()
                row_smooth2 = row_smooth2.column(align=True)
                row_smooth2.label(text='Smooth Anim Curves')
                row_smooth2.label(text='Giacomo Spaconi "j4ck" Method')
                row_smooth2.prop(fourd_prop,'bool_selected_bones')

                row_smooth2.operator('fdh.smooth2',text='Complete').option = 0
                row_smooth2 = row_smooth2.row(align=True)

                row_smooth2.operator('fdh.smooth2',text='Fix Graph').option = 1
                row_smooth2.operator('fdh.smooth2',text='Smooth').option = 2

            if fourd_prop.bool_footlock_panel:
                row_flock = layout.box()
                row_flock = row_flock.column(align=True)
                row_flock.label(text='Foot Lock')

                row_flock_sub0 = row_flock.row(align=True)
                row_flock_sub0.operator('fdh.foot_lock_marker',text='Floor Reference').option=2
                row_flock_sub0.operator('fdh.foot_lock',text='Analyze').option=0
                row_flock.label(text='Markers')
                row_flock_sub = row_flock.row(align=True)
                row_flock_sub.operator('fdh.foot_lock_marker',text='Start').option=0
                row_flock_sub.operator('fdh.foot_lock_marker',text='End').option=1
                # row_flock = row_flock.column(align=True)
                # row_flock.label(text='Apply')
                row_flock_col = row_flock.row(align=True)
                row_flock_col.operator('fdh.foot_lock',text='Apply').option=1
                row_flock_col.operator('fdh.foot_lock',text='Original Data').option=2
                row_flock.operator('fdh.foot_lock_marker',text='REMOVE MARKERS').option=-1

            if fourd_prop.bool_export_panel:

                row_export = layout.box()
                row_export = row_export.column(align=True)
                row_export.label(text='Export Tools')
                row_export_col = row_export.row(align=True)
                row_export_col.operator('fdh.zero_frame_t_pose',text='T Pose F0')
                row_export_col.operator('fdh.remove_location_animation',text='Remove Location')


            if fourd_prop.bool_nla_action_panel:
                #checka se ja existe alguma janela com nla_view
                scr      = bpy.context.window.screen
                nla_window = 0 
                for area in scr.areas:
                    if area.type == 'NLA_EDITOR':
                            nla_window = 1


                row_view = layout.box()
                row_view = row_view.column(align=True)
                if nla_window ==1:
                    row_view.enabled = False
                else:
                    row_view.enabled = True
                row_view.label(text='Open NLA View')
                row_view.operator('fdh.open_nla_view')

                row_nla = layout.box()
                row_nla = row_nla.column(align=True)
                row_nla.label(text='NLA Actions')
                row_nla_col = row_nla.row(align=True)
                row_nla_col.prop(fourd_prop,'str_nla_name')
                row_nla_col_paste = row_nla_col.column(align=True)
                if fourd_prop.str_videopath == '' and fourd_prop.str_pklpath == '':
                    row_nla_col_paste.enabled = False
                else:
                    row_nla_col_paste.enabled = True

                row_nla_col_paste.operator('fdh.nla_copy_name_to_nla',icon='PASTEDOWN',text='')

                #pega dados do objeto na cena
                ##########################
                # rows = 4
                scn = context.scene
                #load name of action that is active
                # ob = bpy.context.object
                if len(bpy.context.selected_objects) >0:
                    ob = bpy.context.selected_objects[0]
                else:
                    ob = None
                ###########################
                row_nla_create = row_nla.column(align=True)
                if ob is not None and ob.type == 'ARMATURE' and ob.animation_data.action is not None:
                    row_nla_create.enabled = True
                else:
                    row_nla_create.enabled = False
                row_nla_create.operator('fdh.nla_create_strip',text='Set Name')

                # row = layout.box()
                # row = row.column(align=True)
                row = row_nla

                if ob is not None:
                    action_name = (ob.animation_data.action.name if ob.animation_data is not None and ob.animation_data.action is not None else "")
                else:
                    action_name = ''

                if ob is not None and ob.animation_data is not None and len(ob.animation_data.nla_tracks)>0:
                    strip = ob.animation_data.nla_tracks[0]
                else:
                    strip = None

                # row.label(text='idx: '+str(scn.active_action_index))
                # row.label(text='Editing: '+action_name)

                # row.label(text=action_name)
                rows = 4
                row.template_list("ACTION_UL_list","",bpy.data,"actions",scn,"active_action_index",rows=rows)
                row.operator('fdh.nla_load_action',text='Load')
                row_act_col = row.row(align=True)
                row_act_col.operator('fdh.set_no_action',text='Unload')
                row_act_del = row_act_col.column(align=True)
                if scn.active_action_index > len(bpy.data.actions)-1:
                    row_act_del.enabled = False
                else:
                    row_act_del.enabled = True
                row_act_del.operator('fdh.nla_delete_action',text='Delete')
                row.separator()
                row.operator('fdh.create_ref')

            if fourd_prop.bool_nla_track_panel:
                #pega dados do objeto na cena
                ##########################
                # rows = 4
                scn = context.scene
                #load name of action that is active
                # ob = bpy.context.object
                if len(bpy.context.selected_objects) >0:
                    ob = bpy.context.selected_objects[0]
                else:
                    ob = None
                ###########################
                if ob is not None and ob.animation_data is not None and len(ob.animation_data.nla_tracks)>0:
                    strip = ob.animation_data.nla_tracks[0]
                else:
                    strip = None
                #checka se ja existe alguma janela com nla_view
                scr      = bpy.context.window.screen
                nla_window = 0 
                for area in scr.areas:
                    if area.type == 'NLA_EDITOR':
                            nla_window = 1


                row_strip = layout.box()
                row_strip = row_strip.column(align=True)
                row_strip.label(text='NLA Track Actions')

                strips_check = ob and ob.animation_data is not None and len(ob.animation_data.nla_tracks) == 0
                if ob is not None and ob.type == 'ARMATURE':
                    row_strip.enabled = True
                else:
                    row_strip.enabled = False

                if strips_check:
                    row_strip.operator('fdh.nla_add_track')
                else:
                    # row_strip.label(text='Action')
                    row_strip_col_act = row_strip.row(align=True)
                    row_strip_col_act.operator('fdh.add_action_to_track',text='Add')
                    row_strip_col_act.operator('fdh.add_action_to_track_w_transition',text='Add w Transition').option=0

                    row_strip.label(text='Transition')
                    # row_strip.prop(fourd_prop,'int_frames_transition')
                    row_strip_col_trans = row_strip.row(align=True)
                    row_strip_col_trans_lt = row_strip_col_trans.column(align=True)
                    row_strip_col_trans_gt = row_strip_col_trans.column(align=True)

                    #pega nome da action selecionada na strip
                    if ob is not None and ob.animation_data is not None and len(ob.animation_data.nla_tracks)>0 and len(ob.animation_data.nla_tracks[0].strips)>0 and scn.active_track_index >=0:
                        act_type_on_strip = ob.animation_data.nla_tracks[0].strips[scn.active_track_index].type
                        if scn.active_track_index > 0:
                            act_type_on_strip_prev = ob.animation_data.nla_tracks[0].strips[scn.active_track_index-1].type
                        else:
                            act_type_on_strip_prev = None

                        if scn.active_track_index < len(ob.animation_data.nla_tracks[0].strips)-1:
                            act_type_on_strip_next = ob.animation_data.nla_tracks[0].strips[scn.active_track_index+1].type
                        else:
                            act_type_on_strip_next = None
                    else:
                        act_type_on_strip = None
                        act_type_on_strip_next = None
                        act_type_on_strip_prev = None



                    if (ob is not None and scn.active_track_index == 0) or (ob is not None and scn.active_track_index is not None and (act_type_on_strip=='TRANSITION' or act_type_on_strip_prev =='TRANSITION')):
                        row_strip_col_trans_lt.enabled = False
                    else:
                        row_strip_col_trans_lt.enabled = True

                    if (ob is not None and ob.animation_data is not None and len(ob.animation_data.nla_tracks)>0 and len(ob.animation_data.nla_tracks[0].strips)-1 == scn.active_track_index) or (ob is not None and ob.animation_data is not None and len(ob.animation_data.nla_tracks)>0 and scn.active_track_index is not None and  (act_type_on_strip=='TRANSITION' or act_type_on_strip_next=='TRANSITION')):
                        row_strip_col_trans_gt.enabled = False
                    else:
                        row_strip_col_trans_gt.enabled = True

                    row_strip_col_trans_lt.operator('fdh.add_action_to_track_w_transition',icon='TRIA_LEFT',text='').option=1
                    row_strip_col_trans_gt.operator('fdh.add_action_to_track_w_transition',icon='TRIA_RIGHT',text='').option=2
                    row_strip_col_trans.prop(fourd_prop,'int_frames_transition')
                    
                    row_strip.separator()
                    if nla_window ==1:
                        # row_strip.label(text='Select on NLA Editor')
                        row_strip.prop(fourd_prop,'bool_nla_selection_tools')
                        if fourd_prop.bool_nla_selection_tools:
                            # row_strip.operator('fdh.select_action_on_strip').option=0
                            row_strip_col_select = row_strip.row(align=True)
                            # row_strip_col_select.operator('fdh.select_action_on_strip',text='Single').option=0 
                            row_strip_col_select.operator('fdh.select_action_on_strip',text='All').option=1
                            row_strip_col_select.operator('fdh.select_action_on_strip',text='None').option=2
                    row_strip.operator('fdh.match_to_prev_action')
                    
                    if not strips_check :
                        rows = 4
                        row_strip.template_list("ACTION_STRIP_UL_list","",strip,"strips",scn,"active_track_index",rows=rows)
                        row_strip.operator('fdh.delete_action_from_track')
                        row_strip.operator('fdh.organize_strip')


        # row_stage2 = layout.box()
        # row_stage2= row_stage2.column(align=True)

        # row_stage2.label(text='Stage2')
        if fourd_prop.bool_retarget_panel:
        
            scn = context.scene
            armature_mesh = context.scene.target_mesh

            row_rest_pose = layout.box()
            row_rest_pose = row_rest_pose.column(align=True)
            row_rest_pose_col = row_rest_pose.row(align= True)
            row_rest_pose_col.label(text='Change Tgt Rest Pose')
            # row_rest_pose_col.operator('fdh.clear_tgt_mesh_shapekeys')
            row_rest_pose.prop(scn,'target')
            row_rest_pose.prop(scn,'target_mesh',text='Mesh')
            row_rest_pose.operator('fdh.start_change_tgt_rest_pose')
            row_rest_pose_alert = row_rest_pose.column(align=True)
            row_rest_pose_alert.alert = True
            if armature_mesh is not None and armature_mesh.type == 'MESH' and armature_mesh.data.shape_keys is not None: #shape_keys is not nonee para ver se tem shapekeys
                _label_multiline(
                            context=context,
                            text='Executing this process will remove your shapekeys',
                            parent=row_rest_pose_alert
                            )
            row_rest_pose.operator('fdh.end_change_tgt_rest_pose')

            # row_rest_source_pose = row_rest_pose.column(align=1)
            # row_rest_source_pose.label(text='Source Pose')
            # row_rest_source_pose.operator('fdh.start_change_source_rest_pose')
            # row_rest_source_pose.operator('fdh.end_change_source_rest_pose')


            







            row_remap = layout.box()
            row_remap= row_remap.column(align=True)
            row_remap_col = row_remap.row(align=True)
            row_remap_col.label(text='Retarget')
            row_remap_choose_retarget = row_remap.column()
            if fourd_prop.enum_list_rig == '-1':
                row_remap_choose_retarget.alert=True
            else:
                row_remap_choose_retarget.alert=False
            

            row_remap_choose_retarget.prop(fourd_prop,'enum_list_rig')

            # row_remap_alert_prefix = row_remap.column()

            # if fourd_prop.enum_list_rig.startswith('mixamo') and  scn.target is not None and scn.target.type == 'ARMATURE':
                # prefix = scn.target.data.bones[0].name.split(':')[0]
                # if prefix+':' == fourd_prop.str_retarget_prefix:
                #     row_remap_alert_prefix.alert=False
                # else:
                #     row_remap_alert_prefix.alert=True

                # row_remap_alert_prefix.label(text='Prefix: '+prefix+':')
                # row_remap_alert_prefix.prop(fourd_prop,'str_retarget_prefix')
            row_remap.separator()
            row_remap.prop(scn,'source')
            row_remap.prop(scn,'target')
            row_remap_retarget = row_remap.column()
            if fourd_prop.enum_list_rig == '-1':
                row_remap_retarget.enabled = False
            else:
                row_remap_retarget.enabled = True
            row_remap_retarget.operator('fdh.retarget',text='Bind').option=0 #bind

            row_remap_unbind = row_remap.column()
            if scn.target is not None and scn.target.get('bind') is not None and scn.target['bind'] == 1:
                row_remap_unbind.enabled = True
            else:
                row_remap_unbind.enabled = False
            row_remap_unbind.operator('fdh.retarget',text='Unbind').option=1 #unbind
            row_remap_unbind.separator()
            row_remap_apply_retarget = row_remap.column()
            if scn.target is not None and scn.target.get('bind') is not None and scn.target['bind'] == 1:
                row_remap_apply_retarget.enabled = True
            else:
                row_remap_apply_retarget.enabled = False
            row_remap_apply_retarget.prop(fourd_prop,'bool_retarget_hide_source')
            row_remap_apply_retarget.operator('fdh.retarget',text='Apply Retarget').option=2 #apply

        if fourd_prop.bool_extract_marked_frames_panel:
            rowb = layout.row(align=True).box()
            rowb = rowb.column(align=True)
            rowb_extract_col = rowb.row(align=True)
            rowb_extract_col.label(text='Extract Marked Frames')
            if context.active_object is not None and context.active_object.type == 'ARMATURE':
                rowb_extract_col.operator('fdh.optimize_marker_view')
            rowb_extract_marker = rowb.column()
            if len(bpy.context.scene.timeline_markers) == 0:
                rowb_extract_marker.enabled = False
            else:
                rowb_extract_marker.enabled = True
            rowb_extract_marker.operator('fdh.extract_marked_frames',text='Entire Character')
            if context.active_object is not None and context.active_object.mode == 'POSE' and len(context.selected_pose_bones) > 0 :
                rowb_extract_marker.operator('fdh.extract_marked_frames_for_selected_bones')
            rowb_extract_marker.operator('fdh.clear_markers')

            row_quicksave = rowb
            row_quicksave.label(text='Quick Save/Load')
            row_quicksave.prop(fourd_prop,'bool_clear_before_load_quickload')
            row_qs_ql = row_quicksave.row(align=True)
            row_qs_ql.operator('fdh.quick_save_markers',text='QS 1').option=1
            row_ql = row_qs_ql.row(align=True)
            row_ql.enabled = False if fourd_prop.str_quick_save_marker1 == '' else True
            row_ql.operator('fdh.quick_load_markers',text='QL 1').option=1
            row_ql.operator('fdh.quick_save_markers_clear',text='X').option=1


            row_qs_ql = row_quicksave.row(align=True)
            row_qs_ql.operator('fdh.quick_save_markers',text='QS 2').option=2
            row_ql = row_qs_ql.row(align=True)
            row_ql.enabled = False if fourd_prop.str_quick_save_marker2 == '' else True
            row_ql.operator('fdh.quick_load_markers',text='QL 2').option=2
            row_ql.operator('fdh.quick_save_markers_clear',text='X').option=2


            row_qs_ql = row_quicksave.row(align=True)
            row_qs_ql.operator('fdh.quick_save_markers',text='QS 3').option=3
            row_ql = row_qs_ql.row(align=True)
            row_ql.enabled = False if fourd_prop.str_quick_save_marker3 == '' else True
            row_ql.operator('fdh.quick_load_markers',text='QL 3').option=3
            row_ql.operator('fdh.quick_save_markers_clear',text='X').option=3


            row_qs_ql = row_quicksave.row(align=True)
            row_qs_ql.operator('fdh.quick_save_markers',text='QS 4').option=4
            row_ql = row_qs_ql.row(align=True)
            row_ql.enabled = False if fourd_prop.str_quick_save_marker4 == '' else True
            row_ql.operator('fdh.quick_load_markers',text='QL 4').option=4
            row_ql.operator('fdh.quick_save_markers_clear',text='X').option=4

            row_qs_ql = row_quicksave.column(align=True)
            row_qs_ql.separator()
            row_qs_ql.operator('fdh.quick_save_markers_clear').option=0 #limpa tudo



        # row = layout.box()
        # scn = context.scene
        # row.operator('fdh.append_stg2')
        # row.prop(scn,'target_stg2')
        # row.operator('fdh.stg2_retarget')
        # row.operator('fdh.mr_switch_snap_anim')

        # row = layout.box()
        # row.operator('fdh.stg2_full')

        if fourd_prop.bool_wham:
            row = layout.box()
            row = row.column(align=True)
            row.operator('fdh.add_video_wham')
            text_path = 'Video Path: '+fourd_prop.str_videopath

            _label_multiline(
                context=context,
                text=text_path,
                parent=row
                )
            row_execute_wham = row.column(align=1)

            if not os.path.exists(flag_video_wham):
                row_execute_wham.enabled = False
            else:
                row_execute_wham.enabled = True
            row_execute_wham.prop(fourd_prop,'bool_wham_simplify')
            row_execute_wham.operator('fdh.execute_wham')
            row_execute_wham.separator()
            row_execute_wham.operator('fdh.load_video_3dview')

            row = layout.box()
            row = row.column(align=True)
            row_export_pkl = row.column(align=1)
            row_export_pkl.label(text='Export/Import PKL Animation')
            row_export_pkl_col = row_export_pkl.row(align=1)
            row_export_pkl_col_export = row_export_pkl_col.row(align=1)
            if os.path.exists(flag_wham_pickle):
                row_export_pkl_col_export.enabled = True
            else:
                row_export_pkl_col_export.enabled = False

            row_export_pkl_col_export.operator('fdh.export_animation',text='Export').option=1 #1 for WHAM
            row_export_pkl_col.operator('fdh.import_pkl_animation',text='Import').option=2 #2 for wham
            row_export_pkl.operator('fdh.import_pkl_animation',text='Import Google Colab PKL').option=3 #2 for wham

            row = layout.box()
            row = row.column(align=True)
            row_import_character = row.column(align=1)
            
            if  os.path.exists(flag_wham_pickle) and  os.path.exists(file_fbx):
                row_import_character.enabled = True
                row_import_character.alert = False

            else:
                row_import_character.alert = True
                row_import_character.enabled = False

            row_import_character_col = row_import_character.row(align=1)
            row_import_character_col.label(text='Total Char: '+ str(fourd_prop.int_tot_character))
            row_import_character_col.operator('fdh.read_pkl_data').option=1
            row_import_character.prop(fourd_prop,'int_character')
            row_import_character.label(text='Enable/Disable World')
            # row_import_character_col = row_import_character.row(align=1)
            # if fourd_prop.bool_trans_world:
            #     trans_w_text = 'Wolrd Trans'
            # else:
            #     trans_w_text = 'Local Trans'
            # if fourd_prop.bool_pose_world:
            #     pose_w_text = 'World Pose'
            # else:
            #     pose_w_text = 'Local Pose'

            if fourd_prop.bool_world: # se local, remover oo movimento Z (deixar a opcao)
                world_local_w_text = 'World'
            else:
                world_local_w_text = 'Local'
            # row_import_character_col.prop(fourd_prop,'bool_trans_world',text=trans_w_text,toggle=1)
            # row_import_character_col.prop(fourd_prop,'bool_pose_world',text=pose_w_text,toggle=1)
            row_import_character.prop(fourd_prop,'bool_world',text=world_local_w_text,toggle=1)
            # row_import_character_col.label(text=pose_w_text)
            # row_import_character_col = row_import_character.row(align=1)

            # row_import_character_col.label(text=trans_w_text)
            # row_import_character_col.label(text=pose_w_text)

            row_import_character_col = row_import_character.row(align=1)
            row_import_character_col.label(text='Import')
            if not fourd_prop.bool_world:
                row_import_character_col.prop(fourd_prop,'bool_fix_z',toggle=True)
            row_import_character.operator('fdh.import_character').option=2 #importa wham
            if not os.path.exists(file_fbx):
                row_import_character.label(text='Import the SMPL FBX')
            
            if fourd_prop.bool_ik_control_panel:
                ik_control_panel(context,layout,row,path_venv,file_fbx)

        if fourd_prop.bool_slahmr:
            row = layout.box()
            row = row.column(align=True)
            row.operator('fdh.add_video_slahmr')
            text_path = 'Video Path: '+fourd_prop.str_videopath

            _label_multiline(
                context=context,
                text=text_path,
                parent=row
                )
            row_load_a_video_alert = row.column()
            row_load_video = row.column()
            if fourd_prop.str_videopath == '':
                row_load_video.enabled = False
                row_load_a_video_alert.alert = True
                row_load_a_video_alert.label(text='Load a Video First')
            else:
                row_load_video.enabled = True
            row_load_video.operator('fdh.load_video_3dview')
            
            row = layout.box()
            row = row.column(align=True)
            row.prop(fourd_prop,'int_fps_slahmr')
            row.label(text=str(fourd_prop.int_end_frame_slahmr - fourd_prop.int_ini_frame_slahmr)+' Frames' )
            row_col  = row.row(align=1)
            row_col.prop(fourd_prop,'int_ini_frame_slahmr')
            row_col.prop(fourd_prop,'int_end_frame_slahmr')
            row.operator('fdh.update_slahmr_setting')



            row = layout.box()
            row = row.column(align=True)
            row_execute_slahmr = row.column(align=1)

            # if not os.path.exists(flag_video_slahmr):
            #     row_execute_slahmr.enabled = False
            # else:
            #     row_execute_slahmr.enabled = True


            row_execute_slahmr.operator('fdh.execute_slahmr')
            row_execute_slahmr_col = row_execute_slahmr.row(align = 1)
            row_execute_slahmr_col.operator('fdh.import_zip_animation')
            row_execute_slahmr_col.operator('fdh.export_animation_slahmr')

            row = layout.box()
            row = row.column(align=True)
            row_execute_slahmr = row.column(align=1)
            row_execute_slahmr.prop(fourd_prop,'int_character')
            row_execute_slahmr.operator('fdh.import_character').option=3 #importa slahmr

            if fourd_prop.bool_ik_control_panel:
                ik_control_panel(context,layout,row,path_venv,file_fbx)





        if fourd_prop.bool_4dhumans:
            #############################################
            ### VENV SETTINGS
            #############################################
            rowb = layout.row(align=True).box()
            rowb = rowb.column(align=True)
            row = rowb.row(align=True)
            # row.enabled = enable_ctr
            row.enabled = True
            row.prop(scene, "fourd_venv",
            icon="TRIA_DOWN" if scene.fourd_venv else "TRIA_RIGHT",
            icon_only=True, emboss=False
            )
            row_alert_create_venv = row.column(align=True)
            if os.path.exists(path_venv) and os.path.exists(file_fbx):
                row_alert_create_venv.alert = False
            else:
                row_alert_create_venv.alert = True
            row_alert_create_venv.label(text='Venv and Model 4D Humans') 


            if scene.fourd_venv:
                row = rowb.column(align=True)

                row_path = row.row(align=True)
                row_path2 = row.row(align=True)
                
                if os.path.exists(fourd_prop.str_venv_path):
                    row_path.alert = False
                    row_path2.alert = False
                else:
                    row_path.alert = True
                    row_path2.alert = True
                    row_path.label(text='Select a valid Path')
                
                row_subpath = row.column(align=True)
                if ' ' in path_venv:
                    # row_path2.alert = True
                    row_subpath.alert=True
                else:
                    # row_path2.alert = False
                    row_subpath.alert=False
                row_path2.prop(fourd_prop,'str_venv_path',text = '')
                row_path2.operator('fdh.venv_path_select',text = 'Path')
                _label_multiline(
                context=context,
                text='Full Path: '+path_venv,
                parent=row_subpath
                )
                
                row_subpath.prop(fourd_prop,'bool_custom_venv')
                if fourd_prop.bool_custom_venv:
                    row_subpath = row_subpath.row(align=True)
                    row_subpath.prop(fourd_prop,'bool_custom_venv_name',text='Name',toggle=1)
                    row_subpath.prop(fourd_prop,'bool_custom_venv_name_from_list',text='List',toggle=1)

                    if fourd_prop.bool_custom_venv_name:
                        row_sub_subpath = row.column(align=True)
                        # row_subpath = row_subpath.column(align=True)
                        row_sub_subpath.prop(fourd_prop,'str_custom_venv_name',text='Name')
                    if fourd_prop.bool_custom_venv_name_from_list:
                        row_sub_subpath = row.column(align=True)
                        # row_subpath = row_subpath.column(align=True)
                        row_sub_subpath.prop(fourd_prop,'enum_custom_venv_list',text='Folder')

                    
                row = layout.row().box()
                row_sub = row.column(align=True)

                row_alert_inst_venv_py = row_sub.column(align=True)
                row_alert_create_venv = row_sub.column(align=True)
                row_alert_install_pre_detectron2 = row_sub.column(align=True)
                row_alert_install_pytorch = row_sub.column(align=True)
                row_alert_install_detectron2 = row_sub.column(align=True)
                row_alert_install_cv2_einops = row_sub.column(align=True)
                row_alert_smpl_pkl = row_sub.column(align=True)
                row_reqs = row_sub.column(align=True)
                # row_alert_install_compiler = row_sub.column(align=True)
                # if not os.path.exists(path_venv_pypack):
                #     row_alert_inst_venv_py.alert = True
                # else:
                #     row_alert_inst_venv_py.alert = False

                if not os.path.exists(path_venv):
                    row_alert_create_venv.alert = True
                    row_alert_install_pytorch.enabled = False
                    row_alert_install_cv2_einops.enabled = False
                else:
                    row_alert_create_venv.alert = False
                    row_alert_install_pytorch.enabled = True
                    row_alert_install_cv2_einops.enabled = True

                if not os.path.exists(flag_installed):
                    row_alert_install_pytorch.alert = True
                else:
                    row_alert_install_pytorch.alert = False

                if not os.path.exists(flag_installed_detectron2):
                    row_alert_install_detectron2.alert = True
                else:
                    row_alert_install_detectron2.alert = False

                if not os.path.exists(flag_installed_pre_detectron2):
                    row_alert_install_pre_detectron2.alert = True
                else:
                    row_alert_install_pre_detectron2.alert = False

                if not os.path.exists(flag_installed_pre_detectron2):
                    row_alert_install_pre_detectron2.alert = True
                else:
                    row_alert_install_pre_detectron2.alert = False

                if not os.path.exists(smpl_path) or not os.path.exists(smpl_path2):
                    row_alert_smpl_pkl.alert = True
                else:
                    row_alert_smpl_pkl.alert = False


                if os.path.exists(flag_installed_cv2): #and os.path.exists(flag_installed_einops):
                    row_alert_install_cv2_einops.alert = False
                else:
                    row_alert_install_cv2_einops.alert = True
                
                if ' ' in path_venv:
                    row_space_alert = row_sub.column(align=True)
                    row_space_alert.alert = True
                    row_space_alert.label(text='Choose a Path with no SPACE')
                else:
                    row_alert_create_venv.operator('fdh.create_virtual_env')
                    row_alert_install_pre_detectron2.operator('fdh.install_pre_detectron_venv')
                    row_alert_install_pytorch.operator('fdh.install_pytorch_venv')
                    row_alert_install_detectron2.operator('fdh.install_detectron_venv')
                    row_alert_smpl_pkl.operator('fdh.import_smpl_pkl',text='Import basicModel_neutral_lbs_10_207_0_v1.0.0.pkl').option=3
                    # row_alert_install_cv2_einops.operator('fdh.install_reqs_venv')
                    row = layout.row().box()
                    row = row.column(align=True)
                    row.label(text='Models Offline Install')
                    row.operator('fdh.import_offline_files')
                row = layout.row().box()
                row = row.column(align=True)
                _label_multiline(
                context=context,
                text='If you had problems running 4d humans, please install Microsoft Visual C++ Redistributable, you can use the link below to get it',
                parent=row
                )
                row.operator('wm.url_open',text='MS Visual C++ Redistributable',icon='URL').url = 'https://aka.ms/vs/16/release/vc_redist.x64.exe'
                row = layout.row().box()
                row = row.column(align=True)
                row.label(text='Official Github')
                row.operator('wm.url_open',text='4d Humans Github',icon='URL').url = 'https://github.com/shubham-goel/4D-Humans'
                _label_multiline(
                context=context,
                text='Get the SMPL for Maya (file: SMPL_maya) and extract the file "basicModel_m_lbs_10_207_0_v1.0.2.fbx" to be imported here',
                parent=row
                )
                row.operator('wm.url_open',text='SMPL Page',icon='URL').url = 'https://smpl.is.tue.mpg.de/download.php'
                row_fbx = row.column()
                # file_fbx = os.path.join(path_addon,'basicModel_m_lbs_10_207_0_v1.0.2.fbx') #joguei la pro comeco
                if os.path.exists(file_fbx):
                    row_fbx.alert = False
                else:
                    row_fbx.alert = True
                row_fbx.operator('fdh.import_smpl_fbx')
                row.operator('wm.url_open',text='SMPLify Page',icon='URL').url = 'https://smplify.is.tue.mpg.de/download.php'

                
                # row = layout.row().box()
                # row = row.column(align=True)
                # row.label(text='Optional - Offline Install')
                # row.operator('fdh.import_offline_files')



        if fourd_prop.bool_wham:
            #############################################
            ### VENV SETTINGS
            #############################################
            rowb = layout.row(align=True).box()
            rowb = rowb.column(align=True)
            row = rowb.row(align=True)
            # row.enabled = enable_ctr
            row.enabled = True
            row.prop(scene, "fourd_venv_wham",
            icon="TRIA_DOWN" if scene.fourd_venv_wham else "TRIA_RIGHT",
            icon_only=True, emboss=False
            )
            row_alert_create_venv = row.column(align=True)
            if os.path.exists(path_venv_wham) and os.path.exists(file_fbx):
                row_alert_create_venv.alert = False
            else:
                row_alert_create_venv.alert = True
            row_alert_create_venv.label(text='Venv and Model WHAM') 


            if scene.fourd_venv_wham:
                row = rowb.column(align=True)

                row_path = row.row(align=True)
                row_path2 = row.row(align=True)
                
                if os.path.exists(fourd_prop.str_venv_path):
                    row_path.alert = False
                    row_path2.alert = False
                else:
                    row_path.alert = True
                    row_path2.alert = True
                    row_path.label(text='Select a valid Path')
                
                row_subpath = row.column(align=True)
                if ' ' in path_venv_wham:
                    # row_path2.alert = True
                    row_subpath.alert=True
                else:
                    # row_path2.alert = False
                    row_subpath.alert=False
                row_path2.prop(fourd_prop,'str_venv_path',text = '')
                row_path2.operator('fdh.venv_path_select',text = 'Path')
                _label_multiline(
                context=context,
                text='Full Path: '+path_venv_wham,
                parent=row_subpath
                )
                
                # row_subpath.prop(fourd_prop,'bool_custom_venv')
                # if fourd_prop.bool_custom_venv:
                #     row_subpath = row_subpath.row(align=True)
                #     row_subpath.prop(fourd_prop,'bool_custom_venv_name',text='Name',toggle=1)
                #     row_subpath.prop(fourd_prop,'bool_custom_venv_name_from_list',text='List',toggle=1)

                #     if fourd_prop.bool_custom_venv_name:
                #         row_sub_subpath = row.column(align=True)
                #         # row_subpath = row_subpath.column(align=True)
                #         row_sub_subpath.prop(fourd_prop,'str_custom_venv_name',text='Name')
                #     if fourd_prop.bool_custom_venv_name_from_list:
                #         row_sub_subpath = row.column(align=True)
                #         # row_subpath = row_subpath.column(align=True)
                #         row_sub_subpath.prop(fourd_prop,'enum_custom_venv_list',text='Folder')

                    
                row = layout.row().box()
                row_sub = row.column(align=True)

                # row_alert_inst_venv_py = row_sub.column(align=True)
                row_alert_create_venv_wham = row_sub.column(align=True)
                row_alert_install_pytorch_wham = row_sub.column(align=True)
                row_alert_install_wham = row_sub.column(align=True)
                row_alert_install_bodymodels = row_sub.column(align=True)
                row_alert_install_checkpoints = row_sub.column(align=True)
                
                # row_alert_install_cv2_einops = row_sub.column(align=True)
                row_reqs = row_sub.column(align=True)
                # row_alert_install_compiler = row_sub.column(align=True)
                # if not os.path.exists(path_venv_pypack):
                #     row_alert_inst_venv_py.alert = True
                # else:
                #     row_alert_inst_venv_py.alert = False

                if not os.path.exists(path_venv_wham):
                    row_alert_create_venv_wham.alert = True
                    row_alert_install_pytorch_wham.enabled = False
                    # row_alert_install_cv2_einops.enabled = False
                else:
                    row_alert_create_venv_wham.alert = False
                    row_alert_install_pytorch_wham.enabled = True
                    # row_alert_install_cv2_einops.enabled = True

                if not os.path.exists(flag_installed_wham):
                    row_alert_install_pytorch_wham.alert = True
                else:
                    row_alert_install_pytorch_wham.alert = False

                if not os.path.exists(flag_installed_wham_reqs):
                    row_alert_install_wham.alert = True
                else:
                    row_alert_install_wham.alert = False

                if not os.path.exists(flag_wham_body_models):
                    row_alert_install_bodymodels.alert = True
                else:
                    row_alert_install_bodymodels.alert = False
                
                if os.path.exists(flag_ckp_dpvo_pth) and os.path.exists(flag_ckp_hmr2a_ckpt) and os.path.exists(flag_ckp_vitpose) and os.path.exists(flag_ckp_wham_vit_w) and os.path.exists(flag_ckp_wha_vit_bedlam) and os.path.exists(flag_ckp_yolov8x) :
                    row_alert_install_checkpoints.alert = 0
                else:
                    row_alert_install_checkpoints.alert = 1
                
                if ' ' in path_venv_wham:
                    row_space_alert = row_sub.column(align=True)
                    row_space_alert.alert = True
                    row_space_alert.label(text='Choose a Path with no SPACE')
                else:
                    row_alert_create_venv_wham.operator('fdh.create_virtual_env_wham')
                    row_alert_install_pytorch_wham.operator('fdh.install_pytorch_venv_wham')
                    row_alert_install_wham.operator('fdh.install_wham_venv')
                    row_alert_install_bodymodels.operator('fdh.download_whan_bodymodels')
                    
                    row_alert_install_checkpoints = row_alert_install_checkpoints.column(align=True)
                    r_a_i_ckpt_box = row_alert_install_checkpoints.box()
                    r_a_i_ckpt_box = r_a_i_ckpt_box.column(align=True)

                    r_a_i_ckpt_box.label(text='WHAM Checkpoint')
                    r_a_i_ckpt_box_col = r_a_i_ckpt_box.row(align=True)
                    r_a_i_ckpt_box_col.operator('fdh.download_whan_checkpoints',text='Online')
                    r_a_i_ckpt_box_col.operator('fdh.import_offline_checkpoint_wham',text='Offline')

                    # row_alert_install_checkpoints.operator('fdh.download_whan_checkpoints')
                row = layout.row().box()
                row = row.column(align=True)
                row.label(text='Official Github')
                row.operator('wm.url_open',text='WHAM Github',icon='URL').url = 'https://github.com/yohanshin/WHAM'
                _label_multiline(
                context=context,
                text='Get the SMPL for Maya (file: SMPL_maya) and extract the file "basicModel_m_lbs_10_207_0_v1.0.2.fbx" to be imported here',
                parent=row
                )
                row.operator('wm.url_open',text='SMPL Page',icon='URL').url = 'https://smpl.is.tue.mpg.de/download.php'
                row.operator('wm.url_open',text='Download SMPL FBX',icon='DISK_DRIVE').url = 'https://download.is.tue.mpg.de/download.php?domain=smpl&sfile=SMPL_maya.zip'
                # row.operator('wm.url_open',text='Download SMPL Male/Female',icon='URL').url = 'https://download.is.tue.mpg.de/download.php?domain=smpl&sfile=SMPL_python_v.1.0.0.zip'
                # row_sub = row.column(align=True)
                # row_alert_install_smpl_male = row_sub.column(align=True)
                # row_alert_install_smpl_female = row_sub.column(align=True)
                

                # if not os.path.exists(flag_installed_smpl_male):
                #     row_alert_install_smpl_male.alert = True
                # else:
                #     row_alert_install_smpl_male.alert = False

                # if not os.path.exists(flag_installed_smpl_female):
                #     row_alert_install_smpl_female.alert = True
                # else:
                #     row_alert_install_smpl_female.alert = False

                
                
                # row_alert_install_smpl_male.label(text='Male PKL - basicmodel_m_lbs_10_207_0_v1.0.0.pkl')
                # row_alert_install_smpl_male.operator('fdh.import_smpl_pkl',text='Import "basicmodel_m" Male ').option=0
                # row_sub.separator()
                # row_alert_install_smpl_female.label(text='Female PKL - basicmodel_f_lbs_10_207_0_v1.0.0.pkl')
                # row_alert_install_smpl_female.operator('fdh.import_smpl_pkl',text='Import "basicmodel_f" Female ').option=1
                # row_sub.separator()
                



                row_fbx = row.column()
                # file_fbx = os.path.join(path_addon,'basicModel_m_lbs_10_207_0_v1.0.2.fbx') #joguei la pro comeco
                if os.path.exists(file_fbx):
                    row_fbx.alert = False
                else:
                    row_fbx.alert = True
                row_fbx.operator('fdh.import_smpl_fbx')
                row.operator('wm.url_open',text='SMPLify Page',icon='URL').url = 'https://smplify.is.tue.mpg.de/download.php'
                row.operator('wm.url_open',text='Download SMPL Neutral',icon='DISK_DRIVE').url = 'https://download.is.tue.mpg.de/download.php?domain=smplify&resume=1&sfile=mpips_smplify_public_v2.zip'
                row_sub = row.column(align=True)
                row_alert_install_smpl_neutral = row_sub.column(align=True)

                if not os.path.exists(flag_installed_smpl_neutral):
                    row_alert_install_smpl_neutral.alert = True
                else:
                    row_alert_install_smpl_neutral.alert = False

                row_alert_install_smpl_neutral.label(text='Neutral PKL - basicModel_neutral_lbs_10_207_0_v1.0.0.pkl')
                row_alert_install_smpl_neutral.operator('fdh.import_smpl_pkl',text='Import "basicmodel_neutral" Neutral ').option=2




        if fourd_prop.bool_slahmr:
            #############################################
            ### VENV SETTINGS
            #############################################
            rowb = layout.row(align=True).box()
            rowb = rowb.column(align=True)
            row = rowb.row(align=True)
            # row.enabled = enable_ctr
            row.enabled = True
            row.prop(scene, "fourd_venv_slahmr",
            icon="TRIA_DOWN" if scene.fourd_venv_slahmr else "TRIA_RIGHT",
            icon_only=True, emboss=False
            )
            row_alert_create_venv = row.column(align=True)
            if os.path.exists(path_venv_slahmr) and os.path.exists(file_fbx):
                row_alert_create_venv.alert = False
            else:
                row_alert_create_venv.alert = True
            row_alert_create_venv.label(text='Venv and Model SLAHMR') 


            if scene.fourd_venv_slahmr:
                row = rowb.column(align=True)

                row_path = row.row(align=True)
                row_path2 = row.row(align=True)
                
                if os.path.exists(fourd_prop.str_venv_path):
                    row_path.alert = False
                    row_path2.alert = False
                else:
                    row_path.alert = True
                    row_path2.alert = True
                    row_path.label(text='Select a valid Path')
                
                row_subpath = row.column(align=True)
                if ' ' in path_venv_slahmr:
                    # row_path2.alert = True
                    row_subpath.alert=True
                else:
                    # row_path2.alert = False
                    row_subpath.alert=False
                row_path2.prop(fourd_prop,'str_venv_path',text = '')
                row_path2.operator('fdh.venv_path_select',text = 'Path')
                _label_multiline(
                context=context,
                text='Full Path: '+path_venv_slahmr,
                parent=row_subpath
                )
                

                row = layout.row().box()
                row_sub = row.column(align=True)

                # row_alert_inst_venv_py = row_sub.column(align=True)
                row_alert_create_venv_slahmr = row_sub.column(align=True)
                row_alert_install_pytorch_slahmr = row_sub.column(align=True)
                row_alert_install_slahmr_reqs = row_sub.column(align=True)
                row_alert_install_slahmr_detectron = row_sub.column(align=True)
                row_alert_install_slahmr_rest_venv = row_sub.column(align=True)

                # row_alert_install_checkpoints = row_sub.column(align=True)
                # row_alert_install_bodymodels = row_sub.column(align=True)
                
                # row_alert_install_cv2_einops = row_sub.column(align=True)
                row_reqs = row_sub.column(align=True)

                

                if not os.path.exists(flag_installed_slahmr_detectron2):
                    row_alert_install_slahmr_detectron.alert = True
                else:
                    row_alert_install_slahmr_detectron.alert = False

                

                # if not os.path.exists(flag_installed_wham):
                #     row_alert_install_pytorch_wham.alert = True
                # else:
                #     row_alert_install_pytorch_wham.alert = False

                # if not os.path.exists(flag_installed_wham_reqs):
                #     row_alert_install_wham.alert = True
                # else:
                #     row_alert_install_wham.alert = False

                # if not os.path.exists(flag_wham_body_models):
                #     row_alert_install_bodymodels.alert = True
                # else:
                #     row_alert_install_bodymodels.alert = False
                
                # if os.path.exists(flag_ckp_dpvo_pth) and os.path.exists(flag_ckp_hmr2a_ckpt) and os.path.exists(flag_ckp_vitpose) and os.path.exists(flag_ckp_wham_vit_w) and os.path.exists(flag_ckp_wha_vit_bedlam) and os.path.exists(flag_ckp_yolov8x) :
                #     row_alert_install_checkpoints.alert = 0
                # else:
                #     row_alert_install_checkpoints.alert = 1

                
                if not os.path.exists(path_venv_slahmr):
                    row_alert_create_venv_slahmr.alert = True
                    row_alert_install_pytorch_slahmr.enabled = False
                    row_alert_install_pytorch_slahmr.enabled = False
                    row_alert_install_slahmr_detectron.enabled = False
                    row_alert_install_slahmr_reqs.enabled = False
                    row_alert_install_slahmr_rest_venv.enabled = False
                else:
                    row_alert_create_venv_slahmr.alert = False
                    row_alert_install_pytorch_slahmr.enabled = True
                    row_alert_install_pytorch_slahmr.enabled = True
                    row_alert_install_slahmr_detectron.enabled = True
                    row_alert_install_slahmr_reqs.enabled = True
                    row_alert_install_slahmr_rest_venv.enabled = True

                if not os.path.exists(flag_installed_slahmr_torch):
                    row_alert_install_pytorch_slahmr.alert = True
                else:
                    row_alert_install_pytorch_slahmr.alert = False


                if not os.path.exists(flag_installed_slahmr_reqs):
                    row_alert_install_slahmr_reqs.alert = True
                else:
                    row_alert_install_slahmr_reqs.alert = False

                

                if not os.path.exists(flag_installed_slahmr_lietorch):
                    row_alert_install_slahmr_rest_venv.alert = True
                else:
                    row_alert_install_slahmr_rest_venv.alert = False
                
                

                
                
                if ' ' in path_venv_slahmr:
                    row_space_alert = row_sub.column(align=True)
                    row_space_alert.alert = True
                    row_space_alert.label(text='Choose a Path with no SPACE')
                else:
                    row_alert_create_venv_slahmr.operator('fdh.create_virtual_env_slahmr')
                    row_alert_install_pytorch_slahmr.operator('fdh.install_pytorch_venv_slahmr')
                    row_alert_install_slahmr_detectron.operator('fdh.install_detectron_venv_slahmr')
                    row_alert_install_slahmr_reqs.operator('fdh.install_slahmr_venv_reqs')
                    row_alert_install_slahmr_rest_venv.operator('fdh.install_slahmr_and_rest_venv')
                row = layout.row().box()
                row = row.column(align=True)
                row.operator('wm.url_open',text='Download SLAHMR Dependencies',icon='DISK_DRIVE').url = 'https://drive.google.com/uc?id=1GXAd-45GzGYNENKgQxFQ4PHrBp8wDRlW'
                row.operator('fdh.import_zip_slahmr_dependencies')
                    # row_alert_install_checkpoints
                row = layout.row().box()
                row = row.column(align=True)
                row.label(text='Official Github')
                row.operator('wm.url_open',text='SLAHMR Github',icon='URL').url = 'https://github.com/vye16/slahmr'

                _label_multiline(
                context=context,
                text='Get the SMPL for Maya (file: SMPL_maya) and extract the file "basicModel_m_lbs_10_207_0_v1.0.2.fbx" to be imported here',
                parent=row
                )
                row.operator('wm.url_open',text='SMPL Page',icon='URL').url = 'https://smpl.is.tue.mpg.de/download.php'
                row.operator('wm.url_open',text='Download SMPL FBX',icon='DISK_DRIVE').url = 'https://download.is.tue.mpg.de/download.php?domain=smpl&sfile=SMPL_maya.zip'
                # row.operator('wm.url_open',text='Download SMPL Male/Female',icon='URL').url = 'https://download.is.tue.mpg.de/download.php?domain=smpl&sfile=SMPL_python_v.1.0.0.zip'
                # row_sub = row.column(align=True)
                # row_alert_install_smpl_male = row_sub.column(align=True)
                # row_alert_install_smpl_female = row_sub.column(align=True)
                

                # if not os.path.exists(flag_installed_smpl_male):
                #     row_alert_install_smpl_male.alert = True
                # else:
                #     row_alert_install_smpl_male.alert = False

                # if not os.path.exists(flag_installed_smpl_female):
                #     row_alert_install_smpl_female.alert = True
                # else:
                #     row_alert_install_smpl_female.alert = False

                
                
                # row_alert_install_smpl_male.label(text='Male PKL - basicmodel_m_lbs_10_207_0_v1.0.0.pkl')
                # row_alert_install_smpl_male.operator('fdh.import_smpl_pkl',text='Import "basicmodel_m" Male ').option=0
                # row_sub.separator()
                # row_alert_install_smpl_female.label(text='Female PKL - basicmodel_f_lbs_10_207_0_v1.0.0.pkl')
                # row_alert_install_smpl_female.operator('fdh.import_smpl_pkl',text='Import "basicmodel_f" Female ').option=1
                # row_sub.separator()
                



                row_fbx = row.column()
                # file_fbx = os.path.join(path_addon,'basicModel_m_lbs_10_207_0_v1.0.2.fbx') #joguei la pro comeco
                if os.path.exists(file_fbx):
                    row_fbx.alert = False
                else:
                    row_fbx.alert = True
                row_fbx.operator('fdh.import_smpl_fbx')
                # row.operator('wm.url_open',text='SMPLify Page',icon='URL').url = 'https://smplify.is.tue.mpg.de/download.php'
                # row.operator('wm.url_open',text='Download SMPL Neutral',icon='DISK_DRIVE').url = 'https://download.is.tue.mpg.de/download.php?domain=smplify&resume=1&sfile=mpips_smplify_public_v2.zip'
                # row_sub = row.column(align=True)
                # row_alert_install_smpl_neutral = row_sub.column(align=True)

                # if not os.path.exists(flag_installed_smpl_neutral):
                #     row_alert_install_smpl_neutral.alert = True
                # else:
                #     row_alert_install_smpl_neutral.alert = False

                # row_alert_install_smpl_neutral.label(text='Neutral PKL - basicModel_neutral_lbs_10_207_0_v1.0.0.pkl')
                # row_alert_install_smpl_neutral.operator('fdh.import_smpl_pkl',text='Import "basicmodel_neutral" Neutral ').option=2


                
                # row = layout.row().box()
                # row = row.column(align=True)
                # row.label(text='Optional - Offline Install')
                # row.operator('fdh.import_offline_files')

from bpy.props import (StringProperty,
                        BoolProperty,
                        FloatProperty,
                        IntProperty,
                        EnumProperty
                    )
from bpy.types import (PropertyGroup)

class PIXELMySettings(PropertyGroup):
    global DEFAULT_NAME
    #venv Path
    path_addon = os.path.dirname(os.path.abspath(__file__))
    path_venv_path_txt = join(path_addon,'venv_path.txt')
    env_has_path_txt = 0
    if os.path.exists(path_venv_path_txt):
        with open(path_venv_path_txt, "rt") as fin:
            for line in fin:
                env_has_path_txt = 1
                path_txt = line
            if env_has_path_txt ==0:
                path_txt = ''
    else:
        path_txt = ''

    str_venv_path: StringProperty(name="Venv Path", description="Place to install/use Venv",default = path_txt)
    
    str_custom_venv_name: StringProperty(name='Name',default=DEFAULT_NAME,update=updt_custom_venv_name)
    str_custom_venv_name_wham: StringProperty(name='Name',default=DEFAULT_NAME_WHAM,update=updt_custom_venv_name)
    str_custom_venv_name_slahmr: StringProperty(name='Name',default=DEFAULT_NAME_SLAHMR,update=updt_custom_venv_name)
    bool_custom_venv: BoolProperty(name='Custom venv',default=False,update=updt_bool_custom_venv)
    
    bool_custom_venv_name: BoolProperty(name='Custom venv Name',default=False,update=updt_bool_venv_custom_name)
    bool_custom_venv_name_from_list: BoolProperty(name='Custom venv Name from List',default=False,update=updt_bool_venv_custom_name_from_list)
    enum_custom_venv_list : EnumProperty(
        name="Folder",
        description="Select Existing compatible folder.",
        items=folder_venv_callback,
        update=update_venv_name_from_list
        )
    
    int_tot_character: IntProperty(name='Total of Characters',default=0,min=0)
    int_character: IntProperty(name='Character',default=1, min=1)
    str_list_characters: StringProperty(name='Character List')
    int_gpu: IntProperty(name='GPU id',default=0, min=0)
    bool_fix_z: BoolProperty(name='Fix Z Location',default=True)
    str_videopath: StringProperty(name='Video to process',default='')
    str_pklpath: StringProperty(name='PKL to import',default='')
    enum_fps : EnumProperty(
        name="FPS",
        description="Choose a FPS.",
        items=[
            ("24","24","24"),
            ("25","25","25"),
            ("30","30","30"),
            ("50","50","50"),
            ("60","60","60"),
            ("120","120","120"),
        ],
        update=update_fps
        )
    bool_selected_bones: BoolProperty(name='Only Selected Bones',default=False)
    str_nla_name: StringProperty(name='Name',default='Action')
    int_frames_transition: IntProperty(name='Frames',default=5)
    bool_use_selected_character: BoolProperty(name='Use selected character',default=False)


    bool_4dhumans: BoolProperty(name='Show 4Dhumans',default=False)
    bool_wham: BoolProperty(name='Show WHAM',default=False)
    bool_slahmr: BoolProperty(name='Show SLAHMR',default=False)
    bool_core_panel: BoolProperty(name='Show Core Panel',default=True)
    bool_core_exe_panel: BoolProperty(name='Show Core Panel',default=True)
    bool_core_imp_exp_panel: BoolProperty(name='Show Core Panel',default=True)
    bool_core_load_panel: BoolProperty(name='Show Core Panel',default=True)
    bool_core_smooth_panel: BoolProperty(name='Show Smooth Panel',default=False)
    bool_smooth_panel: BoolProperty(name='Show Smooth Panel',default=True)
    bool_footlock_panel: BoolProperty(name='Show Foot Lock Panel',default=False)
    bool_export_panel: BoolProperty(name='Show Export Panel',default=False)
    bool_nla_action_panel: BoolProperty(name='Show NLA Action Panel',default=False)
    bool_nla_track_panel: BoolProperty(name='Show NLA Track Panel',default=False)
    bool_retarget_panel: BoolProperty(name='Show Retarget Panel',default=False)
    bool_extract_marked_frames_panel: BoolProperty(name='Show Extract Marked Frames Panel',default=False)
    bool_ik_control_panel: BoolProperty(name='Show IK Control Panel',default=True)

    bool_nla_selection_tools: BoolProperty(name='Show NLA Selection tools Panel',default=False)
    bool_retarget_hide_source: BoolProperty(name='Hide Source After Retarget',default=True)
    enum_list_rig : EnumProperty(
        name="Rig",
        description="Select desired RIG",
        items=rig_list_callback,
        )
    str_retarget_prefix: StringProperty(name='Retarget Prefix',default='mixamorig:')
    
    ### Floor setup
    fl_floor_distance_fine_tune: FloatProperty(name='Floor Fine Tune',default=0.061255,update=floor_distance_fine_tune)
    int_fadein_foot_lock_frames: IntProperty(name='Frames',default=3)
    int_fadeout_foot_lock_frames: IntProperty(name='Frames',default=3)
    
    bool_pose_world: BoolProperty(name='Pose',default=True)
    bool_trans_world: BoolProperty(name='Translation',default=True)
    bool_world: BoolProperty(name='World',default=True)
    int_fps_slahmr: IntProperty(name='FPS',default=30)
    int_ini_frame_slahmr: IntProperty(name='Start',default=0)
    int_end_frame_slahmr: IntProperty(name='End',default=0)

    ### Marked Frames quicksave
    bool_clear_before_load_quickload: BoolProperty(name='Clear before load',default=True)
    str_quick_save_marker1: StringProperty(name='Quick Save Marker 1')
    str_quick_save_marker2: StringProperty(name='Quick Save Marker 2')
    str_quick_save_marker3: StringProperty(name='Quick Save Marker 3')
    str_quick_save_marker4: StringProperty(name='Quick Save Marker 4')

    bool_wham_simplify: BoolProperty(name='Run Simplify',default=True)



    


