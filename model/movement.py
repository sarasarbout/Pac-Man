from model.pacman import Pacman
from model.maze import Maze
from model.position import Position
from model.direction import Direction
from mazegenerator import MazeGenerator


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



# ==== Test ====
# if __name__ == "__main__":
#     grid = [
#         [9, 1, 1, 1, 1, 5, 1, 5, 1, 5, 5, 5, 5, 3, 11],
#         [10, 10, 12, 4, 4, 1, 4, 1, 6, 9, 5, 1, 3, 12, 2],
#         [10, 10, 9, 5, 5, 6, 13, 0, 5, 6, 9, 4, 4, 3, 10],
#         [10, 8, 4, 1, 1, 5, 3, 14, 9, 1, 4, 1, 5, 0, 6],
#         [8, 2, 9, 4, 4, 3, 12, 5, 4, 4, 5, 4, 1, 2, 11],
#         [12, 6, 12, 3, 15, 8, 5, 3, 15, 15, 15, 9, 4, 2, 10],
#         [9, 1, 5, 2, 15, 12, 5, 0, 5, 7, 15, 8, 3, 8, 2],
#         [8, 4, 1, 6, 15, 15, 15, 10, 15, 15, 15, 14, 10, 12, 2],
#         [8, 3, 8, 5, 5, 3, 15, 10, 15, 13, 5, 1, 4, 5, 2],
#         [10, 8, 0, 3, 9, 2, 15, 10, 15, 15, 15, 12, 1, 1, 2],
#         [10, 10, 10, 14, 12, 4, 3, 8, 1, 1, 1, 5, 4, 6, 10],
#         [10, 8, 4, 1, 5, 3, 10, 10, 10, 12, 2, 9, 1, 5, 2],
#         [10, 8, 1, 4, 1, 2, 10, 8, 4, 1, 2, 12, 2, 9, 2],
#         [12, 6, 10, 9, 2, 10, 8, 2, 9, 2, 8, 7, 8, 4, 2],
#         [13, 5, 4, 4, 4, 4, 4, 4, 6, 12, 4, 5, 4, 5, 6]
#     ]
#     maze = Maze(grid)

#     pacman = Pacman(Direction.EAST, Position(0, 1))
#     movement = Movement()

#     print("Before:", pacman.position)
#     print("Can move:", maze.can_move(pacman.position, pacman.direction))

#     movement.move(pacman, maze)

#     print("After:", pacman.position)