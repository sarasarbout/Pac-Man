import argparse
from pathlib import Path
import sys

from src.parser.config_parser import ConfigParser, ConfigError, GameConfig
from src.ui.controller import main as run_controller
import pygame


def main() -> None:
    argument_parser = argparse.ArgumentParser(
        description="Run Pacman Ghosts with a JSON config file."
    )
    frozen = getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS")
    if frozen:
        bundled_config = Path(getattr(sys, "_MEIPASS")) / "config.json"
        argument_parser.add_argument(
            "config",
            nargs="?",
            default=str(bundled_config),
            help="Path to the JSON configuration file",
        )
    else:
        argument_parser.add_argument(
            "config",
            help="Path to the JSON configuration file",
        )
    args = argument_parser.parse_args()

    try:
        parser = ConfigParser(args.config)
        config: GameConfig = parser.config_data

        pygame.init()
        screen = pygame.display.set_mode(
            (config.screen_width, config.screen_height),
            pygame.RESIZABLE,
        )
        pygame.display.set_caption("Pac-Man")
        run_controller(config, screen)

    except ConfigError as error:
        print(f"Configuration error: {error}")
    finally:
        pygame.quit()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGame stopped by the user.")
