"""GUI Elements for Clue Tracker"""
from PySide6 import QtWidgets  # pylint: disable=no-name-in-module # GitHub Actions cant import Qt modules
from __feature__ import snake_case, true_property  # pylint: disable=unused-import # used for making Qt pythonic

from interface.game_objects import Rooms, Suspects, Weapons


class QHLine(QtWidgets.QFrame):
    """Creates a Horizontal Line for separating widgets"""

    def __init__(self):
        super().__init__()
        self.frame_shape = QtWidgets.QFrame.HLine
        self.frame_shadow = QtWidgets.QFrame.Sunken


class ClueTrackerWidget(QtWidgets.QFrame):
    """Clue Tracker Layout"""

    def __init__(self, parent):
        super().__init__()
        self._parent = parent
        self.layout = QtWidgets.QVBoxLayout()
        self.frame_shape = QtWidgets.QFrame.StyledPanel

        self.layout.add_widget(QtWidgets.QLabel('Suspects'))
        suspect_form = QtWidgets.QFormLayout()
        for suspect in Suspects.get_suspect_list():
            checkbox = QtWidgets.QCheckBox()
            checkbox.tristate = True
            suspect_form.add_row(QtWidgets.QLabel(suspect),
                                 checkbox)
        self.layout.add_layout(suspect_form)
        self.layout.add_widget(QHLine())

        self.layout.add_widget(QtWidgets.QLabel('Rooms'))
        room_form = QtWidgets.QFormLayout()
        for room in Rooms.get_room_list():
            checkbox = QtWidgets.QCheckBox()
            checkbox.tristate = True
            room_form.add_row(QtWidgets.QLabel(room),
                              checkbox)
        self.layout.add_layout(room_form)
        self.layout.add_widget(QHLine())

        self.layout.add_widget(QtWidgets.QLabel('Weapons'))
        weapon_form = QtWidgets.QFormLayout()
        for weapon in Weapons.get_weapon_list():
            checkbox = QtWidgets.QCheckBox()
            checkbox.tristate = True
            weapon_form.add_row(QtWidgets.QLabel(weapon),
                                checkbox)
        self.layout.add_layout(weapon_form)
        self.layout.add_widget(QHLine())

        self.set_layout(self.layout)
