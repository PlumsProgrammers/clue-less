"""
Makes a Drag-and-Drop Moveable Widget
Thanks to:
    https://zetcode.com/gui/pyqt5/dragdrop/
    https://stackoverflow.com/questions/12219727/dragging-moving-a-qpushbutton-in-pyqt
"""
import re

from PySide6 import QtCore  # pylint: disable=no-name-in-module # GitHub Actions cant import Qt modules
from PySide6 import QtGui  # pylint: disable=no-name-in-module # GitHub Actions cant import Qt modules
from PySide6 import QtWidgets  # pylint: disable=no-name-in-module # GitHub Actions cant import Qt modules

from interface.game_objects import Rooms, Suspects, Weapons

# pylint: disable=wrong-import-order # Import must go last
from __feature__ import snake_case, true_property  # pylint: disable=unused-import # used for making Qt pythonic


class GamePiece(QtWidgets.QLabel):
    """Moveable Game Piece

    Attributes:
        parent (BoardWidget): Board Widget containing this piece
        image (QPixMap): Image used for Game Board
        ratio (float): image Width/Height
    """

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
        if event.button() == QtCore.Qt.LeftButton:
            self._mouse_press_pos = event.global_pos()
            self._mouse_move_pos = event.global_pos()

    def mouse_move_event(self, event):
        """Updates button position when mouse moves"""
        if event.buttons() == QtCore.Qt.LeftButton:
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
        if width < 1 or height < 1:
            self.hide()
        else:
            new_size = QtCore.QSize()
            new_size.set_height(height)
            new_size.set_width(width)
            self.size = new_size
            painter = QtGui.QPainter(self)
            painter.render_hint = QtGui.QPainter.SmoothPixmapTransform
            rect = QtCore.QRect(self.rect.x(),
                                self.rect.y(),
                                width,
                                height)
            painter.draw_pixmap(rect, self.image)
            self.raise_()


class BoardImage(QtWidgets.QWidget):
    """Widget containing scalable game board

    Attributes:
        image (QPixMap): Image used for Game Board
        ratio (float): image Width/Height
        img_width (int): Current board image width
    """

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
        super().paint_event(event)
        painter = QtGui.QPainter(self)
        painter.render_hint = QtGui.QPainter.SmoothPixmapTransform
        # Pylint cannot find width() and height() functions
        # pylint: disable=no-member
        if self.rect.height() < self.rect.width():
            self.img_width = self.ratio * self.rect.height()
            rect = QtCore.QRect((self.rect.width() - self.img_width)/2,
                                self.rect.y(),
                                self.img_width,
                                self.rect.height())
            painter.draw_pixmap(rect, self.image)
        else:
            self.img_width = self.rect.width()
            rect = QtCore.QRect((self.rect.width() - self.img_width)/2,
                                self.rect.y(),
                                self.img_width,
                                self.rect.width() / self.ratio)
            painter.draw_pixmap(rect, self.image)


class BoardWidget(QtWidgets.QFrame):
    """Widget Showing Game Board and Game Pieces

    Attributes:
        game_board (BoardImage): Resizable Game Board widget
        game_piece (GamePiece): Movable Game Piece widget
    """

    def __init__(self, parent, image_mgr):
        super().__init__()
        self._parent = parent
        self.frame_shape = QtWidgets.QFrame.StyledPanel
        self._parent.splitterMoved.connect(self.resize)
        self._image_mgr = image_mgr

        layout = QtWidgets.QVBoxLayout()
        self.accept_drops = True

        self.game_board = BoardImage(image_mgr)
        layout.add_widget(self.game_board)

        self.game_piece = GamePiece(self, image_mgr)
        # Pylint cannot find width() and height() functions
        # pylint: disable=no-member
        self.game_piece.move(self.rect.x(), self.rect.y())

        self.set_layout(layout)

    def resize(self):
        """Resize object to fit Image"""
        self.game_board.repaint()
        if self.game_piece.is_hidden():
            self.game_piece.show()
        self.game_piece.repaint()


