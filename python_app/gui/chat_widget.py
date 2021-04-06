"""GUI Elements for Chat Widget"""
from PySide6 import QtWidgets  # pylint: disable=no-name-in-module # GitHub Actions cant import Qt modules
from __feature__ import snake_case, true_property  # pylint: disable=unused-import # used for making Qt pythonic


class ChatWidget(QtWidgets.QFrame):
    """Chat Layout"""

    def __init__(self, parent):
        """Adds chat to main layout"""
        super().__init__()
        self._parent = parent
        self.chat_layout = QtWidgets.QVBoxLayout()
        self.frame_shape = QtWidgets.QFrame.StyledPanel

        top_layout = QtWidgets.QHBoxLayout()
        self.chat_box = QtWidgets.QTextEdit('Chat coming soon')
        self.chat_box.read_only = True
        top_layout.add_widget(self.chat_box)
        # pylint: disable=no-member
        top_layout.add_item(QtWidgets.QSpacerItem(0,
                                                  int(self.size.height()),
                                                  QtWidgets.QSizePolicy.Minimum,
                                                  QtWidgets.QSizePolicy.Maximum))
        self.chat_layout.add_layout(top_layout)

        bottom_layout = QtWidgets.QHBoxLayout()
        message_box = QtWidgets.QTextEdit('Type to Chat', self)
        bottom_layout.add_widget(message_box)
        button = QtWidgets.QPushButton('Send', self)
        bottom_layout.add_widget(button)
        self.chat_layout.add_layout(bottom_layout)

        self.set_layout(self.chat_layout)
