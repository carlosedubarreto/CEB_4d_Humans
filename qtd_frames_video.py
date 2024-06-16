import cv2,os

path_addon = os.path.dirname(os.path.abspath(__file__))
        
# base_path_img = os.path.join(path_addon,'4D-Humans-main','datasets','TEST_DATA')
path_file = os.path.join(path_addon,'4D-Humans-main','example_data','videos')


vid = os.path.join(path_file,'video.mp4')

cap = cv2.VideoCapture(vid)
length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
print( length )
# name = 'qtd_frames.txt'
# with open(os.path.join(path_addon,name), "wt") as fout:
#     fout.write(str(length))
