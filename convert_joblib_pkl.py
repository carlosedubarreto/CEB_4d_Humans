import joblib
import pickle
import os

path_addon = os.path.dirname(os.path.abspath(__file__))
base_file = os.path.join(path_addon,'4D-Humans-main','outputs','results')
file = os.path.join(base_file,'demo_video.pkl')
file_converted = os.path.join(base_file,'demo_video_converted.pkl')
results = joblib.load(file)


with open(file_converted, 'wb') as handle:
   pickle.dump(results, handle, protocol=pickle.HIGHEST_PROTOCOL)
   
# with open('filename.pickle', 'rb') as handle:
#    b = pickle.load(handle)