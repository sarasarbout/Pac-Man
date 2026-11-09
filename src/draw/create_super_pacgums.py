import pygame
from src.model.pacman import Pacman
from src.model.cell import Pacgum
from src.parser.config_parser import GameConfig


def create_super_pacgums(
    width: int,
    height: int,
    cell_size: int,
    screen: pygame.Surface,
    pacman: Pacman,
    super_pacgums: set[Pacgum],
    config: GameConfig,
) -> bool:

    eaten = False
    for pacgum in super_pacgums.copy():
        if pacgum.position == pacman.position:
            super_pacgums.remove(pacgum)
            eaten = True
            pacman.score += (config.points_per_super_pacgum)
            eaten = True
            break
    for pacgum in super_pacgums:
        x = pacgum.position.x * cell_size + cell_size // 2
        y = pacgum.position.y * cell_size + cell_size // 2
        pygame.draw.circle(
            screen,
            (255, 255, 255),
            (x, y),
            max(1, cell_size // 5)
        )
    return eaten
