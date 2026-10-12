from src.model.direction import Direction
from enum import Enum
from src.model.position import Position


class Dots(Enum):
    SMALL = 1
    BIG = 2
    NONE = 3


class Cell:
    def __init__(self, walls: int) -> None:
        self.walls = walls

    def has_wall(self, direction: Direction) -> bool:
        return (self.walls & direction.value) != 0


class Pacgum:
    def __init__(self, position: Position) -> None:
        self.position = position


# cell = Cell(3)
# print(cell.has_Wall(Direction.NORTH))
# print(cell.has_Wall(Direction.EAST))
# print(cell.has_Wall(Direction.SOUTH))
# print(cell.has_Wall(Direction.WEST))
