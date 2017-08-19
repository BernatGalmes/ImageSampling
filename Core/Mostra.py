import numpy as np
import cv2
import xml.etree.ElementTree as ET
from Core.Config import Config
from Core.utils import check_dir, get_rand_points

class Mostra:
    n_pix = 300


    def __init__(self, name_image, image_bgr, image_rgb, mid):
        self.folder_results = Config.DEFAULT_FOLDER_RESULTS
        check_dir(self.folder_results)

        self.amp = 200
        self.correct = False
        self.discard = False

        self.name_image = name_image
        self.image_rgb = image_rgb
        self.image_bgr = image_bgr
        self.mid = mid

        self.image_lab = cv2.cvtColor(self.image_rgb, cv2.COLOR_RGB2LAB).astype("uint8")  # np.copy(sample.original_bgr)
        self.image_hsv = cv2.cvtColor(self.image_rgb, cv2.COLOR_RGB2HSV).astype("uint8")  # np.copy(sample.original_bgr)



    def onClick(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            print("click event on " + str(x) + " " + str(y))
            self.mid=[x,y]
            cv2.destroyAllWindows()


    def registreDades(self, node_img):
        node_pixels = ET.SubElement(node_img, 'pixels')
        for p in self.pixs:
            px_lab = self.image_lab[p[1], p[0]]
            px_rgb = self.image_rgb[p[1], p[0]]
            px_hsv = self.image_hsv[p[1], p[0]]
            node_pix = ET.SubElement(node_pixels, 'pix', attrib={'x': str(p[0]), 'y': str(p[1])})
            node_lab = ET.SubElement(node_pix,'lab', attrib={'L': str(px_lab[0]), 'a': str(px_lab[1]), 'b': str(px_lab[2])})
            node_rgb = ET.SubElement(node_pix, 'rgb', attrib={'r': str(px_rgb[0]), 'g': str(px_rgb[1]), 'b': str(px_rgb[2])})
            node_hsv = ET.SubElement(node_pix, 'hsv',
                                    attrib={'h': str(px_hsv[0]), 's': str(px_hsv[1]), 'v': str(px_hsv[2])})

    def imageProces(self):
        self.pixs = get_rand_points(self.mid, self.n_pix, self.amp)  # ger n_pix mostres

        image_pixels = np.copy(self.image_bgr)
        # color mitj de les mostres
        for i, p in enumerate(self.pixs):
            cv2.circle(image_pixels, (p[0], p[1]), 10, (0, 0, 0), -1)

        if not self.correct:

            cv2.namedWindow('winImg', flags=cv2.WINDOW_NORMAL)
            cv2.setMouseCallback("winImg", self.onClick)
            cv2.resizeWindow('winImg', 600, 600)
            cv2.imshow('winImg', image_pixels)
            key = cv2.waitKey(-1)
            self.applyKey(key, image_pixels)
            cv2.destroyAllWindows()
        else:
            self.saveFile(image_pixels)

    def saveFile(self, image):
        cv2.imwrite(self.folder_results + "/" + self.name_image, image)

    def applyKey(self,key, image_pixels):
        key = key % 256
        if key == ord('-'):
            self.amp -= 5

        elif key == ord('+'):
            self.amp += 5

        elif key == ord('w'):
            self.mid[1] += 5

        elif key == ord('s'):
            self.mid[1] -= 5

        elif key == ord('a'):
            self.mid[0] -= 5

        elif key == ord('d'):
            self.mid[0] += 5

        elif key == ord('\n'):
            self.correct = True
            self.saveFile(image_pixels)

        elif key == ord('x'):
            self.discard =True

        else:
            print("another key")

    def setData(self, mid, amp):
        self.mid = mid
        self.amp = amp