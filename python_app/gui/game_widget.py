"""
Makes a Drag-and-Drop Moveable Widget
Thanks to:
    https://zetcode.com/gui/pyqt5/dragdrop/
    https://stackoverflow.com/questions/12219727/dragging-moving-a-qpushbutton-in-pyqt
"""
from PySide6 import Qt
from PySide6.QtCore import Qt, SIGNAL, QRect
from PySide6.QtGui import QPixmap, QPainter
from PySide6.QtWidgets import (QLabel, QWidget, QPushButton,
                               QTextEdit, QVBoxLayout, QHBoxLayout,
                               QSpacerItem, QSizePolicy, QSplitter)
from __feature__ import snake_case, true_property  # pylint: disable=unused-import # used for making Qt pythonic


class GamePiece(QLabel):
    """Moveable Game Piece"""

    def __init__(self, parent, image_mgr):
        super().__init__(parent)
        image = image_mgr.get_image('piece')
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


class BoardImage(QWidget):
    def __init__(self, image_mgr):
        super().__init__()
        self.image = image_mgr.get_image('game_board')
        self.ratio = self.image.width() / self.image.height()

    def paint_event(self, event):
        """Repaint Board so it is Max size and Centered"""
        super().paint_event(event)
        painter = QPainter(self)
        painter.render_hint = QPainter.SmoothPixmapTransform
        # Pylint cannot find width() and height() functions
        # pylint: disable=no-member
        if self.rect.height() < self.rect.width():
            img_width = self.ratio * self.rect.height()
            rect = QRect((self.rect.width() - img_width)/2,
                         self.rect.y(),
                         img_width,
                         self.rect.height())
            painter.draw_pixmap(rect, self.image)
        else:
            img_width = self.rect.width()
            rect = QRect((self.rect.width() - img_width)/2,
                         self.rect.y(),
                         img_width,
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
        # pix = self._image_mgr.get_image('game_board')
        # print(self._parent, self._parent.width)
        # self.game_board.pixmap = pix.scaled(self._parent.height,
        #                                     self._parent.height,
        #                                     Qt.KeepAspectRatio)
        self.layout.add_widget(self.game_board)

        # self.game_piece = GamePiece(self, image_mgr)
        # self.layout.add_widget(self.game_piece)

        self.set_layout(self.layout)

    def resize(self):
        """Resize object to fit Image"""
        self.game_board.repaint()


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
        print(self.size.height())

        self.game_board = None
        self.hand_widget = None

        self.add_game_board()
        self.add_hand()
        self.add_action_widgets()

        self.set_stretch_factor(0, 30)
        self.set_stretch_factor(1, 1)
        self.set_stretch_factor(2, 1)
        # self.set_sizes([300, 1, 1])
        # print(self.sizes())

    def add_game_board(self):
        # widget = QWidget(self)
        # board_layout = QHBoxLayout()
        self.game_board = BoardWidget(self, self._image_mgr)
        # board_layout.add_widget(self.game_board)
        # board_layout.add_item(QSpacerItem(0,
        #                                   0.6 * self.size.height(),  # pylint: disable=no-member
        #                                   QSizePolicy.Preferred,
        #                                   QSizePolicy.Expanding))
        # widget.set_layout(board_layout)
        # self.add_widget(widget)
        self.add_widget(self.game_board)

    def add_hand(self):
        # widget = QWidget(self)
        # hand_layout = QHBoxLayout()
        self.hand_widget = HandWidget(self, self._image_mgr)
        # hand_layout.add_widget(self.hand_widget)
        # hand_layout.add_item(QSpacerItem(0,
        #                                  0.2 * self.size.height(),  # pylint: disable=no-member
        #                                  QSizePolicy.Maximum,
        #                                  QSizePolicy.Maximum))
        # widget.set_layout(hand_layout)
        # self.add_widget(widget)
        self.add_widget(self.hand_widget)

    def add_action_widgets(self):
        # widget = QWidget(self)
        # action_layout = QHBoxLayout()
        self.action_widget = ActionsWidget(self)
        # action_layout.add_widget(self.action_widget)
        # action_layout.add_item(QSpacerItem(0,
        #                                    0.2 * self.size.height(),  # pylint: disable=no-member
        #                                    QSizePolicy.Maximum,
        #                                    QSizePolicy.Maximum))
        # widget.set_layout(action_layout)
        # self.add_widget(widget)
        self.add_widget(self.action_widget)

    # def resize_event(self, event):
    #     super().resize_event(event)
    #     print(self.size.height())
    #     print(self.game_board.size.height())
    #     print(self.hand_widget.size.height())
    #     print(self.action_widget.size.height())
