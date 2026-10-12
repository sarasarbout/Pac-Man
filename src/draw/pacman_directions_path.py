from pathlib import Path
from src.model.direction import Direction
from src.model.pacman import Pacman


def pacman_picture(pacman: Pacman) -> Path:
    if pacman.direction == Direction.NORTH:
        path = Path('/Users/sarasarbout/Desktop/Pac-Man/assets/pacman-up/1.png')
    elif pacman.direction == Direction.EAST:
        path = Path('/Users/sarasarbout/Desktop/Pac-Man/assets/pacman-right/1.png')
    elif pacman.direction == Direction.SOUTH:
        path = Path('/Users/sarasarbout/Desktop/Pac-Man/assets/pacman-down/1.png')
    elif pacman.direction == Direction.WEST:
        path = Path('/Users/sarasarbout/Desktop/Pac-Man/assets/pacman-left/1.png')
    return path