class HandWidget(QtWidgets.QScrollArea):
    """Widget Showing Images for cards in Player's Hand

    Attributes:
        card_layout (QtWidgets.QHBoxLayout): Horizontal Layout where Cards are shown
    """

    def __init__(self, parent, image_mgr):
        super().__init__()
        self._parent = parent
        self.img_height = int(self._parent.rect.height()/5)
        self._image_mgr = image_mgr
        self.content = QtWidgets.QWidget(self)
        self.card_layout = QtWidgets.QHBoxLayout()

        self.default_card = QtWidgets.QLabel(self)
        img = image_mgr.get_image('Card')
        self.default_card.pixmap = img.scaled(self.img_height,
                                              self.img_height,
                                              QtGui.Qt.KeepAspectRatioByExpanding,
                                              QtGui.Qt.FastTransformation)
        self.card_layout.add_widget(self.default_card)
        self.content.set_layout(self.card_layout)

        self.set_widget(self.content)

        scroll_bar = QtWidgets.QScrollBar(self)
        self.set_horizontal_scroll_bar(scroll_bar)

    def add_cards(self, hand):
        """Add given Cards to Hand"""
        if hand:
            self.content.parent = None
            self.content = QtWidgets.QWidget(self)
            self.card_layout = QtWidgets.QHBoxLayout()

            for card in hand:
                name = re.sub(r'[^a-zA-Z0-9 ]', '', card['name'])
                img = self._image_mgr.get_image(name)
                new_card = QtWidgets.QLabel(self)
                new_card.pixmap = img.scaled(self.img_height,
                                             self.img_height,
                                             QtGui.Qt.KeepAspectRatioByExpanding,
                                             QtGui.Qt.FastTransformation)
                self.card_layout.add_widget(new_card)

            self.content.set_layout(self.card_layout)
            self.set_widget(self.content)
            self.update()


class ActionsWidget(QtWidgets.QWidget):
    """Widget showing Action History and Suggestion/Accusation button

    Attributes:
        action_log (QtWidgets.QTextEdit): Text box for showing action history
    """

    def __init__(self, parent):
        super().__init__()
        self._parent = parent

        layout = QtWidgets.QHBoxLayout()
        self.action_log = LogBox(self)
        layout.add_widget(self.action_log)

        button_layout = QtWidgets.QVBoxLayout()
        suggestion_button = QtWidgets.QPushButton('Make Suggestion')
        accusation_button = QtWidgets.QPushButton('Make Accusation')
        self.connect(accusation_button,
                     QtCore.SIGNAL('clicked()'),
                     self.make_accusation)
        button_layout.add_widget(suggestion_button)
        button_layout.add_widget(accusation_button)

        layout.add_layout(button_layout)
        self.set_layout(layout)

    def make_accusation(self):
        """Create Form to Select Accusation, then submit"""
        accusation = AccusationWidget(self)
        status = accusation.exec_()
        if status == QtWidgets.QDialog.Accepted:
            result, message = self._parent.game_instance.make_accusation(accusation.person,
                                                                         accusation.place,
                                                                         accusation.thing)
            if result:
                QtWidgets.QMessageBox.information(self, 'Result', message)
            else:
                QtWidgets.QMessageBox.warning(self, 'Oops', message)

    def update_log(self, event):
        """Add message to event log"""
        event_msg = event.replace('Message:', '').strip()
        self.action_log.update_text(f'\n> {event_msg}')


class LogBox(QtWidgets.QScrollArea):
    """Creates a scrollable text box for logging actions
    Source: https://www.geeksforgeeks.org/pyqt5-scrollable-label/
    """

    def __init__(self, parent):
        super().__init__(parent)
        self.style_sheet = 'background-color: white'
        self.widget_resizable = True
        content = QtWidgets.QWidget(self)
        self.set_widget(content)
        layout = QtWidgets.QVBoxLayout(content)
        self.log = QtWidgets.QLabel(content)
        self.log.alignment = QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop
        self.log.word_wrap = True
        layout.add_widget(self.log)

    def update_text(self, text):
        """Appends action to log box"""
        self.log.text += text


