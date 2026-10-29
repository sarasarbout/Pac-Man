from pathlib import Path
from src.model.direction import Direction
from src.model.pacman import Pacman
from src.model.position import Position
import pygame

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



def move_only_center(
    pacman,
    game_started,
    pacman_x,
    pacman_y,
    cell_size,
    pacman_size,
    maze,
    keys,
    next_direction,
):
    at_cell_center = (
        pacman_x == pacman.position.x * cell_size + cell_size // 2 - pacman_size // 2
        and
        pacman_y == pacman.position.y * cell_size + cell_size // 2 - pacman_size // 2
    )

    if at_cell_center:
        if next_direction is not None:
            if maze.can_move(pacman.position, next_direction):
                pacman.direction = next_direction
                next_direction = None
                game_started = True

        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            game_started = True
            if maze.can_move(pacman.position, Direction.EAST):
                pacman.direction = Direction.EAST

        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            game_started = True
            if maze.can_move(pacman.position, Direction.WEST):
                pacman.direction = Direction.WEST

        elif keys[pygame.K_UP] or keys[pygame.K_w]:
            game_started = True
            if maze.can_move(pacman.position, Direction.NORTH):
                pacman.direction = Direction.NORTH

        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            game_started = True
            if maze.can_move(pacman.position, Direction.SOUTH):
                pacman.direction = Direction.SOUTH

    return pacman.direction, game_started, next_direction

def handle_events(next_direction):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return "exit"
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "menu"
            if event.key in (pygame.K_RIGHT, pygame.K_d):
                next_direction = Direction.EAST
            elif event.key in (pygame.K_LEFT, pygame.K_l):
                next_direction = Direction.WEST
            elif event.key in (pygame.K_UP, pygame.K_w):
                next_direction = Direction.NORTH
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                next_direction = Direction.SOUTH
            elif event.key == pygame.K_SPACE:
                return "pause_menu"
    return next_direction