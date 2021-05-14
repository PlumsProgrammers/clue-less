"""Adds Websocket Connections for Python Client"""

from PySide6 import QtCore

import socketio


class WebSocket(QtCore.QThread):
    """Creates websocket connection running on a separate thread"""

    def __init__(self):
        super().__init__()
        self._config = None
        self.gui = None
        self.game_instance = None
        self.socket = socketio.Client()
        self.waiting = False

    def setup(self, gui, game, config):
        """Sets up required attributes for connecting to game

        Args:
            gui (MainWindow): Clueless GUI main window instance
            game (Clueless): Game Insance that the Socket is communicating to
            config (ConfigManager): Manages path to Clueless Server
        """
        self.gui = gui
        self.game_instance = game
        self._config = config

    def start_connection(self):
        """Starts websocket connection to Clueless Server"""
        if self._config:
            query = f'?gameId={self.game_instance.game_id}&' +\
                f'uuid={self.game_instance.player.uuid}'
            path = self._config.get_host() + query
            self.socket.connect(path)

    def run(self):
        """Starts socket running in a second thread"""
        try:
            self.socket.wait()
        except Exception as error:
            print('Socket Exception in run!', error)

    def end_connection(self):
        """Ends websocket connection and ends second thread"""
        self.socket.disconnect()


thread = WebSocket()
sio = thread.socket


def get_socket():
    """Get instance of the Websocket Thread"""
    return thread


@ sio.event
def connect():
    """Method that runs on Websocket connection"""
    if thread.game_instance is not None:
        thread.gui.socket_event(event_type='status',
                                event='Connected')


@ sio.event
def connect_error(error):
    """Method that runs on Websocket connection error"""
    print('Socket Disconnected')
    if thread.game_instance is not None:
        thread.gui.socket_event(event_type='status',
                                event=f'Connection Error: {error}')


@ sio.event
def disconnect():
    """Method that runs when Websocket disconnects"""
    try:
        if thread.game_instance is not None:
            thread.gui.socket_event(event_type='status',
                                    event='Disconnected')

    except Exception as error:
        print('Socket Exception in disconnect!', error)


@ sio.on('game')
def game_event(data):
    """Method handles all Game events"""
    if thread.game_instance is not None:
        while thread.waiting:
            continue
        thread.waiting = True
        try:
            thread.gui.socket_event(event_type='event',
                                    event=f'Message: {data}')
            thread.waiting = False

        except Exception as error:
            print('Socket Exception in game_event!', error)


@ sio.on('message')
def group_message(data):
    """Method handles all Whole Game messages"""
    if thread.game_instance is not None:
        while thread.waiting:
            continue
        thread.waiting = True
        try:
            thread.gui.socket_message(msg_type='group',
                                      message=f'Message: {data}')
            thread.waiting = False

        except Exception as error:
            print('Socket Exception in group_message!', error)


@ sio.on('private')
def private_message(data):
    """Method handles all Private message"""
    if thread.game_instance is not None:
        while thread.waiting:
            continue
        thread.waiting = True
        try:
            thread.gui.socket_message(msg_type='private',
                                      message=f'Message: {data}')
            thread.waiting = False

        except Exception as error:
            print('Socket Exception in private_message!', error)
