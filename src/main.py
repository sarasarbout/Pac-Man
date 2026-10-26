from pathlib import Path

from src.parser.config_parser import ConfigParser, ConfigError, GameConfig
from src.ui.controller import main as run_controller
import pygame


def main() -> None:
    try:
        # 1. Locate config.json relative to this file
        project_root = Path(__file__).resolve().parent
        config_path = project_root / "config.json"

        # 2. Load configuration
        parser = ConfigParser(str(config_path))
        config: GameConfig = parser.config_data

        # 3. Initialize Pygame
        pygame.init()
        level = config.levels[0]
        maze_width = level["width"] * config.cell_size
        maze_height = level["height"] * config.cell_size
        info = pygame.display.Info()
        max_width = info.current_w
        max_height = info.current_h
        # 4. Create the display
        if max_width < maze_width or max_height < maze_height:
            print("Level rejected: maze is too large for your screen!")
            return
        config.screen_width = level["width"] * config.cell_size
        config.screen_height = level["height"] * config.cell_size + 120
        screen = pygame.display.set_mode(
            (config.screen_width, config.screen_height)
        )
        pygame.display.set_caption("Pac-Man")

        # 5. Start the controller
        run_controller(config, screen)

    except ConfigError as error:
        print(f"Configuration error: {error}")

    finally:
        pygame.quit()


if __name__ == "__main__":
    main()
