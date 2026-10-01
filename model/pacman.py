from model.position import Position
from model.direction import Direction
from model.game_state import GameStatus


class Pacman:
    def __init__(self, direction: Direction, position: Position, mode: GameStatus, lives: int = 3 , score: int = 0):
        self.direction = direction
        self.position = position
        self.lives = lives
        self.score = score
        self.mode = mode


# ====== Test =======

# mk = Pacman(Direction.EAST, Position(4, 1))
# print(mk.direction)
# print(mk.position)
# print(mk.lives)