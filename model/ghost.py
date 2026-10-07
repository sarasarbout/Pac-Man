from model.direction import Direction
from model.position import Position
from enum import Enum


class Color(Enum):
    RED = 1
    PINK = 2
    CYAN = 3
    ORANGE = 4


class GhostMode(Enum):
    """Blinky trying to chase pacman ,As Pac-Man eats enough dots, Blinky becomes faster and increasingly aggressive, it starts from the top-right corner"""
    """Pinky tries to predict where Pac-Man is going, it start from the left-top corner"""
    """Inky depends on both pacman and blinky to calculate its position"""
    """Clyde: is the funniest one, it chases pacman when he gets close he runs away, it starts from the left-down corner"""
    CHASE = 1
    SCATTER = 2
    FRIGHTENED = 3


class GhostName(Enum):
    BLINKY = 1
    PINKY = 2
    INKY = 3
    CLYDE = 4


class Ghost:
    def __init__(self, name: str, position: Position, direction: Direction, color: Color, mode: GhostMode):
        self.position = position
        self.direction = direction
        self.color = color
        self.mode = mode
        self.name = name


# ======== Test ========

# ghost = Ghost(GhostName.BLINKY, Position(0, 1), Direction.SOUTH, COLOR.RED, GhostMode.CHASE)
# print(ghost.name)
# print(ghost.color)
# print(ghost.position)
# print(ghost.direction)
# print(ghost.mode)