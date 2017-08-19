import os
from Core.Image import Image
import xml.etree.ElementTree as ET

class Dataset:

    def __init__(self, path, dataFiles=None):
        self.path = path
        self.files = os.listdir(self.path)

        self.dataFiles = dataFiles


    def size(self):
        files = os.listdir(self.path)
        return len(files)

    def name(self):
        return os.path.basename(self.path)

    def sampling(self):
        for file in self.files:
            print("-------------------------")
            try:
                print(self.path + file)
                image = Image(self.path + os.path.sep + file)
            except:

                continue
            print(image.name())

            node_meta = False
            for im in self.dataFiles.root_meta.findall('img'):
                if im.attrib['dataset'] == self.name() and im.attrib['name'] == str(image.name()):
                    node_meta = im
                    break

            node_img = ET.SubElement(self.dataFiles.root_node, 'image',
                                     attrib={'dataset': str(self.name()), 'name': str(image.name())})
            if not node_meta:
                node_meta = ET.SubElement(self.dataFiles.root_meta, 'img',
                                          attrib={'dataset': str(self.name()), 'name': str(image.name())})
            else:
                print("node_meta readed from xml")

            mostres = image.mostrejar(node_img, node_meta)

            if mostres is not None:
                ET.SubElement(node_meta, 'mid', attrib={'x': str(mostres.mid[0]), 'y': str(mostres.mid[1])})
                print(mostres)

    def studying(self, stats):
        for file in self.files:
            print("-------------------------")
            try:
                print(self.path + file)
                image = Image(self.path + os.path.sep + file)
            except:

                continue
            print(image.name())
            distances_rgb, distances_lab, distances_hsv = image.generate_distances2mean(stats)

