"""GUI Elements for Clue Tracker"""
from PySide6 import QtWidgets  # pylint: disable=no-name-in-module # GitHub Actions cant import Qt modules
from __feature__ import snake_case, true_property  # pylint: disable=unused-import # used for making Qt pythonic


class ClueTrackerWidget(QtWidgets.QFrame):
    """Clue Tracker Layout"""

    def __init__(self, parent):
        super().__init__()
        self._parent = parent
        self.layout = QtWidgets.QVBoxLayout()
        message = QtWidgets.QLabel('Tracker Coming Soon')
        self.layout.add_widget(message)
        self.frame_shape = QtWidgets.QFrame.StyledPanel

        self.set_layout(self.layout)
