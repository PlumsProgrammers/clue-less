"""Central GUI for Clue-less game"""
from PySide6 import QtCore  # pylint: disable=no-name-in-module # GitHub Actions cant import Qt modules
from PySide6 import QtGui  # pylint: disable=no-name-in-module # GitHub Actions cant import Qt modules
from PySide6 import QtWidgets  # pylint: disable=no-name-in-module # GitHub Actions cant import Qt modules

from gui.chat_widget import ChatWidget
from gui.game_widget import GameWidget
from gui.tracker_widget import ClueTrackerWidget

from interface.game_objects import Suspects
from interface.web_socket import get_socket

from resources.resource_manager import ImageManager

# pylint: disable=wrong-import-order # Import must go last
from __feature__ import snake_case, true_property  # pylint: disable=unused-import # used for making Qt pythonic


class MainWindow(QtWidgets.QMainWindow):  # pylint: disable=too-many-instance-attributes # All attrs required
    """Main Layout

    Attributes:
        game_instance (clueless_app.Clueless): Main Game Instance
        image_mgr (ImageManager): Manages Loading of Images for GUI
        central_widget (QtWidgets.QSplitter): Resizable Widget containing three main
            GUI sections
        game_info (QtWidgets.QLabel): Widget displaying current game status
        chat_gui (ChatWidget): Widget displaying User-User chat
        game_gui (GameWidget): Widget displaying Game information and interface
        tracker_gui (ClueTrackerWidget): Widget for users to track clue information
    """

    def __init__(self, game_instance):
        super().__init__()

        self.socket = get_socket()
        self.socket.setup(gui=self,
                          game=game_instance,
                          config=game_instance.config)
        self.socket.start()

        self.game_instance = game_instance

        self.image_mgr = ImageManager()
        self.image_mgr.load_images()

        self.central_widget = QtWidgets.QSplitter(self)
        self.game_info = None
        self.chat_gui = None
        self.game_gui = None
        self.tracker_gui = None

        self.add_chat_gui()
        self.add_game_gui()

        self.central_widget.splitterMoved.connect(  # pylint: disable=no-member # cant find connect
            self.game_gui.game_board.resize)
        self.add_clue_tracker_gui()

        self.set_central_widget(self.central_widget)

        self.add_menu_bar()
        self.update_game_info_text()

    def add_chat_gui(self):
        """Create chat GUI Layout"""
        widget = QtWidgets.QWidget(self)
        chat_layout = QtWidgets.QVBoxLayout()

        self.game_info = QtWidgets.QLabel(self)
        chat_layout.add_widget(self.game_info)

        self.chat_gui = ChatWidget(self)
        chat_layout.add_widget(self.chat_gui)
        chat_layout.add_item(QtWidgets.QSpacerItem(0.25 * self.size.width(),  # pylint: disable=no-member
                                                   0,
                                                   QtWidgets.QSizePolicy.Expanding,
                                                   QtWidgets.QSizePolicy.Maximum))
        widget.set_layout(chat_layout)
        self.central_widget.add_widget(widget)

    def update_game_info_text(self):
        """Update Game Information text"""
        self.game_info.text = f'Game ID: {self.game_instance.game_id} | ' + \
            f'Status: {self.game_instance.status}'

    def add_game_gui(self):
        """Create game GUI Layout"""
        widget = QtWidgets.QWidget(self)
        game_layout = QtWidgets.QVBoxLayout()
        self.game_gui = GameWidget(self, self.game_instance, self.image_mgr)
        game_layout.add_widget(self.game_gui)
        game_layout.add_item(QtWidgets.QSpacerItem(0.5 * self.size.width(),  # pylint: disable=no-member
                                                   0,
                                                   QtWidgets.QSizePolicy.Expanding,
                                                   QtWidgets.QSizePolicy.Maximum))
        widget.set_layout(game_layout)
        self.central_widget.add_widget(widget)

    def add_clue_tracker_gui(self):
        """Adds clue tracker to main layout"""
        widget = QtWidgets.QWidget(self)
        tracker_layout = QtWidgets.QVBoxLayout()
        self.tracker_gui = ClueTrackerWidget(self)
        tracker_layout.add_widget(self.tracker_gui)
        tracker_layout.add_item(QtWidgets.QSpacerItem(0.25 * self.size.width(),  # pylint: disable=no-member
                                                      0,
                                                      QtWidgets.QSizePolicy.Expanding,
                                                      QtWidgets.QSizePolicy.Maximum))
        widget.set_layout(tracker_layout)
        self.central_widget.add_widget(widget)

    def add_menu_bar(self):
        """Adds Menu Bar to Layout"""
        menu_bar = QtWidgets.QMenuBar(self)
        self.set_menu_bar(menu_bar)

        game_menu = menu_bar.add_menu('&Game')
        start_action = game_menu.add_action('Start &Game')
        start_action.shortcut = 'Ctrl+g'
        self.connect(start_action,
                     QtCore.SIGNAL('triggered()'),
                     self.start_game)
        check_action = game_menu.add_action('Check Game Status')
        check_action.shortcut = 'Ctrl+r'
        self.connect(check_action,
                     QtCore.SIGNAL('triggered()'),
                     self.check_game_status)
        end_action = game_menu.add_action('End Turn')
        end_action.shortcut = 'Ctrl+e'
        self.connect(end_action,
                     QtCore.SIGNAL('triggered()'),
                     self.end_turn)

        help_menu = menu_bar.add_menu('&Help')
        help_menu.add_action('&Rules')
        about_action = help_menu.add_action('&About')
        about_action.shortcut = 'Ctrl+a'
        self.connect(about_action,
                     QtCore.SIGNAL('triggered()'),
                     self.show_about_message)

    def show_suspect_select_menu(self):
        """Shows character selection menu"""
        suspect_menu = CharacterSelect(self)
        suspect_menu.exec_()

    def show_about_message(self):
        """Show About Message Popup"""
        response = self.game_instance.about()
        QtWidgets.QMessageBox.information(self, 'About', response)

    def show(self):
        """Initialze Game GUI if Game Login Succeeds"""
        join_menu = JoinMenu(self)
        result = join_menu.exec_()
        if result == QtWidgets.QDialog.Accepted:
            super().show()
            self.socket.start_connection()
            return True
        return False

    def start_game(self):
        """Start Current Game"""
        result, message = self.game_instance.start_game()
        if result:
            QtWidgets.QMessageBox.information(self, 'Success', message.title())
            self.game_gui.game_board.set_player(
                self.game_instance.player.suspect)

        if not result:
            QtWidgets.QMessageBox.warning(self, 'Oops', message.title())

        self.update_game_info_text()

        result, player_dict = self.get_player_locs()
        if result:
            self.chat_gui.set_tabs(player_dict.keys())

    def check_game_status(self):
        """Check Status of Current Game"""
        result, message = self.game_instance.check_game_status()
        if result:
            QtWidgets.QMessageBox.information(self, 'Success', message.title())
            self.game_gui.game_board.set_player(
                self.game_instance.player.suspect)

        if not result:
            QtWidgets.QMessageBox.warning(self, 'Oops', message.title())

        self.game_gui.update_cards(self.game_instance.player.hand)

        self.update_game_info_text()

        result, player_dict = self.get_player_locs()
        if result:
            self.chat_gui.set_tabs(player_dict.keys())

    def get_player_locs(self):
        """Get dictionary of players and locations"""
        result, player_dict = self.game_instance.get_player_locs()
        return result, player_dict

    def end_turn(self):
        """Notifies server that turn is complete"""
        result, message = self.game_instance.end_turn()
        if result:
            QtWidgets.QMessageBox.information(self, 'Success', message.title())
        if not result:
            QtWidgets.QMessageBox.warning(self, 'Oops', message.title())

    def socket_event(self, event_type, event):
        """Handles Event notifications from websocket"""
        # Add all events to Log
        self.game_gui.update_log(event)

        if event_type == 'event':
            # Add actions here based on message content
            pass

        self.game_gui.game_board.update_all_positions()

    def socket_message(self, msg_type, message):  # pylint: disable=no-self-use # update when messaging added
        """Handles Event notifications from websocket"""
        self.chat_gui.receive_message(msg_type, message)


