"""Central GUI for Clue-less game"""
from PySide6.QtCore import QRect
from PySide6.QtWidgets import (QMainWindow, QWidget,
                               QVBoxLayout, QSplitter,
                               QSpacerItem, QSizePolicy)

from gui.chat_widget import ChatWidget
from gui.game_widget import GameWidget
from gui.tracker_widget import ClueTrackerWidget

from resources.resource_manager import ImageManager

from __feature__ import snake_case, true_property  # pylint: disable=unused-import # used for making Qt pythonic


class MainWindow(QMainWindow):
    """Main Layout"""

    def __init__(self, app):
        super().__init__()
        self._screen_size = app.primary_screen.size

        self.image_mgr = ImageManager()
        self.image_mgr.load_images()

        self.window_title = 'Clue-less'
        self.geometry = QRect(0, 0,
                              self._screen_size.width(),
                              self._screen_size.width())
        self.central_widget = QSplitter(self)

        self.add_chat_gui()
        self.add_game_gui()
        self.add_clue_tracker_gui()

        self.set_central_widget(self.central_widget)

    def add_chat_gui(self):
        """Create chat GUI Layout"""
        widget = QWidget(self)
        chat_layout = QVBoxLayout()
        self.chat_gui = ChatWidget(self)
        chat_layout.add_widget(self.chat_gui)
        chat_layout.add_item(QSpacerItem(0.25 * self.size.width(),
                                         0,
                                         QSizePolicy.Expanding,
                                         QSizePolicy.Maximum))
        widget.set_layout(chat_layout)
        self.central_widget.add_widget(widget)

    def add_game_gui(self):
        """Create game GUI Layout"""
        widget = QWidget(self)
        game_layout = QVBoxLayout()
        self.game_gui = GameWidget(self, self.image_mgr)
        game_layout.add_widget(self.game_gui)
        game_layout.add_item(QSpacerItem(0.5 * self.size.width(),
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
        tracker_layout.add_item(QSpacerItem(0.25 * self.size.width(),
                                            0,
                                            QSizePolicy.Expanding,
                                            QSizePolicy.Maximum))
        widget.set_layout(tracker_layout)
        self.central_widget.add_widget(widget)
