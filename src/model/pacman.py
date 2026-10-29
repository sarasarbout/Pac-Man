from src.model.position import Position
from src.model.direction import Direction
from src.model.game_state import GameStatus


class Pacman:
    def __init__(self, direction: Direction, position: Position, mode: GameStatus, lives: int = 3 , score: int = 0):
        self.direction = direction
        self.position = position
        self.lives = lives
        self.score = score
        self.mode = mode
