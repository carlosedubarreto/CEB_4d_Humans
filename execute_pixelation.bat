call "D:\AI_VENV_PIXEL\py39_torch1.12.1_cu116_env\Scripts\activate.bat"
cd 4D-Humans-main
python test.py --gpu_ids 0 --batch_size 1 --preprocess none --num_test 4 --epoch 160 --dataroot ./datasets/TEST_DATA/ --name pixelart_vgg19