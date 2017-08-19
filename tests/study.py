from .Latex_figure import LatexFigure
import json
import cv2 as cv2

from Core.utils import *
from Core.Dataset import Dataset

"""
    PROGRAM CONSTANTS
"""

fileData = 'mostreig/results/values/data_v1.xml'
fileMetadata = 'mostreig/results/values/metadata.xml'
fileStats = 'mostreig/results/values/estadistics_v1.json'
folder_results = "mostreig/results/images/study"

datasets = ["24012017","marina"]
"""
Contingut de les imatges amb cieLAB:

Valors python
8-bit images: L <-- L∗255/100,a <-- a+128,b <-- b+128

Valors reals
L --> 0 - 100
a --> -127 a 127
b --> -127 a 127
estudiar si donaria informacio convertirlos als valors reals
"""

#
# def testIC(sample, image, ic0, ic1, ic2, name):
#     for ic in ['85', '90', '95', '99']:
#         img_bin = study_range(image, [ic0[ic][0], ic1[ic][0], ic2[ic][0]], [ic0[ic][1], ic1[ic][1], ic2[ic][1]])
#         f.saveFig(img_bin, folder_results + "/ic_"+name+"_" + ic + "_" + sample.sampleName)



if __name__ == "__main__":
    with open(fileStats) as statsFile:
        data = json.load(statsFile)

    print(data)

    for dataset in datasets:
        ds = Dataset(dataset)
        ds.studying(data)

