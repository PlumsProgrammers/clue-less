"""Central GUI for Clue-less game"""
from PySide6.QtCore import SIGNAL, QRect
from PySide6.QtGui import QIntValidator
from PySide6.QtWidgets import (QMainWindow, QWidget, QMenuBar,
                               QMessageBox, QVBoxLayout, QHBoxLayout,
                               QSpacerItem, QSizePolicy, QLabel,
                               QSplitter, QDialog, QPushButton,
                               QFrame, QLineEdit)

from gui.chat_widget import ChatWidget
from gui.game_widget import GameWidget
from gui.tracker_widget import ClueTrackerWidget

from resources.resource_manager import ImageManager

from __feature__ import snake_case, true_property  # pylint: disable=unused-import # used for making Qt pythonic


class MainWindow(QMainWindow):
    """Main Layout"""

    def __init__(self, app, game_instance):
        super().__init__()
        screen_size = app.primary_screen.size

        self.game_instance = game_instance

        self.image_mgr = ImageManager()
        self.image_mgr.load_images()

        self.window_title = 'Clue-less'
        self.geometry = QRect(0, 0,
                              screen_size.width(),
                              screen_size.width())

        self.central_widget = QSplitter(self)

        self.add_chat_gui()
        self.add_game_gui()
        self.add_clue_tracker_gui()

        self.set_central_widget(self.central_widget)

        self.add_menu_bar()

    def add_chat_gui(self):
        """Create chat GUI Layout"""
        widget = QWidget(self)
        chat_layout = QVBoxLayout()

        self.game_info = QLabel(self)
        chat_layout.add_widget(self.game_info)

        self.chat_gui = ChatWidget(self)
        chat_layout.add_widget(self.chat_gui)
        chat_layout.add_item(QSpacerItem(0.25 * self.size.width(),  # pylint: disable=no-member
                                         0,
                                         QSizePolicy.Expanding,
                                         QSizePolicy.Maximum))
        widget.set_layout(chat_layout)
        self.central_widget.add_widget(widget)

    def set_game_info_text(self):
        """Update Game Information text"""
        self.game_info.text = f'Game Name: {self.game_instance.game_name} | ' + \
                              f'Game ID: {self.game_instance.game_id}'

    def add_game_gui(self):
        """Create game GUI Layout"""
        widget = QWidget(self)
        game_layout = QVBoxLayout()
        self.game_gui = GameWidget(self, self.image_mgr)
        game_layout.add_widget(self.game_gui)
        game_layout.add_item(QSpacerItem(0.5 * self.size.width(),  # pylint: disable=no-member
                                         0,
                                         QSizePolicy.Expanding,
                                         QSizePolicy.Maximum))
        widget.set_layout(game_layout)
        self.central_widget.add_widget(widget)

    def add_clue_tracker_gui(self):
        """Adds clue tracker to main layout"""
        widget = QWidget(self)
        tracker_layout = QVBoxLayout()
        self.tracker_gui = ClueTrackerWidget(self)
        tracker_layout.add_widget(self.tracker_gui)
        tracker_layout.add_item(QSpacerItem(0.25 * self.size.width(),  # pylint: disable=no-member
                                            0,
                                            QSizePolicy.Expanding,
                                            QSizePolicy.Maximum))
        widget.set_layout(tracker_layout)
        self.central_widget.add_widget(widget)

    def add_menu_bar(self):
        """Adds Menu Bar to Layout"""
        menu_bar = QMenuBar(self)
        self.set_menu_bar(menu_bar)

        help_menu = menu_bar.add_menu('&Help')

        help_menu.add_action('&Rules')

        about_action = help_menu.add_action('&About')
        about_action.shortcut = 'Ctrl+a'
        self.connect(about_action,
                     SIGNAL('triggered()'),
                     self.show_about_message)

    def show_about_message(self):
        """Show About Message Popup"""
        response = self.game_instance.about()
        QMessageBox.information(self, 'About', response)

    def show(self):
        """Initialze Game GUI if Game Login Succeeds"""
        join_menu = JoinMenu(self)
        result = join_menu.exec_()
        if result == QDialog.Accepted:
            super().show()
            return True
        return False


