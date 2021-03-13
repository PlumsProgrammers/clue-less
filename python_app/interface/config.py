# -*- coding: utf-8 -*-
"""User Configuration"""
import os


class ConfigManager:
    """Stores and access information about local configuration"""

    def __init__(self):
        self._host_location = r'http://localhost:' + \
            os.environ.get('PORT') + '/'
        self._user = os.environ.get('USER')

    def get_host(self):
        """Getter method for path to server"""
        return self._host_location

    def get_user(self):
        """Getter method for username"""
        return self._user
