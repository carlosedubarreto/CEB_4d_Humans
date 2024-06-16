import os
import pickle
import dill


def convert_pkl(old_pkl):
    # Code adapted from https://github.com/nkolot/ProHMR
    # Convert SMPL pkl file to be compatible with Python 3
    # Script is from https://rebeccabilbro.github.io/convert-py2-pickles-to-py3/

    # Make a name for the new pickle
    new_pkl = os.path.splitext(os.path.basename(old_pkl))[0]+"_p3.pkl"

    # Convert Python 2 "ObjectType" to Python 3 object
    dill._dill._reverse_typemap["ObjectType"] = object

    # Open the pickle using latin1 encoding
    with open(old_pkl, "rb") as f:
        loaded = pickle.load(f, encoding="latin1")

    # Re-save as Python 3 pickle
    with open(new_pkl, "wb") as outfile:
        pickle.dump(loaded, outfile)

path_addon = os.path.dirname(os.path.abspath(__file__))
old_pkl = os.path.join(path_addon,'basicModel_neutral_lbs_10_207_0_v1.0.0.pkl')
convert_pkl(old_pkl)