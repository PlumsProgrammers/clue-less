"""GUI Elements for Clue Tracker"""
from PySide6.QtWidgets import (QLabel, QFrame, QVBoxLayout)
from __feature__ import snake_case, true_property  # pylint: disable=unused-import # used for making Qt pythonic


class ClueTrackerWidget(QFrame):
    """Clue Tracker Layout"""

    def __init__(self, parent):
        super().__init__()
        self._parent = parent
        self.layout = QVBoxLayout()
        message = QLabel('Tracker Coming Soon')
        self.layout.add_widget(message)
        self.frame_shape = QFrame.StyledPanel

        self.set_layout(self.layout)
