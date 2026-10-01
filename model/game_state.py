from enum import Enum
from model.pacman import Pacman
from model.ghost import Ghost
from game.collision import Collision
from model.ghost import GhostMode


class GameStatus(Enum):
    READY = 1
    PLAYING = 2
    PAUSED = 3
    GAME_OVER = 4
    WON = 5


class GameState:
    def __init__(
            self, pacman: Pacman, ghosts: list[Ghost],
            status: GameStatus = GameStatus.READY, ghost_eaten_count: int = 0
    ) -> None:
        self.pacman = pacman
        self.ghosts = ghosts
        self.status = status
        self.ghost_eaten_count = ghost_eaten_count


class Rules:
    def check_collision(self, state: GameState) -> Ghost | None:
        collision = Collision()
        for ghost in state.ghosts:
            if collision.check(state.pacman, ghost):
                return ghost
        return None

    def handle_collision(self, state: GameState) -> None:
        ghost = self.check_collision(state)
        if ghost:
            if ghost.mode != GhostMode.FRIGHTENED:
                state.pacman.lives -= 1
            else:
                state.ghost_eaten_count += 1
                state.pacman.score += 200

    def check_game_over(self, state: GameState):
        return state.pacman.lives <= 0

    def check_win(self, state: GameState):
        pass