class JoinMenu(QtWidgets.QDialog):
    """Popup Menu for Starting/Joining Games

    Attributes:
        game_name_box (QtWidgets.QLineEdit): Set Game Name - New Game
        create_password_box (QtWidgets.QLineEdit): Set Game Password - New Game
        create_username_box (QtWidgets.QLineEdit): Set Player Username - New Game
        game_code_box (QtWidgets.QLineEdit): Set GameId Value - Join Game
        join_password_box (QtWidgets.QLineEdit): Set Game Password - Join Game
        join_username_box (QtWidgets.QLineEdit): Set Player Username - New Game
    """

    def __init__(self, parent):
        super().__init__(parent)
        menu_layout = QtWidgets.QHBoxLayout()
        self._game_instance = parent.game_instance

        # Set Up Start Game Options
        new_game_layout = QtWidgets.QVBoxLayout()
        new_game_layout.add_widget(QtWidgets.QLabel('New Game'))
        line = QtWidgets.QFrame()
        line.frame_shape = QtWidgets.QFrame.HLine
        line.frame_shadow = QtWidgets.QFrame.Sunken
        new_game_layout.add_widget(line)
        new_game_layout.add_widget(QtWidgets.QLabel('Game Name'))
        self.game_name_box = QtWidgets.QLineEdit(self)
        new_game_layout.add_widget(self.game_name_box)
        new_game_layout.add_widget(
            QtWidgets.QLabel('Set Game Password (Optional)'))
        self.create_password_box = QtWidgets.QLineEdit(self)
        self.create_password_box.echo_mode = QtWidgets.QLineEdit.Password
        new_game_layout.add_widget(self.create_password_box)
        new_game_layout.add_widget(QtWidgets.QLabel('Username'))
        self.create_username_box = QtWidgets.QLineEdit(self)
        new_game_layout.add_widget(self.create_username_box)
        new_game_button = QtWidgets.QPushButton('Start', self)
        self.connect(new_game_button,
                     QtCore.SIGNAL('clicked()'),
                     self.start_new_game)
        new_game_layout.add_widget(new_game_button)
        menu_layout.add_layout(new_game_layout)

        # Add Vertical Seperator
        line = QtWidgets.QFrame()
        line.frame_shape = QtWidgets.QFrame.VLine
        line.frame_shadow = QtWidgets.QFrame.Sunken
        menu_layout.add_widget(line)

        # Set Up Join Game Options
        join_game_layout = QtWidgets.QVBoxLayout()
        join_game_layout.add_widget(QtWidgets.QLabel('Join Game'))
        line = QtWidgets.QFrame()
        line.frame_shape = QtWidgets.QFrame.HLine
        line.frame_shadow = QtWidgets.QFrame.Sunken
        join_game_layout.add_widget(line)
        join_game_layout.add_widget(QtWidgets.QLabel('Game Code'))
        self.game_code_box = QtWidgets.QLineEdit(self)
        self.game_code_box.set_validator(QtGui.QIntValidator())
        join_game_layout.add_widget(self.game_code_box)
        join_game_layout.add_widget(
            QtWidgets.QLabel('Game Password (Optional)'))
        self.join_password_box = QtWidgets.QLineEdit(self)
        self.join_password_box.echo_mode = QtWidgets.QLineEdit.Password
        join_game_layout.add_widget(self.join_password_box)
        join_game_layout.add_widget(QtWidgets.QLabel('Username'))
        self.join_username_box = QtWidgets.QLineEdit(self)
        join_game_layout.add_widget(self.join_username_box)
        join_game_button = QtWidgets.QPushButton('Join', self)
        self.connect(join_game_button,
                     QtCore.SIGNAL('clicked()'),
                     self.join_game)
        join_game_layout.add_widget(join_game_button)
        menu_layout.add_layout(join_game_layout)

        self.set_layout(menu_layout)

    def start_new_game(self):
        """Start New Game using User Provided Responses"""
        game_name = str(self.game_name_box.text).strip()
        password = self.create_password_box.text
        username = str(self.create_username_box.text).strip()

        if game_name and username:
            result, message = self._game_instance.create_game(game_name=game_name,
                                                              password=password)
            if result:
                result, message = self._game_instance.join_game(game_id=self._game_instance.game_id,
                                                                username=username,
                                                                password=password)
                if result:
                    QtWidgets.QMessageBox.information(self,
                                                      'Success',
                                                      message.title())
                    super().accept()

            if not result:
                QtWidgets.QMessageBox.warning(self, 'Oops', message.title())

    def join_game(self):
        """Join Existing Game using User Provided Responses"""
        game_id = int(self.game_code_box.text)
        password = self.join_password_box.text
        username = str(self.join_username_box.text).strip()

        if game_id and username:
            result, message = self._game_instance.join_game(game_id=game_id,
                                                            username=username,
                                                            password=password)
            if result:
                QtWidgets.QMessageBox.information(self,
                                                  'Success',
                                                  message.title())
                super().accept()

            if not result:
                QtWidgets.QMessageBox.warning(self, 'Oops', message.title())