class JoinMenu(QDialog):
    """Popup Menu for Starting/Joining Games

    Attributes:
        game_name_box (QLineEdit): Set Game Name - New Game
        create_password_box (QLineEdit): Set Game Password - New Game
        create_username_box (QLineEdit): Set Player Username - New Game
        game_code_box (QLineEdit): Set GameId Value - Join Game
        join_password_box (QLineEdit): Set Game Password - Join Game
        join_username_box (QLineEdit): Set Player Username - New Game
    """

    def __init__(self, parent):
        super().__init__(parent)
        menu_layout = QHBoxLayout()
        self._game_instance = parent.game_instance

        # Set Up Start Game Options
        new_game_layout = QVBoxLayout()
        new_game_layout.add_widget(QLabel('New Game'))
        line = QFrame()
        line.frame_shape = QFrame.HLine
        line.frame_shadow = QFrame.Sunken
        new_game_layout.add_widget(line)
        new_game_layout.add_widget(QLabel('Game Name'))
        self.game_name_box = QLineEdit(self)
        new_game_layout.add_widget(self.game_name_box)
        new_game_layout.add_widget(QLabel('Set Game Password (Optional)'))
        self.create_password_box = QLineEdit(self)
        self.create_password_box.echo_mode = QLineEdit.Password
        new_game_layout.add_widget(self.create_password_box)
        new_game_layout.add_widget(QLabel('Username'))
        self.create_username_box = QLineEdit(self)
        new_game_layout.add_widget(self.create_username_box)
        new_game_button = QPushButton('Start', self)
        self.connect(new_game_button,
                     SIGNAL('clicked()'),
                     self.start_new_game)
        new_game_layout.add_widget(new_game_button)
        menu_layout.add_layout(new_game_layout)

        # Add Vertical Seperator
        line = QFrame()
        line.frame_shape = QFrame.VLine
        line.frame_shadow = QFrame.Sunken
        menu_layout.add_widget(line)

        # Set Up Join Game Options
        join_game_layout = QVBoxLayout()
        join_game_layout.add_widget(QLabel('Join Game'))
        line = QFrame()
        line.frame_shape = QFrame.HLine
        line.frame_shadow = QFrame.Sunken
        join_game_layout.add_widget(line)
        join_game_layout.add_widget(QLabel('Game Code'))
        self.game_code_box = QLineEdit(self)
        self.game_code_box.set_validator(QIntValidator())
        join_game_layout.add_widget(self.game_code_box)
        join_game_layout.add_widget(QLabel('Game Password (Optional)'))
        self.join_password_box = QLineEdit(self)
        self.join_password_box.echo_mode = QLineEdit.Password
        join_game_layout.add_widget(self.join_password_box)
        join_game_layout.add_widget(QLabel('Username'))
        self.join_username_box = QLineEdit(self)
        join_game_layout.add_widget(self.join_username_box)
        join_game_button = QPushButton('Join', self)
        self.connect(join_game_button,
                     SIGNAL('clicked()'),
                     self.join_game)
        join_game_layout.add_widget(join_game_button)
        menu_layout.add_layout(join_game_layout)

        self.set_layout(menu_layout)

    def start_new_game(self):
        """Start New Game using User Provided Responses"""
        game_name = str(self.game_name_box.text).strip()
        password = self.create_password_box.text
        username = str(self.create_username_box.text).strip()
        result, message = self._game_instance.create_game(game_name=game_name,
                                                          password=password)
        if result:
            result, message = self._game_instance.join_game(game_id=self._game_instance.game_id,
                                                            username=username,
                                                            password=password)
            if result:
                QMessageBox.information(self, 'Success', message.title())
                super().accept()

        if not result:
            QMessageBox.warning(self, 'Oops', message.title())

    def join_game(self):
        """Join Existing Game using User Provided Responses"""
        game_id = int(self.game_code_box.text)
        password = self.join_password_box.text
        username = str(self.join_username_box.text).strip()

        result, message = self._game_instance.join_game(game_id=game_id,
                                                        username=username,
                                                        password=password)
        if result:
            QMessageBox.information(self, 'Success', message.title())
            super().accept()

        if not result:
            QMessageBox.warning(self, 'Oops', message.title())
