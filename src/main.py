from src.parser.config_parser import ConfigParser, ConfigError, GameConfig
from src.ui.controller import main as run_controller
import pygame
import sys


def main() -> None:
    try:
        # 1. Load configuration
        parser = ConfigParser(
            "/home/iait-mou/Desktop/Pac-Man/src/config.json"
        )
        config: GameConfig = parser.config_data

        # 2. Initialize Pygame
        pygame.init()

        # 3. Create the display using the configured dimensions
        screen = pygame.display.set_mode(
            (config.screen_width, config.screen_height)
        )
        pygame.display.set_caption("Pac-Man")

        # 4. Start the state controller
        run_controller(config, screen)

    except ConfigError as error:
        print(f"Configuration error: {error}")

    finally:
        pygame.quit()


if __name__ == "main":
    main()