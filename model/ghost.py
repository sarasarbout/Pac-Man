from model.direction import Direction
from model.position import Position
from enum import Enum


class Color(Enum):
    RED = 1
    BLUE = 2
    GREEN = 3
    ORANGE = 4


class GhostMode(Enum):
    """blinky trying to chase pacman ,As Pac-Man eats enough dots, Blinky becomes faster and increasingly aggressive"""
    """Pinky tries to predict where Pac-Man is going, it start from the left-top corner"""
    CHASE = 1
    SCATTER = 2
    FRIGHTENED = 3


class Ghost:
    def __init__(self, position: Position, direction: Direction, color: Color):
        pass