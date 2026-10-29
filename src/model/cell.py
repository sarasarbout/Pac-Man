from src.model.direction import Direction
from enum import Enum
from src.model.position import Position


class Cell:
    def __init__(self, walls: int) -> None:
        self.walls = walls

    def has_wall(self, direction: Direction) -> bool:
        return (self.walls & direction.value) != 0


class Pacgum:
    def __init__(self, position: Position) -> None:
        self.position = position
