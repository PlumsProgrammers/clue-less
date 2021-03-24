"""GUI Elements for Chat Widget"""
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                               QTextEdit, QPushButton, QSpacerItem,
                               QSizePolicy)
from __feature__ import snake_case, true_property  # pylint: disable=unused-import # used for making Qt pythonic


class ChatWidget(QWidget):
    """Chat Layout"""

    def __init__(self, parent):
        """Adds chat to main layout"""
        super().__init__()
        self._parent = parent
        self.chat_layout = QVBoxLayout()

        top_layout = QHBoxLayout()
        chat_box = QTextEdit('Chat coming soon')
        chat_box.is_read_only = True
        top_layout.add_widget(chat_box)
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
