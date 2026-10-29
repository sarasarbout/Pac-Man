from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.model.pacman import Pacman
from enum import Enum
from src.model.ghost import Ghost
from src.game.collision import Collision
from src.model.ghost import GhostMode


class GameStatus(Enum):
    READY = 1
    PLAYING = 2
    PAUSED = 3
    GAME_OVER = 4
    WON = 5


class GameState:
    def __init__(
            self, pacman: "Pacman", ghosts: list[Ghost],
            status: GameStatus = GameStatus.READY
    ) -> None:
        self.pacman = pacman
        self.ghosts = ghosts
        self.status = status
