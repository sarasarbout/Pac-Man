from model.pacman import Pacman
from model.maze import Maze
from model.position import Position
from model.direction import Direction


class Movement:
    def get_next_position(self, position: Position, direction: Direction) -> Position:
        if direction == Direction.NORTH:
            return Position(position.x, position.y - 1)
        elif direction == Direction.WEST:
            return Position(position.x - 1, position.y)
        elif direction == Direction.EAST:
            return Position(position.x + 1, position.y)
        elif direction == Direction.SOUTH:
            return Position(position.x, position.y + 1)

    def move(self, pacman: Pacman, maze: Maze) -> None:
        if not (maze.can_move(pacman.position, pacman.direction)):
            return None
        new_position = self.get_next_position(pacman.position, pacman.direction)
        pacman.position = new_position