class GameWidget(QtWidgets.QSplitter):
    """Central Game Layout

    Attributes:
        game_instance (clueless_app.Clueless): Main Game instance
        game_board (BoardWidget): Resizable Game Board widget
        hand_widget (HandWidget): Widget containing player cards
        action_widtet (ActionsWidget): Widget containing action
            history and accusation/suggestion buttons
    """

    def __init__(self, parent, game_instance, image_mgr):
        super().__init__(QtCore.Qt.Vertical)
        self.game_instance = game_instance
        self._image_mgr = image_mgr
        self._parent = parent

        self.game_board = None
        self.hand_widget = None

        self.game_board = BoardWidget(self, self._image_mgr)
        self.add_widget(self.game_board)
        self.set_stretch_factor(0, 30)

        widget = QtWidgets.QFrame(self)
        lower_layout = QtWidgets.QVBoxLayout()
        self.hand_widget = HandWidget(self, self._image_mgr)
        lower_layout.add_widget(self.hand_widget)

        self.action_widget = ActionsWidget(self)
        lower_layout.add_widget(self.action_widget)
        widget.set_layout(lower_layout)
        self.add_widget(widget)

    def update_log(self, event):
        """Pass events to Action Log"""
        self.action_widget.update_log(event)

    def update_cards(self, hand):
        """Pass hand to Hand Widget"""
        self.hand_widget.add_cards(hand)


class AccusationWidget(QtWidgets.QDialog):
    """Create a form for making Accusations

    Attributes:
        person (str): Suspect Selected for Accusation
        place (str): Room Selected for Accusation
        thing (str): Weapon Selected for Accusation
        suspect_selector (QtWidgets.QComboBox): Dropdown for selecting suspects
        room_selector (QtWidgets.QComboBox): Dropdown for selecting rooms
        weapon_selector (QtWidgets.QComboBox): Dropdown for selecting weapons
    """

    def __init__(self, parent):
        super().__init__(parent)
        self._parent = parent
        self.person = None
        self.place = None
        self.thing = None

        form = QtWidgets.QFormLayout()
        self.suspect_selector = QtWidgets.QComboBox(self)
        self.suspect_selector.add_items(['None'] + Suspects.get_suspect_list())
        form.add_row(QtWidgets.QLabel('Suspect'), self.suspect_selector)
        self.room_selector = QtWidgets.QComboBox(self)
        self.room_selector.add_items(['None'] + Rooms.get_room_list())
        form.add_row(QtWidgets.QLabel('Room'), self.room_selector)
        self.weapon_selector = QtWidgets.QComboBox(self)
        self.weapon_selector.add_items(['None'] + Weapons.get_weapon_list())
        form.add_row(QtWidgets.QLabel('Weapon'), self.weapon_selector)

        accept_button = QtWidgets.QPushButton('Accuse', self)
        self.connect(accept_button,
                     QtCore.SIGNAL('clicked()'),
                     self.accept)

        cancel_button = QtWidgets.QPushButton('Cancel', self)
        self.connect(cancel_button,
                     QtCore.SIGNAL('clicked()'),
                     self.reject)
        form.add_row(accept_button, cancel_button)
        self.set_layout(form)

    def accept(self):
        """Override of QDialog accept method, verifies user selections"""
        self.person = self.suspect_selector.current_text
        self.place = self.room_selector.current_text
        self.thing = self.weapon_selector.current_text

        if self.person == 'None':
            QtWidgets.QMessageBox.warning(self,
                                          'Oops',
                                          'Please Select a Suspect')
        elif self.place == 'None':
            QtWidgets.QMessageBox.warning(self,
                                          'Oops',
                                          'Please Select a Room')
        elif self.thing == 'None':
            QtWidgets.QMessageBox.warning(self,
                                          'Oops',
                                          'Please Select a Weapon')
        else:
            super().accept()
