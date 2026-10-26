from pathlib import Path
from src.model.direction import Direction
from src.model.pacman import Pacman
from src.model.position import Position

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ASSETS_DIR = PROJECT_ROOT / "assets"


def pacman_picture(pacman: Pacman) -> Path:
    if pacman.direction == Direction.NORTH:
        path = Path(ASSETS_DIR / "pacman-up" / "1.png")

    elif pacman.direction == Direction.EAST:
        path = Path(ASSETS_DIR / "pacman-right" / "1.png")

    elif pacman.direction == Direction.SOUTH:
        path = Path(ASSETS_DIR / "pacman-down" / "1.png")

    elif pacman.direction == Direction.WEST:
        path = Path(ASSETS_DIR / "pacman-left" / "1.png")
    return path


def respawn_pacman(
    pacman, pacman_x, pacman_y, cell_size,
    start_position, game_started, pacman_size,
    target_position, next_direction
):
    pacman.position = Position(start_position.x, start_position.y)

    pacman_x = start_position.x * cell_size + cell_size // 2 - pacman_size // 2
    pacman_y = start_position.y * cell_size + cell_size // 2 - pacman_size // 2
    target_position = Position(start_position.x, start_position.y)

    pacman.direction = Direction.EAST
    game_started = False
    next_direction = None

    return pacman_x, pacman_y, target_position, game_started, next_direction