
import numpy as np
from pyCGM_Single.pycgmStatic import pelvisJointCenter

import os
import pyCGM_Single.c3d as c3d
import pyCGM_Single.c3dold as c3dold
import pyCGM_Single.pycgmCalc as pycgmCalc

cwd = os.getcwd()
if (cwd.split(os.sep)[-1] == "pyCGM_Single"):
    parent = os.path.dirname(cwd)
    os.chdir(parent)
cwd = os.getcwd()

# dynamic_trial, static_trial, vsk_file, _, _ = pyCGM_Helpers.getfilenames(x=2)

def loadC3D(filename):
    reader = c3d.Reader(open(filename, 'rb'))

    labels = reader.get('POINT:LABELS').string_array
    mydict = {}
    mydictunlabeled ={}
    data = []
    dataunlabeled = []
    prog_val = 1
    counter = 0
    data_length = reader.last_frame - reader.first_frame
    markers=[str(label.rstrip()) for label in labels]

    for frame_no, points, analog in reader.read_frames(True):
        for label, point in zip(markers, points):
            #Create a dictionary with format LFHDX: 123
            point = point[:3]
            if label[0]=='*':
                if point[0]!=np.nan:
                    mydictunlabeled[label]=point
            else:
                mydict[label] = point
        data.append(mydict)
        dataunlabeled.append(mydictunlabeled)
        mydict = {}
        mydictunlabeled ={}
    return [data,dataunlabeled,markers]

def loadC3DOld(filename):
    reader = c3dold.Reader(open(filename, 'rb'))

    labels = reader.get('POINT:LABELS').string_array
    mydict = {}
    mydictunlabeled ={}
    data = []
    dataunlabeled = []
    prog_val = 1
    counter = 0
    data_length = reader.last_frame() - reader.first_frame()
    markers=[str(label.rstrip()) for label in labels]

    for frame_no, points, analog in reader.read_frames(True, True):
        for label, point in zip(markers, points):
            #Create a dictionary with format LFHDX: 123
            point = point[:3]
            if label[0]=='*':
                if point[0]!=np.nan:
                    mydictunlabeled[label]=point
            else:
                mydict[label] = point
        data.append(mydict)
        dataunlabeled.append(mydictunlabeled)
        mydict = {}
        mydictunlabeled ={}
    return [data,dataunlabeled,markers]

import json
data = loadC3DOld("SampleData/ROM/Sample_Static.c3d")

for item in data:
    for a in item:
        print(a)

# loadC3D("SampleData/ROM/Sample_Static.c3d", c3dold.Reader)
# print(static_trial)
# motion_data = pycgmIO.loadData(os.path.join(cwd, static_trial))
# vsk_data = pycgmIO.loadVSK(os.path.join(cwd, vsk_file), dict=False)


# frame = {'RASI': np.array([ 395.36532593,  428.09790039, 1036.82763672]),
#          'LASI': np.array([ 183.18504333,  422.78927612, 1033.07299805]),
#          'RPSI': np.array([ 341.41815186,  246.72117615, 1055.99145508]),
#          'LPSI': np.array([ 255.79994202,  241.42199707, 1057.30065918]) }
# pelvisJointCenter(frame) #doctest: +NORMALIZE_WHITESPACE

# # frame = {'RASI': np.array([ 395.36532593,  428.09790039, 1036.82763672]),
# #          'LASI': np.array([ 183.18504333,  422.78927612, 1033.07299805]),
# #          'SACR': np.array([ 294.60904694,  242.07158661, 1049.64605713]) }
# # pelvisJointCenter(frame) #doctest: +NORMALIZE_WHITESPACE
# result = pycgmStatic.getStatic(motion_data, vsk_data)