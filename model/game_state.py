from enum import Enum
from model.pacman import Pacman
from model.ghost import Ghost
from game.collision import Collision


class GameStatus(Enum):
    READY = 1
    PLAYING = 2
    PAUSED = 3
    GAME_OVER = 4
    WON = 5


class GameState:
    def __init__(self, pacman: Pacman, ghosts: list[Ghost], status: GameStatus.READY, score: 0) -> None:
        self.pacman = pacman
        self.ghosts = ghosts
        self.status = status
        self.score = score


class Rules:
    def check_collision(self, state: GameState) -> Ghost | None:
        collision = Collision()
        for ghost in state.ghosts:
            if collision.check(state.pacman, ghost):
                return ghost
        return None

    def handle_collision(self, state: GameState) -> None:
        ghost = state.check_collision(state)
        if ghost:
            if ghost.mode != state.FRIGHTENED:
                state.pacman.lives -= 1


    def check_game_over(self, state: GameState):
        pass

    def check_win(self, state: GameState):
        pass
