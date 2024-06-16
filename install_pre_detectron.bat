call "D:\AI_VENV_4D_TEST\py310_torch1.13.0_cu117_env\Scripts\activate.bat"
set python_include="C:\Users\carlo\AppData\Roaming\Blender Foundation\Blender\4.1\scripts\addons\CEB_4d_Human\python_source\include"
set python_pc="C:\Users\carlo\AppData\Roaming\Blender Foundation\Blender\4.1\scripts\addons\CEB_4d_Human\python_source\PC"
set python_libs="C:\Users\carlo\AppData\Roaming\Blender Foundation\Blender\4.1\scripts\addons\CEB_4d_Human\python_source\libs"
set INCLUDE=%python_include%;%python_pc%;%INCLUDE%
set LIB=%python_libs%;%LIB%
python -mpip install pywin32==305
python -mpip install Cython
python -mpip install git+https://github.com/facebookresearch/fvcore
C:
cd "\Users\carlo\AppData\Roaming\Blender Foundation\Blender\4.1\scripts\addons\CEB_4d_Human"
python -mpip install pycocotools-2.0-cp310-cp310-win_amd64.whl
python -mpip install av==10.0.0
python -mpip install scipy==1.10.0
python -mpip install ninja
@echo -----------------------------------------------
@echo --------- YOU CAN CLOSE THIS WINDOW  ----------
@echo -----------------------------------------------