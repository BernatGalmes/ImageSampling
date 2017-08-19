import os
from Core.Config import Config
import xml.etree.ElementTree as ET


class DataFiles:

    def __init__(self, file_metadata=None, file_data=None):

        if file_metadata is None:
            self.file_metadata = Config.DEFAULT_FILENAME_METADATA
        else:
            self.file_metadata = file_metadata

        if file_data is None:
            self.file_data = Config.DEFAULT_FILENAME_DATA
        else:
            self.file_data = file_data

        self.__init_result_files()

    def __init_result_files(self):
        self.root_node = ET.Element('imatges')
        if os.path.exists(self.file_metadata):
            metadata = ET.ElementTree()
            metadata.parse(self.file_metadata)
            self.root_meta = metadata.getroot()

        else:
            self.root_meta = ET.Element('metadata')

        print(ET.tostring(self.root_meta, encoding="us-ascii", method="xml"))

    def save(self):
        tree = ET.ElementTree(self.root_node)
        tree.write(self.file_data)
        metadata = ET.ElementTree(self.root_meta)
        metadata.write(self.file_metadata)
        tree.find('pix')
        print(ET.tostring(self.root_node, encoding="us-ascii", method="xml"))


    @staticmethod
    def registreMeta(node_meta, mid, amp):
        ET.SubElement(node_meta, 'mid', attrib={'x': str(mid[0]), 'y': str(mid[1])})
        ET.SubElement(node_meta, 'amp', attrib={'val': str(amp)})