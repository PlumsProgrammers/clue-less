"""GUI Elements for Chat Widget"""
from PySide6.QtWidgets import (QVBoxLayout, QHBoxLayout, QTextEdit,
                               QPushButton, QSpacerItem,
                               QFrame, QSizePolicy)
from __feature__ import snake_case, true_property  # pylint: disable=unused-import # used for making Qt pythonic


class ChatWidget(QFrame):
    """Chat Layout"""

    def __init__(self, parent):
        """Adds chat to main layout"""
        super().__init__()
        self._parent = parent
        self.chat_layout = QVBoxLayout()
        self.frame_shape = QFrame.StyledPanel

        top_layout = QHBoxLayout()
        self.chat_box = QTextEdit('Chat coming soon')
        self.chat_box.read_only = True
        top_layout.add_widget(self.chat_box)
        # pylint: disable=no-member
        top_layout.add_item(QSpacerItem(0,
                                        int(self.size.height()),
                                        QSizePolicy.Minimum,
                                        QSizePolicy.Maximum))
        self.chat_layout.add_layout(top_layout)

        bottom_layout = QHBoxLayout()
        message_box = QTextEdit('Type to Chat', self)
        bottom_layout.add_widget(message_box)
        button = QPushButton('Send', self)
        bottom_layout.add_widget(button)
        self.chat_layout.add_layout(bottom_layout)

        self.set_layout(self.chat_layout)
