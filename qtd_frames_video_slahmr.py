import cv2,os

path_addon = os.path.dirname(os.path.abspath(__file__))
        
# base_path_img = os.path.join(path_addon,'4D-Humans-main','datasets','TEST_DATA')
# path_file = os.path.join(path_addon,'4D-Humans-main','example_data','videos')
path_file = os.path.join(path_addon,'slahmr','data_input','videos')


# vid = os.path.join(path_file,'video.mp4')
vid = os.path.join(path_file,'video_slahmr.mp4')

cap = cv2.VideoCapture(vid)
length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
fps = int(cap.get(cv2.CAP_PROP_FPS))
print( str(length)+"|"+str(fps)+"|")
# name = 'qtd_frames.txt'
# with open(os.path.join(path_addon,name), "wt") as fout:
#     fout.write(str(length))
