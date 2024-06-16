call "D:\AI_VENV_WHAM\py39_torch1.11.0_cu113_env\Scripts\activate.bat"
C:
cd "\Users\carlo\AppData\Roaming\Blender Foundation\Blender\4.0\scripts\addons\CEB_4d_Human"
cd "WHAM"
if not exist "checkpoints" mkdir checkpoints
if not exist "checkpoints/wham_vit_w_3dpw.pth.tar" gdown "https://drive.google.com/uc?id=1i7kt9RlCCCNEW2aYaDWVr-G778JkLNcB&export=download&confirm=t" -O "checkpoints/wham_vit_w_3dpw.pth.tar"
if not exist "checkpoints/wham_vit_bedlam_w_3dpw.pth.tar" gdown "https://drive.google.com/uc?id=19qkI-a6xuwob9_RFNSPWf1yWErwVVlks&export=download&confirm=t" -O "checkpoints/wham_vit_bedlam_w_3dpw.pth.tar"
if not exist "checkpoints/hmr2a.ckpt" gdown "https://drive.google.com/uc?id=1J6l8teyZrL0zFzHhzkC7efRhU0ZJ5G9Y&export=download&confirm=t" -O "checkpoints/hmr2a.ckpt"
if not exist "checkpoints/dpvo.pth" gdown "https://drive.google.com/uc?id=1kXTV4EYb-BI3H7J-bkR3Bc4gT9zfnHGT&export=download&confirm=t" -O "checkpoints/dpvo.pth"
if not exist "checkpoints/yolov8x.pt" gdown "https://drive.google.com/uc?id=1zJ0KP23tXD42D47cw1Gs7zE2BA_V_ERo&export=download&confirm=t" -O "checkpoints/yolov8x.pt"
if not exist "checkpoints/vitpose-h-multi-coco.pth" gdown "https://drive.google.com/uc?id=1xyF7F3I7lWtdq82xmEPVQ5zl4HaasBso&export=download&confirm=t" -O "checkpoints/vitpose-h-multi-coco.pth"
@echo -----------------------------------------------
@echo --------- YOU CAN CLOSE THIS WINDOW  ----------
@echo -----------------------------------------------