from pathlib import Path
from src.model.direction import Direction
from src.model.pacman import Pacman
from src.model.position import Position
from src.model.maze import Maze
from src.parser.config_parser import GameConfig
from src.ui.hud import HUD_HEIGHT
from typing import Optional
import pygame

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ASSETS_DIR = PROJECT_ROOT / "assets"
MAZE_MARGIN = 16


def calculate_cell_size(
    screen: pygame.Surface,
    rows: list[list[int]],
    hud_height: int = HUD_HEIGHT,
    margin: int = MAZE_MARGIN,
) -> int:
    screen_width, screen_height = screen.get_size()

    maze_rows = int(len(rows))
    maze_cols = int(len(rows[0]))

    available_width = max(1, screen_width)
    available_height = max(1, screen_height - hud_height)

    return int(
        max(
            1,
            min(
                available_width // maze_cols,
                available_height // maze_rows,
            ),
        )
    )


def calculate_maze_offset(
    screen: pygame.Surface,
    maze_surface: pygame.Surface,
    hud_height: int = HUD_HEIGHT,
    margin: int = MAZE_MARGIN,
) -> tuple[int, int]:
    screen_width, screen_height = screen.get_size()
    maze_width, maze_height = maze_surface.get_size()
    available_width = max(0, screen_width - 2 * margin)
    available_height = max(0, screen_height - hud_height - 2 * margin)

    return (
        margin + (available_width - maze_width) // 2,
        margin + (available_height - maze_height) // 2,
    )


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
    pacman: Pacman,
    pacman_x: float,
    pacman_y: float,
    cell_size: int,
    start_position: Position,
    game_started: bool,
    pacman_size: int,
    target_position: Position,
    next_direction: Optional[Direction],
) -> tuple[float, float, Position, bool, Optional[Direction]]:
    print("Before respawn:", pacman.position)

    pacman.position = Position(start_position.x, start_position.y)

    print("After respawn:", pacman.position)

    pacman_x = start_position.x * cell_size + cell_size // 2 - pacman_size // 2
    pacman_y = start_position.y * cell_size + cell_size // 2 - pacman_size // 2
    target_position = Position(start_position.x, start_position.y)

    game_started = False
    next_direction = None

    return pacman_x, pacman_y, target_position, game_started, next_direction


def move_only_center(
    pacman: Pacman,
    game_started: bool,
    pacman_x: float,
    pacman_y: float,
    cell_size: int,
    pacman_size: int,
    maze: Maze,
    keys: pygame.key.ScancodeWrapper,
    next_direction: Optional[Direction],
) -> tuple[Direction, bool, Optional[Direction]]:
    at_cell_center = (
        pacman_x ==
        pacman.position.x * cell_size + cell_size // 2 - pacman_size // 2
        and
        pacman_y ==
        pacman.position.y * cell_size + cell_size // 2 - pacman_size // 2
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


def handle_events(
    next_direction: Optional[Direction],
    screen: pygame.Surface,
    pause_rect: pygame.Rect,
    cheats_rect: pygame.Rect,
    config: GameConfig,
) -> tuple[Optional[Direction], Optional[str], pygame.Surface]:

    action = None

    for event in pygame.event.get():

        if event.type in (
            pygame.VIDEORESIZE,
            pygame.WINDOWRESIZED,
            pygame.WINDOWSIZECHANGED,
        ):
            screen = pygame.display.get_surface()
            if screen is None:
                raise RuntimeError("The display surface is unavailable.")
            config.screen_width, config.screen_height = screen.get_size()

        elif event.type == pygame.QUIT:
            action = "exit"

        elif event.type == pygame.KEYDOWN:

            if event.key in (pygame.K_ESCAPE, pygame.K_SPACE):
                action = "pause_menu"

            elif event.key == pygame.K_F1:
                action = "cheat_menu"

            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                next_direction = Direction.EAST

            elif event.key in (pygame.K_LEFT, pygame.K_a):
                next_direction = Direction.WEST

            elif event.key in (pygame.K_UP, pygame.K_w):
                next_direction = Direction.NORTH

            elif event.key in (pygame.K_DOWN, pygame.K_s):
                next_direction = Direction.SOUTH

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

            if pause_rect.collidepoint(event.pos):
                action = "pause_menu"

            elif cheats_rect.collidepoint(event.pos):
                action = "cheat_menu"

    return next_direction, action, screen
