import os
import numpy as np
import random

"""
    FILE SYSTEM FUNCTIONS
"""


def check_dir(path):
    """
    Check if the specified path exists into file system. If not exists, it is created
    :param path: String
    :return:
    """
    if not os.path.exists(path):
        os.makedirs(path)


"""
    GENERAL UTILS
"""


def get_rand_points(point, num=10, width=30):
    """
    Performs an automatic thresholding based on otsu method. Useful for blue channel segmentation

    Parameters
    ----------
    point : seed of the point generator

    num: number of points to generate

    width: amplitude of the square where to generate new points

    Returns
    -------
    points : 2d integer point list
    """

    random.seed(10)

    points = np.zeros([num, 2])

    points[:, 0] = point[0] + np.random.randint(-width, width, num)  # generate num x coordinates
    points[:, 1] = point[1] + np.random.randint(-width, width, num)  # generate num y coordinates

    return points.astype('int')

def image_distances(image, value):
    if image.shape[2] != len(value):
        raise Exception("image and value hasn't got the correct size")
    i2 = np.full(image.shape, value)
    m1 = image - i2
    return np.linalg.norm(m1, axis=2)  # imatge amb les distancies


def image_distances_2(image, val):
    image_2 = image[:,:,(1,2)]
    return image_distances(image_2, val)


def image_distances_1(image, value):
    i2 = np.full(image.shape, value)
    m1 = image - i2
    return np.absolute(m1)


# currently not used, used to test confidence intervals
def study_range(image, vInf, vSup):
    """
    Build a binary mask where pixels that are between vInf and vSup are 1
    :param image:
    :param vInf:
    :param vSup:
    :return:
    """
    shape = image.shape
    img_bin = np.zeros((shape[0], shape[1]))
    for i in range(0, shape[0]):
        for j in range(0, shape[0]):
            pix = image[i, j]
            if np.greater_equal(pix, vInf).all() and np.less_equal(pix, vSup).all():
                img_bin[i, j] = 255
            else:
                img_bin[i, j] = 0

    return img_bin


"""
    XML UTILS
"""


def xmltodict(node, res):
    rep = {}

    if len(node):
        # n = 0
        for n in list(node):
            rep[node.tag] = []
            value = xmltodict(n, rep[node.tag])
            if len(n):

                value = {'value': rep[node.tag], 'attributes': n.attrib, 'tail': n.tail}
                res.append({n.tag: value})
            else:

                res.append(rep[node.tag][0])

    else:

        value = {}
        value = {'value': node.text, 'attributes': node.attrib, 'tail': node.tail}

        res.append({node.tag: value})

    return

def attr2List(data, attr):
    res=[]
    for item in data:
        res.append(item.attrib[attr])
    return res

def dictlist(node):
    res = {}
    res[node.tag] = []
    xmltodict(node, res[node.tag])
    reply = {}
    reply[node.tag] = {'value': res[node.tag], 'attribs': node.attrib, 'tail': node.tail}

    return reply
