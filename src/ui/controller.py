from src.mazegenerator.maze_game import create_the_maze
from src.model.pacman import Pacman
from src.model.position import Position
from src.model.direction import Direction
from src.model.game_state import GameStatus
from src.ui.menu import main_menu
from src.parser.config_parser import GameConfig
import pygame


def run_game(config: GameConfig, screen) -> str:
    """Initialize and run the selected maze level."""

    pacman = Pacman(
        Direction.EAST,
        Position(4, 1),
        GameStatus.READY
    )

    #level 1 for now.
    level = config.levels[0]

    return create_the_maze(
        pacman,
        0.3,
        config,
        screen,
        level
    )


def main(config: GameConfig, screen: pygame.Surface) -> None:
    """Manage transitions between application states."""

    state = "menu"

    while True:
        if state == "menu":
            state = main_menu(config, screen)

        elif state == "playing":
            state = run_game(config, screen)

        elif state == "highscores":
            state = "menu"

        elif state == "instructions":
            state = "menu"

        elif state == "exit":
            return
