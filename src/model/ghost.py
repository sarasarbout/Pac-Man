from src.model.position import Position
from enum import Enum


class Color(Enum):
    RED = 1
    PINK = 2
    CYAN = 3
    ORANGE = 4


class GhostMode(Enum):
    CHASE = 1
    frightened = 2
    DEAD = 3


class GhostName(Enum):
    BLINKY = 1
    PINKY = 2
    INKY = 3
    CLYDE = 4


class Ghost:
    def __init__(self, position: Position, name: GhostName):
        self.position = position
        self.mode = GhostMode.CHASE
        self.name = name
        self.frightened_until = 0
        self.x = position.x * 50
        self.y = position.y * 50
        self.dead_until = 0