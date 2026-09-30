from model.cell import Cell
from model.direction import Direction
from model.position import Position


class Maze:
    def __init__(self, grid: list[list[int]]):
        self.width = len(grid[0])
        self.height = len(grid)