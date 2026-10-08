from model.cell import Pacgum
from model.position import Position
import pygame
from model.pacman import Pacman


def create_super_pacgums(width: int, height: int, cell_size: int, screen, pacman: Pacman, super_pacgums) -> None:
    eating_sound = pygame.mixer.Sound('/home/sasarbou/Desktop/pacman/pacman-art/sounds/eat_dot.wav')
    for pacgum in super_pacgums.copy():
        if pacgum.position == pacman.position:
            super_pacgums.remove(pacgum)
            pacman.score += 50
            eating_sound.play()
            break
    for pacgum in super_pacgums:
        x = pacgum.position.x * cell_size + cell_size // 2
        y = pacgum.position.y * cell_size + cell_size // 2
        pygame.draw.circle(
            screen,
            (255, 255, 255),
            (x, y),
            10
        )