from model.cell import Cell
from model.direction import Direction
from model.position import Position
from mazegenerator import MazeGenerator


class Maze:
    def __init__(self, grid: list[list[int]]):
        self.width = len(grid[0])   # cells inside row
        self.height = len(grid)    # rows
        self.cells = [
                    [Cell(value) for value in row]
                    for row in grid]

    def get_cell(self, position: Position) -> Cell:
        return self.cells[position.y][position.x]

    def has_wall(self, position: Position, direction: Direction) -> bool:
        return self.get_cell(position).has_Wall(direction)


generator = MazeGenerator()
maze = Maze(generator.maze)

position = Position(0, 0)

print(maze.has_wall(position, Direction.NORTH))
print(maze.has_wall(position, Direction.EAST))
print(maze.has_wall(position, Direction.WEST))
print(maze.has_wall(position, Direction.SOUTH))
