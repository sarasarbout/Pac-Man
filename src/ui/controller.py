from src.draw.generate import create_the_maze
from src.model.pacman import Pacman
from src.model.position import Position
from src.model.direction import Direction
from src.model.game_state import GameStatus
from src.ui.main_menu import main_menu
from src.ui.pause_menu import pause_menu
from src.ui.game_over import game_over
from src.ui.highscores import highscores
from src.parser.config_parser import GameConfig
import pygame


def run_game(config: GameConfig, screen, level_index: int) -> tuple[str, int]:
    """Initialize and run the selected maze level."""

    pacman = Pacman(
        Direction.EAST,
        Position(4, 1),
        GameStatus.READY
    )

    # level 1 for now
    level = config.levels[level_index]

    result = create_the_maze(
        pacman,
        0.3,
        config,
        screen,
        level,
        level_index
    )

    print("Gameplay returned:", result)
    print("Final score:", pacman.score)
    return result, pacman.score


def main(config: GameConfig, screen: pygame.Surface) -> None:
    """Manage transitions between application states."""

    state = "main_menu"
    level_index = 0
    final_score = 0
    while True:
        if state == "main_menu":
            state = main_menu(config, screen)

        elif state == "playing":
            state, final_score = run_game(config, screen, level_index)
            if state == "level_complete":
                if level_index + 1 < len(config.levels):
                    level_index += 1
                    state = "playing"
                else:
                    state = "victory"

        elif state == "pause_menu":
            state = pause_menu(config, screen)

        elif state == "game_over":
            state = game_over(config, screen, final_score)

        elif state == "highscores":
            state = highscores(config, screen)

        elif state == "instructions":
            state = "instructions"

        elif state == "exit":
            return

        elif state == "victory":
            return
