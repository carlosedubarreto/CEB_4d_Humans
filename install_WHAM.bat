call "D:\AI_VENV_4D_TEST\py39_torch1.11.0_cu113_env\Scripts\activate.bat"
C:
cd "\Users\carlo\AppData\Roaming\Blender Foundation\Blender\4.1\scripts\addons\CEB_4d_Human"
cd "WHAM"
python -mpip install -r requirements_wham.txt
python -mpip install mmpose-0.24.0-py2.py3-none-any.whl
python -mpip install dpvo-0.0.0-cp39-cp39-win_amd64.whl
@echo -----------------------------------------------
@echo --------- YOU CAN CLOSE THIS WINDOW  ----------
@echo -----------------------------------------------