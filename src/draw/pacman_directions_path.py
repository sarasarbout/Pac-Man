from pathlib import Path
from src.model.direction import Direction
from src.model.pacman import Pacman


def pacman_picture(pacman: Pacman) -> Path:
    if pacman.direction == Direction.NORTH:
        path = Path('/home/sasarbou/Desktop/pacman/pacman-art/pacman-up/1.png')
    elif pacman.direction == Direction.EAST:
        path = Path('/home/sasarbou/Desktop/pacman/pacman-art/pacman-right/1.png')
    elif pacman.direction == Direction.SOUTH:
        path = Path('/home/sasarbou/Desktop/pacman/pacman-art/pacman-down/1.png')
    elif pacman.direction == Direction.WEST:
        path = Path('/home/sasarbou/Desktop/pacman/pacman-art/pacman-left/1.png')
    return path
