"""Adds Websocket Connections for Python Client"""

from PySide6 import QtCore

import socketio


class WebSocket(QtCore.QThread):
    """Creates websocket connection running on a separate thread"""

    def __init__(self):
        super().__init__()
        self._config = None
        self.running = False
        self.game_instance = None
        self.socket = socketio.Client()

    def setup(self, game, config):
        """Sets up required attributes for connecting to game

        Args:
            game (Clueless): Game Insance that the Socket is communicating to
            config (ConfigManager): Manages path to Clueless Server
        """
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
        self.socket.wait()

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
        thread.game_instance.event('Connected')


@ sio.event
def connect_error(error):
    """Method that runs on Websocket connection error"""
    if thread.game_instance is not None:
        thread.game_instance.event(f'Connection Error: {error}')


@ sio.event
def disconnect():
    """Method that runs when Websocket disconnects"""
    if thread.game_instance is not None:
        thread.game_instance.event('Disconnected')


@ sio.on('game')
def game_event(data):
    """Method handles all Game events"""
    if thread.game_instance is not None:
        thread.game_instance.event(f'Message: {data}')


@ sio.on('message')
def group_message(data):
    """Method handles all Whole Game messages"""
    if thread.game_instance is not None:
        thread.game_instance.event(f'Message: {data}')


@ sio.on('private')
def private_message(data):
    """Method handles all Private message"""
    if thread.game_instance is not None:
        thread.game_instance.event(f'Message: {data}')
