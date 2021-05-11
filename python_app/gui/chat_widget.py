"""GUI Elements for Chat Widget"""
from PySide6 import QtCore  # pylint: disable=no-name-in-module # GitHub Actions cant import Qt modules
from PySide6 import QtWidgets  # pylint: disable=no-name-in-module # GitHub Actions cant import Qt modules
from __feature__ import snake_case, true_property  # pylint: disable=unused-import # used for making Qt pythonic


class ChatWidget(QtWidgets.QFrame):
    """Chat Layout"""

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.chat_layout = QtWidgets.QVBoxLayout()
        self.frame_shape = QtWidgets.QFrame.StyledPanel
        self.tabs = QtWidgets.QTabWidget()

        new_widget = IndividualChat(self, 'Game')
        self.tabs.add_tab(new_widget, 'All Players')
        self.tab_indexes = {'Game': new_widget}
        self.chat_layout.add_widget(self.tabs)
        self.set_layout(self.chat_layout)

    def set_tabs(self, names):
        """Adds tabs for each player"""
        self.tabs.clear()
        new_widget = IndividualChat(self, 'Game')
        self.tabs.add_tab(new_widget, 'All Players')
        self.tab_indexes = {'Game': new_widget}
        for player in names:
            new_widget = IndividualChat(self, player)
            self.tab_indexes[player] = new_widget
            self.tabs.add_tab(new_widget, player.title())

    def send_message(self, chat, message):
        """Sends message to game/player"""
        if chat == 'Game':
            self.parent.game_instance.send_public_message(message)
        else:
            self.parent.game_instance.send_private_message(chat, message)

    def receive_message(self, msg_type, message):
        """Add received message to chat window"""
        _, sender, message = message.split(':')
        if msg_type == 'group':
            tab = self.tab_indexes['Game']
            tab.add_msg(sender, message)
        else:
            tab = self.tab_indexes.get(sender, IndividualChat(None, None))
            tab.add_msg(sender, message)


class IndividualChat(QtWidgets.QFrame):
    """Chat Layout"""

    def __init__(self, parent, chat):
        """Adds chat to main layout"""
        super().__init__()
        self._parent = parent
        self.chat_room = chat
        self.chat_layout = QtWidgets.QVBoxLayout()
        self.frame_shape = QtWidgets.QFrame.StyledPanel

        top_layout = QtWidgets.QHBoxLayout()
        self.chat_box = ChatBox(self)
        self.chat_box.read_only = True
        top_layout.add_widget(self.chat_box)
        # pylint: disable=no-member
        top_layout.add_item(QtWidgets.QSpacerItem(0,
                                                  int(self.size.height()),
                                                  QtWidgets.QSizePolicy.Minimum,
                                                  QtWidgets.QSizePolicy.Maximum))
        self.chat_layout.add_layout(top_layout)

        bottom_layout = QtWidgets.QHBoxLayout()
        self.message_box = QtWidgets.QTextEdit('Type to Chat', self)
        bottom_layout.add_widget(self.message_box)
        button = QtWidgets.QPushButton('Send', self)
        self.connect(button,
                     QtCore.SIGNAL('clicked()'),
                     self.send)
        bottom_layout.add_widget(button)
        self.chat_layout.add_layout(bottom_layout)

        self.set_layout(self.chat_layout)

    def send(self):
        """Send message to player/group"""
        text = self.message_box.plain_text
        self._parent.send_message(self.chat_room,
                                  text)
        self.message_box.plain_text = ''

    def add_msg(self, username, message):
        """Adds message to message box"""
        self.chat_box.update_text(f'>{username}: {message}\n')


class ChatBox(QtWidgets.QScrollArea):
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
