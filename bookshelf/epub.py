import os
import zipfile
from xml.etree import ElementTree as ET


class Epub:
    def __init__(self, path):
        """


        :param path:
        :type path: str
        """
        self.path = os.path.abspath(path)
        self.filename = os.path.basename(path)
        self.zipfile = zipfile.ZipFile(path)

        #Initialize epub metadata
        self.container = self._getContainer()
        self.rootfile_path = self._getRootfilePath()
        self.rootfile = self._getRootfile()

    def read(self, file_path):
        """

        :param file_path:
        :type file_path: str
        :return:
        :rtype: str
        """
        return self.zipfile.read(file_path)

    def readFirstInPaths(self, file_paths):
        """

        :param file_paths:
        :type file_paths: list
        :return:
        :rtype: str
        """
        for path in file_paths:
            try:
                return self.read(path)
            except KeyError:
                continue
        raise KeyError

    def _getContainer(self):
        """

        :return:
        :rtype: EpubXml
        """
        return EpubXml(self.read('META-INF/container.xml'))

    def _getRootfilePath(self):
        """
        :return:
        :rtype: str
        """
        return self.container.find('n:rootfiles/n:rootfile').get('full-path')

    def _getRootfile(self):
        """

        :return:
        :rtype: EpubXml
        """
        return EpubXml(self.read(self.rootfile_path))


class EpubXml:
    def __init__(self, xml):
        """

        :param xml:
        :type xml: str
        """
        """:type : xml.etree.ElementTree.Element"""
        self.element = ET.fromstring(xml)
        self.ns = {
            'n': 'urn:oasis:names:tc:opendocument:xmlns:container',
            'pkg': 'http://www.idpf.org/2007/opf',
            'dc': 'http://purl.org/dc/elements/1.1/',
            'opf': 'http://www.idpf.org/2007/opf'
        }

    def find(self, xpath):
        """

        :param xpath:
        :type xpath: str
        :return:
        :rtype: xml.etree.ElementTree.Element
        """
        return self.element.find(xpath, self.ns)

    def findall(self, xpath):
        """

        :param xpath:
        :type xpath: str
        :return:
        :rtype: list of xml.etree.ElementTree.Element
        """
        return self.element.findall(xpath, self.ns)

    def findInPaths(self, xpaths):
        """

        :param xpaths:
        :type xpaths: list of str
        :return:
        :rtype: xml.etree.ElementTree.Element
        """
        for xpath in xpaths:
            found = self.find(xpath)
            if found is not None:
                return found
        return None

    def findallInPaths(self, xpaths):
        """

        :param xpaths:
        :type xpaths: list of str
        :return:
        :rtype: list of xml.etree.ElementTree.Element
        """
        for xpath in xpaths:
            found = self.findall(xpath)
            if found is not None:
                return found
        return None
