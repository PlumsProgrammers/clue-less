"""Loads All Image Resources"""
import os
import glob
from PySide6 import QtGui  # pylint: disable=no-name-in-module # GitHub Actions cant import Qt modules


class ImageManager:
    """Loads Image Files

    Attributes:
        images (Dict{str: QtGui.QPixmap}): Dictionary of QPixmap objects
    """

    def __init__(self):
        self.images = {}

    def load_images(self):
        """Recusively loads all Images in resources/"""
        resource_folder = os.path.dirname(os.path.abspath(__file__))
        for item in glob.glob(os.path.join(resource_folder, '*'),
                              recursive=True):
            filename, ext = os.path.splitext(os.path.basename(item))
            if ext in ['.png', '.jpg']:
                self.images[filename] = QtGui.QPixmap(item)

    def get_image(self, name):
        """Get Image Object for selected filename"""
        return self.images.get(name, QtGui.QPixmap())
