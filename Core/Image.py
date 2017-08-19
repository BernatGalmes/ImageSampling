import os
import cv2
import matplotlib.pyplot as plt

from Core.Mostra import Mostra
from Core.DataFiles import DataFiles
from Core.utils import *
from Core.Config import Config
class Image:

    # Colors adjusted to Opencv interpretation of Lab
    # OpenCV CIELab normalisation: L←L∗255/100,a←a+128,b←b+128
    colors_lab = {'red': (127.5, 204.50, 192.19), 'blue': (127.5, 172.47, 51.24), 'green': (127.5, 73.16, 181.24),
                  'white': (255, 128, 128), 'black': (0, 128, 128)}

    colors_rgb = {'red': (240, 0, 0), 'blue': (100, 100, 255), 'green': (0, 140, 0), 'white': (255, 255, 255),
                  'black': (0, 0, 0)}

    inv_colors_rgb = {(240, 0, 0): 'red', (100, 100, 255): 'blue', (0, 140, 0): 'green', (255, 255, 255): 'white',
                      (0, 0, 0): 'black'}

    inv_colors_lab = {(127.5, 204.50, 192.19): 'red', (127.5, 172.47, 51.24): 'blue', (127.5, 73.16, 181.24): 'green',
                      (255, 128, 128): 'white', (0, 128, 128): 'black'}

    def __init__(self, file_path):
        self.file_path = file_path

        # Original image
        self.bgr = cv2.imread(file_path).astype("uint8")   # BGR
        if self.bgr is None:
            raise Exception("not a valid image file")
        self.rgb = cv2.cvtColor(self.bgr, cv2.COLOR_BGR2RGB).astype("uint8")
        self.lab = cv2.cvtColor(self.rgb, cv2.COLOR_RGB2Lab).astype("float32")  # np.copy(sample.original_bgr)
        self.hsv = cv2.cvtColor(self.rgb, cv2.COLOR_RGB2HSV).astype("float32")  # np.copy(sample.original_bgr)


    def name(self):
        return os.path.basename(self.file_path)

    def mostrejar(self, node_img, node_meta):

        # load images and mid point
        mid = [self.bgr.shape[0] / 2, self.bgr.shape[1] / 2]

        mostreig = Mostra(self.name(), self.bgr, self.rgb, mid)

        mid_node = node_meta.find('mid')
        amp_node = node_meta.find('amp')

        # comprovam si tenim les seves dades guardades
        if mid_node is not None and amp_node is not None:
            print("authomatic")
            mid = [float(mid_node.attrib['x']), float(mid_node.attrib['y'])]
            amp = float(amp_node.attrib['val'])
            mostreig.setData(mid, amp)
            mostreig.correct = True
            mostreig.imageProces()
            mostreig.registreDades(node_img)
            return None

        while True:
            mostreig.imageProces()

            if mostreig.discard:
                return None

            elif mostreig.correct:
                DataFiles.registreMeta(node_meta, mostreig.mid, mostreig.amp)
                mostreig.registreDades(node_img)
                return mostreig


    def generate_distances2mean(self, stats):
        stats_rgb = stats['rgb']
        stats_lab = stats['lab']
        stats_hsv = stats['hsv']
        mean_rgb = (stats_rgb['r']['mean'], stats_rgb['g']['mean'], stats_rgb['b']['mean'])
        mean_lab = (stats_lab['L']['mean'], stats_lab['a']['mean'], stats_lab['b']['mean'])
        mean_hsv = (stats_hsv['h']['mean'], stats_hsv['s']['mean'], stats_hsv['v']['mean'])

        distances_rgb = image_distances(self.rgb, mean_rgb)
        distances_lab = image_distances(self.lab, mean_lab)
        distances_lab_ab = image_distances_2(self.lab, [mean_lab[1], mean_lab[2]])
        distances_hsv = image_distances(self.hsv, mean_hsv)
        distances_hue = image_distances_1(self.hsv[:, :, 1], [mean_hsv[1]])

        folder_distances = Config.DEFAULT_FOLDER_RESULTS_DISTS
        check_dir(folder_distances)

        self.plot_image_distances(distances_lab_ab,
                     folder_distances + "dist_lab_ab_" + self.name(), 1)
        self.plot_image_distances(distances_lab,
                     folder_distances + "dist_lab_" + self.name(), 1)

        self.plot_image_distances(distances_rgb,
                     folder_distances + "dist_rgb_" + self.name(), 1)

        self.plot_image_distances(distances_hsv,
                     folder_distances + "dist_hsv_" + self.name(), 1)

        self.plot_image_distances(distances_hue,
                     folder_distances + "dist_hsv_hue_" + self.name(), 1)

        return distances_rgb, distances_lab, distances_hsv

    def plot_image_distances(self, image, filename=None, type=0):
        plt.title(self.name())
        plt.imshow(image)
        plt.colorbar()
        if filename is not None:
            plt.savefig(filename, bbox_inches='tight')
        else:
            plt.show()
        plt.clf()


    @staticmethod
    def __display_image_bgr(image_bgr):
        """ Create new window with the image requested """
        image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
        plt.imshow(image_rgb)
        plt.show()

    @staticmethod
    def __display_image_lab(image_lab):
        """ Create new window with the image requested """
        image_rgb = cv2.cvtColor(image_lab, cv2.COLOR_Lab2RGB)
        plt.imshow(image_rgb)
        plt.show()