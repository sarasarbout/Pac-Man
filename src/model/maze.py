from src.model.cell import Cell
from src.model.direction import Direction
from src.model.position import Position


class Maze:
    def __init__(self, grid: list[list[int]]) -> None:
        self.width = len(grid[0])   # cells inside row
        self.height = len(grid)    # rows
        self.cells = [
                    [Cell(value) for value in row]
                    for row in grid]

    def get_cell(self, position: Position) -> Cell:
        return self.cells[position.y][position.x]

    def has_wall(self, position: Position, direction: Direction) -> bool:
        return bool(self.get_cell(position).has_wall(direction))

    def can_move(self, position: Position, direction: Direction) -> bool:
        if self.has_wall(position, direction):
            return False

        if direction == Direction.NORTH:
            new_position = Position(position.x, position.y - 1)
        elif direction == Direction.EAST:
            new_position = Position(position.x + 1, position.y)
        elif direction == Direction.SOUTH:
            new_position = Position(position.x, position.y + 1)
        elif direction == Direction.WEST:
            new_position = Position(position.x - 1, position.y)
        else:
            return False

        if not (
            0 <= new_position.x < self.width
            and 0 <= new_position.y < self.height
        ):
            return False

        return True
