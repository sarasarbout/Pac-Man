from src.draw.generate import create_the_maze
from src.model.pacman import Pacman
from src.model.position import Position
from src.model.direction import Direction
from src.model.game_state import GameStatus
from src.ui.main_menu import main_menu
from src.ui.cheat_menu import CheatState
from src.ui.pause_menu import pause_menu
from src.ui.game_over import game_over
from src.ui.highscores import highscores
from src.parser.config_parser import GameConfig
import pygame
from src.ui.instructions import instructions
from src.ui.victory import victory


def run_game(
            config: GameConfig, screen: pygame.Surface, level_index: int,
            cheats: CheatState,
            pacman: Pacman
        ) -> str:
    """Initialize and run the selected maze level."""

    # pacman = Pacman(
    #     Direction.NONE,
    #     Position(4, 1),
    #     GameStatus.READY
    # )

    level = config.levels[level_index]
    pacman.direction = Direction.NONE
    pacman.position = Position(4, 1)
    pacman.mode = GameStatus.READY

    result: str = create_the_maze(
        pacman,
        0.3,
        config,
        screen,
        level,
        level_index,
        cheats
    )
    return result


def main(config: GameConfig, screen: pygame.Surface) -> None:
    """Manage transitions between application states."""

    state = "main_menu"
    level_index = 0
    final_score = 0
    cheats: CheatState = {
        "Invincibility": False,
        "Freeze Ghosts": False,
        "Speed Boost": False
    }
    while True:
        if state == "main_menu":
            state, cheats = main_menu(config, screen, cheats)

            """reset the game state"""
            if state == "playing":
                level_index = 0
                final_score = 0

                pacman = Pacman(
                    Direction.NONE,
                    Position(4, 1),
                    GameStatus.READY
                )

        elif state == "playing":
            state = run_game(
                config, screen, level_index, cheats, pacman
            )
            final_score = pacman.score

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
            state = instructions(config, screen)

        elif state == "victory":
            state = victory(config, screen, final_score)

            if state == "playing":
                level_index = 0
                final_score = 0

        elif state == "exit":
            return
