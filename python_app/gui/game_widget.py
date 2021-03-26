"""
Makes a Drag-and-Drop Moveable Widget
Thanks to:
    https://zetcode.com/gui/pyqt5/dragdrop/
    https://stackoverflow.com/questions/12219727/dragging-moving-a-qpushbutton-in-pyqt
"""
from PySide6 import Qt
from PySide6.QtCore import Qt, SIGNAL, QRect, QSize
from PySide6.QtGui import QPixmap, QPainter
from PySide6.QtWidgets import (QLabel, QWidget, QPushButton,
                               QTextEdit, QVBoxLayout, QHBoxLayout,
                               QSpacerItem, QSizePolicy, QSplitter)
from __feature__ import snake_case, true_property  # pylint: disable=unused-import # used for making Qt pythonic


class GamePiece(QLabel):
    """Moveable Game Piece"""

    def __init__(self, parent, image_mgr):
        super().__init__(parent)
        self.parent = parent
        self.image = image_mgr.get_image('piece')
        self.ratio = self.image.size().width() / self.image.size().height()
        self.resize(self.image.size())
        self._mouse_press_pos = None
        self._mouse_move_pos = None

    def mouse_press_event(self, event):
        """Sets Click or Move based on mouse button"""
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

    def paint_event(self, event):
        """Repaint Board so it is Max size and Centered"""
        super().paint_event(event)
        # Pylint cannot find width() and height() functions
        # pylint: disable=no-member
        width = int(self.parent.game_board.img_width / 18)
        height = int(self.rect.width() / self.ratio)
        new_size = QSize()
        new_size.set_height(height)
        new_size.set_width(width)
        self.size = new_size
        painter = QPainter(self)
        painter.render_hint = QPainter.SmoothPixmapTransform
        rect = QRect(self.rect.x(),
                     self.rect.y(),
                     width,
                     height)
        painter.draw_pixmap(rect, self.image)
        self.raise_()


class BoardImage(QWidget):
    def __init__(self, image_mgr):
        super().__init__()
        self.image = image_mgr.get_image('game_board')
        self.ratio = self.image.width() / self.image.height()
        self.img_width = self.image.width()

    def paint_event(self, event):
        """Repaint Board so it is Max size and Centered

        Source: https://stackoverflow.com/questions/44505229/
                pyqt-automatically-resizing-widget-picture
        """
        painter = QPainter(self)
        painter.render_hint = QPainter.SmoothPixmapTransform
        # Pylint cannot find width() and height() functions
        # pylint: disable=no-member
        if self.rect.height() < self.rect.width():
            self.img_width = self.ratio * self.rect.height()
            rect = QRect((self.rect.width() - self.img_width)/2,
                         self.rect.y(),
                         self.img_width,
                         self.rect.height())
            painter.draw_pixmap(rect, self.image)
        else:
            self.img_width = self.rect.width()
            rect = QRect((self.rect.width() - self.img_width)/2,
                         self.rect.y(),
                         self.img_width,
                         self.rect.width() / self.ratio)
            painter.draw_pixmap(rect, self.image)


class BoardWidget(QWidget):

    def __init__(self, parent, image_mgr):
        super().__init__()
        self._parent = parent
        self._parent.splitterMoved.connect(self.resize)
        self._image_mgr = image_mgr

        self.layout = QVBoxLayout()
        self.accept_drops = True

        self.game_board = BoardImage(image_mgr)
        self.layout.add_widget(self.game_board)

        self.game_piece = GamePiece(self, image_mgr)
        # Pylint cannot find width() and height() functions
        # pylint: disable=no-member
        self.game_piece.move(self.rect.x(), self.rect.y())

        self.set_layout(self.layout)

    def resize(self):
        """Resize object to fit Image"""
        self.game_board.repaint()
        self.game_piece.repaint()


class HandWidget(QWidget):

    def __init__(self, parent, image_mgr):
        super().__init__()
        self._parent = parent
        self._image_mgr = image_mgr
        self.card_layout = QHBoxLayout()

        test_card = QLabel(self)
        test_card.pixmap = image_mgr.get_image('card')
        self.card_layout.add_widget(test_card)
        self.set_layout(self.card_layout)


class ActionsWidget(QWidget):

    def __init__(self, parent):
        super().__init__()
        self._parent = parent

        layout = QHBoxLayout()
        self.action_log = QTextEdit(self)
        layout.add_widget(self.action_log)

        button_layout = QVBoxLayout()
        self.suggestion_button = QPushButton('Make Suggestion')
        self.accusation_button = QPushButton('Make Accusation')
        button_layout.add_widget(self.suggestion_button)
        button_layout.add_widget(self.accusation_button)

        layout.add_layout(button_layout)
        self.set_layout(layout)


class GameWidget(QSplitter):
    """Central Game Layout"""

    def __init__(self, parent, image_mgr):
        super().__init__(Qt.Vertical)
        self._image_mgr = image_mgr
        self._parent = parent

        self.game_board = None
        self.hand_widget = None

        self.game_board = BoardWidget(self, self._image_mgr)
        self.add_widget(self.game_board)
        self.set_stretch_factor(0, 30)

        self.hand_widget = HandWidget(self, self._image_mgr)
        self.add_widget(self.hand_widget)
        self.set_stretch_factor(1, 1)

        self.action_widget = ActionsWidget(self)
        self.add_widget(self.action_widget)
        self.set_stretch_factor(2, 1)q
