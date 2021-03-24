"""GUI Elements for Clue Tracker"""
from PySide6.QtWidgets import (QLabel, QWidget, QVBoxLayout)
from __feature__ import snake_case, true_property  # pylint: disable=unused-import # used for making Qt pythonic


class ClueTrackerWidget(QWidget):
    """Clue Tracker Layout"""

    def __init__(self, parent):
        super().__init__()
        self._parent = parent
        self.layout = QVBoxLayout()
        message = QLabel('Tracker Coming Soon')
        self.layout.add_widget(message)

        self.set_layout(self.layout)
