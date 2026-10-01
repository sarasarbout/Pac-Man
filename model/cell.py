from model.direction import Direction
from enum import Enum


class Dots(Enum):
    SMALL = 1
    BIG = 2
    NONE


class Cell:
    def __init__(self, walls: int, dots: Dots) -> None:
        self.walls = walls
        self.dots = dots

    def has_wall(self, direction: Direction) -> bool:
        return (self.walls & direction.value) != 0


# cell = Cell(3)
# print(cell.has_Wall(Direction.NORTH))
# print(cell.has_Wall(Direction.EAST))
# print(cell.has_Wall(Direction.SOUTH))
# print(cell.has_Wall(Direction.WEST))