class CharacterSelect(QtWidgets.QDialog):
    """Create a form for making Accusations

    Attributes:
        suspect (str): Name of suspect selected
        suspect_selector (QtWidgets.QComboBox): Dropdown for selecting suspect
    """

    def __init__(self, parent):
        super().__init__(parent)
        self.window_title = 'Select Suspect'
        self._parent = parent
        self.suspect = None

        form = QtWidgets.QFormLayout()
        self.suspect_selector = QtWidgets.QComboBox(self)
        suspects = Suspects.get_suspect_list()
        self.suspect_selector.add_items(['Random'] + suspects)
        form.add_row(QtWidgets.QLabel('Suspects'), self.suspect_selector)

        accept_button = QtWidgets.QPushButton('Select', self)
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
        self.suspect = self.suspect_selector.current_text
        if self.suspect == 'Random':
            super().reject()
        else:
            status, message = self._parent.game_instance.select_suspect(
                self.suspect)
            if status:
                QtWidgets.QMessageBox.information(self, 'Success', message)
                super().accept()
            else:
                QtWidgets.QMessageBox.warning(self, 'Oops', message)

    def reject(self):
        """Override of QDialog reject method, alerts user of random suspect"""
        self.suspect = None
        QtWidgets.QMessageBox.information(self,
                                          'Alert',
                                          'Random Suspect will be selected')
        super().reject()
