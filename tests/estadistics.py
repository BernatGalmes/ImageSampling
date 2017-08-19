import json
import xml.etree.ElementTree as ET

import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import pylab as pl

from Core.Stats import Stats
from Core.utils import *
from tests.Latex_figure import LatexFigure


# TODO: calculs de tots els estadistics que puguin ser utils
def getStatistics(stats):
    return {
        "mean": str(stats.mean()),
        'std': str(stats.std()),
        "ic": {
            "85": stats.confidence_interval(0.85),
            "90": stats.confidence_interval(0.90),
            "95": stats.confidence_interval(0.95),
            "99": stats.confidence_interval(0.99),
        }
    }


# call plt.show before this call
def distNorm(data, label):
    data = sorted(data)
    pdf = mlab.normpdf(data, np.mean(data), np.std(data))
    plt.plot(data, pdf, label=label)  # including h here is crucial
    pl.hist(data, bins=40,normed=True)  # use this to draw histogram of your data

def plotNorm(data, nameData, title):
    plt.xlabel('Values')
    plt.ylabel('Probability')
    plt.title(title)
    distNorm(data, nameData)
    plt.xlim([0, 255])
    #plt.ylim([0, 3800])
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)


def plotData(data, attrs, pref):
    figure = LatexFigure(0.9)
    for at in attrs:
        figure.plotNorm(data[at], at, at, True)

    figure.save('colors_diag_'+ pref + '_full')

    for at in attrs:
        figure = LatexFigure(0.9)
        figure.plotNorm(data[at], at, at)
        figure.save('colors_diag_'+pref+'_' + at + 'Channel')



def plotHSV(hsv):
    figure = LatexFigure(0.9)

    figure.plotNorm(hsv['h'], "h", "h", True)
    figure.ax.set_xlim([0, 179])
    figure.plotNorm(hsv['s'], "s", "s", True)
    figure.plotNorm(hsv['v'], "v", "v", True)
    figure.save('colors_diag_'+ version +'_hsv_full')

    figure = LatexFigure(0.9)
    figure.plotNorm(hsv['h'], "h", "h")
    figure.ax.set_xlim([0, 179])
    figure.save('colors_diag_'+ version +'_hsv_hChannel')

    figure = LatexFigure(0.9)
    figure.plotNorm(hsv['s'], "s", "s")
    figure.save('colors_diag_'+ version +'_hsv_sChannel')

    figure = LatexFigure(0.9)
    figure.plotNorm(hsv['v'], "v", "v")
    figure.save('colors_diag_'+ version +'_vChannel')
    #
    # # TODO: change xlim hue channel
    # plotData(hsv, ['h', 's', 'v'], 'hsv')

def plot(lab, bgr, hsv):
    plotData(lab, ['L', 'a', 'b'], version +'_lab')
    plotData(bgr, ['b', 'g', 'r'], version +'_rgb')

    plotHSV(hsv)


def getInfo(data):
    return {
        "nPix": len(data.findall('.//pix'))
    }

def getData (xml, nodes, attrs):
    nodes = xml.findall('.//' + nodes)

    data = {}
    for at in attrs:
        data[at] = np.asarray(attr2List(nodes, at)).astype("float32")
    print (nodes)
    return data

def getStats (data, attrs):
    res = {}
    for at in attrs:
        res[at] = getStatistics(Stats(data[at]))

    return res


def retrieveStadistics(path_datafile, path_outputfile):
    # retrieve data
    data = ET.ElementTree()
    data.parse(path_datafile)
    root_meta = data.getroot()
    res = dictlist(root_meta)

    # build data structures
    lab = getData(data, 'lab', ['L', 'a', 'b'])
    if version == 'v1':
        rgb = getData(data, 'bgr', ['r', 'g', 'b'])
    else:
        rgb = getData(data, 'rgb', ['r', 'g', 'b'])
    hsv = getData(data, 'hsv', ['h', 's', 'v'])

    # get statistics
    statLab = getStats(lab, ['L', 'a', 'b'])
    statRGB = getStats(rgb, ['r', 'g', 'b'])
    statHSV = getStats(hsv, ['h', 's', 'v'])

    # plot graphs
    plot(lab, rgb, hsv)
    # plotAll(lab, rgb, hsv)

    # write statistics to a file
    data = {'lab': statLab, 'rgb': statRGB, 'hsv': statHSV, 'info': getInfo(data)}
    json.dumps(data)
    print(data)
    with open(path_outputfile, 'w') as outputFile:
        json.dump(data, outputFile)


if __name__ == "__main__":
    version = 'v2'
    if version == 'v1':
        filename = os.path.dirname(os.path.abspath(__file__)) + '/results/values/data_v1.xml'
        outputFilename = os.path.dirname(os.path.abspath(__file__)) + '/results/values/estadistics_v1.json'
    else:
        filename = os.path.dirname(os.path.abspath(__file__)) + '/results/values/data.xml'
        outputFilename = os.path.dirname(os.path.abspath(__file__)) + '/results/values/estadistics.json'

    retrieveStadistics(filename, outputFilename)








