from model.position import Position
from model.direction import Direction


class Pacman:
    def __init__(self, direction: Direction, position: Position, lives: int = 3):
        self.direction = direction
        self.position = position
        self.lives = lives


# ====== Test =======

# mk = Pacman(Direction.EAST, Position(4, 1))
# print(mk.direction)
# print(mk.position)
# print(mk.lives)