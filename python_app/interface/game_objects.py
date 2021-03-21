"""Clue Game Objects
To include Player, Card, Suspect, Weapon, Location
"""


class Player:  # pylint: disable=too-few-public-methods # Will need updates
    """Store current Player information"""

    def __init__(self):
        self.username = None
        self.uuid = None
        self.game_id = None
        self.suspect = None
        self.cards = []
        self.location = None
        self.status = None
