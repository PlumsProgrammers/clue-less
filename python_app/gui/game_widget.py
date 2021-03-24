"""
Makes a Drag-and-Drop Moveable Widget
Thanks to:
    https://zetcode.com/gui/pyqt5/dragdrop/
    https://stackoverflow.com/questions/12219727/dragging-moving-a-qpushbutton-in-pyqt
"""
from PySide6.QtCore import Qt, SIGNAL
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (QLabel, QWidget, QPushButton,
                               QTextEdit, QVBoxLayout, QHBoxLayout,
                               QSpacerItem, QSizePolicy)
from __feature__ import snake_case, true_property  # pylint: disable=unused-import # used for making Qt pythonic


class GamePiece(QLabel):
    """Moveable Game Piece"""

    def __init__(self):
        super().__init__()
        image = QPixmap('piece.png')
        self.pixmap = image
        self._mouse_press_pos = None
        self._mouse_move_pos = None

    def resize(self):
        """Resize object to fit Image"""
        super().resize(self.pixmap.width(),
                       self.pixmap.height())

    def mouse_press_event(self, event):
        """Sets Click or Move based on mouse button"""
        self.resize()
        if event.button() == Qt.LeftButton:
            self._mouse_press_pos = event.global_pos()
            self._mouse_move_pos = event.global_pos()

    def mouse_move_event(self, event):
        """Updates button position when mouse moves"""
        if event.buttons() == Qt.LeftButton:
            # adjust offset from clicked point to origin of widget
            curr_pos = self.map_to_global(self.pos)
            global_pos = event.global_pos()
            diff = global_pos - self._mouse_move_pos
            new_pos = self.map_from_global(curr_pos + diff)
            self.move(new_pos)
            self._mouse_move_pos = global_pos


class Button(QPushButton):
    """Moveable Button"""

    def __init__(self, title, parent):
        super().__init__(title, parent)
        self.connect(self,
                     SIGNAL('clicked()'),
                     lambda: self.parent().update_text(self))
        self._mouse_press_pos = None
        self._mouse_move_pos = None

    def mouse_press_event(self, event):
        """Sets Click or Move based on mouse button"""
        if event.button() == Qt.LeftButton:
            super().mouse_press_event(event)
        else:
            if event.button() == Qt.RightButton:
                self._mouse_press_pos = event.global_pos()
                self._mouse_move_pos = event.global_pos()

    def mouse_move_event(self, event):
        """Updates button position when mouse moves"""
        if event.buttons() == Qt.RightButton:
            # adjust offset from clicked point to origin of widget
            curr_pos = self.map_to_global(self.pos)
            global_pos = event.global_pos()
            diff = global_pos - self._mouse_move_pos
            new_pos = self.map_from_global(curr_pos + diff)
            self.move(new_pos)

            self._mouse_move_pos = global_pos


class GameWidget(QWidget):
    """Central Game Layout"""

    def __init__(self, parent):
        super().__init__()
        self._parent = parent
        self.layout = QVBoxLayout()
        self.accept_drops = True

        self.text_box = QTextEdit('Press a Button', self)
        self.layout.add_widget(self.text_box)

        button3_layout = QHBoxLayout()
        button3 = QPushButton('StaticButton', self)
        button3.connect(button3,
                        SIGNAL('clicked()'),
                        lambda: self.update_text(button3))
        spacer = QSpacerItem(10, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
        button3_layout.add_widget(button3)
        button3_layout.add_item(spacer)
        self.layout.add_layout(button3_layout)

        button_layout = QHBoxLayout()
        button = Button('Button', self)
        spacer = QSpacerItem(10, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
        button_layout.add_widget(button)
        button_layout.add_item(spacer)
        self.layout.add_layout(button_layout)

        self.game_piece = GamePiece()
        self.layout.add_widget(self.game_piece)

        self.set_layout(self.layout)

    def update_text(self, button):
        """Set text in central text box"""
        self.text_box.set_text(f'Clicked {button.text}')
