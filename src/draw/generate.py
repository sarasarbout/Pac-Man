from pathlib import Path
import pygame
from typing import Optional

from src.model.game_state import GameStatus


from src.draw.create_ghosts import (
    GhostAnimation,
    chase_pacman,
    draw_ghosts,
    ghost_rect,
    move_ghost_randomly,
    respawn_ghosts,
    walk_away,
)
from src.draw.create_normal_pacgums import create_normal_pacgums
from src.draw.create_super_pacgums import create_super_pacgums
from src.draw.create_the_maze import create_maze
from src.draw.utils import (
    calculate_cell_size,
    calculate_maze_offset,
    move_only_center,
    pacman_picture,
    respawn_pacman,
    handle_events
)
from src.model.cell import Pacgum
from src.model.direction import Direction
from src.model.ghost import Ghost, GhostMode, GhostName
from src.model.maze import Maze
from src.model.pacman import Pacman
from src.model.position import Position
from mazegenerator import MazeGenerator
from src.parser.config_parser import GameConfig
from src.ui.cheat_menu import CheatState, cheat_menu
from src.ui.hud import get_hud_button_rects, hud_menu
from src.ui.pause_menu import pause_menu

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ASSETS_DIR = PROJECT_ROOT / "assets"
GHOST_MOVE_INTERVAL = 700
FRIGHTENED_DURATION = 6000
GHOST_DEAD_DURATION = 4000


def create_the_maze(
    pacman: Pacman,
    speed: float,
    config: GameConfig,
    screen: pygame.Surface,
    level: dict,
    level_index: int,
    cheats: CheatState,
) -> str:
    width = level["width"]
    height = level["height"]
    rows = MazeGenerator(
        size=(width, height), perfect=False, seed=level["seed"]
    ).maze
    maze = Maze(rows)

    pygame.init()
    start_time = pygame.time.get_ticks()
    """Game Sounds"""
    start_sound = pygame.mixer.Sound(ASSETS_DIR / "sounds" / "starting.wav")
    eating_sound = pygame.mixer.Sound(ASSETS_DIR / "sounds" / "eat_dot.wav")
    fail_sound = pygame.mixer.Sound(ASSETS_DIR / "sounds" / "fail.flac")
    got_eaten_sound = pygame.mixer.Sound(
        ASSETS_DIR / "sounds" / "got_eaten.mp3")

    cell_size = calculate_cell_size(screen, rows)
    """get the initial size of the window to check after if it change it"""
    maze_screen_size = screen.get_size()

    speed = cell_size * 0.1
    maze_surface = pygame.Surface(
        (width * cell_size, height * cell_size)
    )

    """check if pacman position is in 42 block"""
    x = width // 2
    y = height // 2
    while x >= 0:
        position = Position(x, y)
        if maze.get_cell(position).walls != 15:
            pacman.position = position
            break
        x -= 1

    start_position = Position(pacman.position.x, pacman.position.y)
    pacman_size = max(1, int(cell_size * 0.7))
    """calculate pixels pacman coordinates"""
    pacman_x: float = (
        pacman.position.x * cell_size
        + cell_size // 2
        - pacman_size // 2
    )
    pacman_y: float = (
        pacman.position.y * cell_size
        + cell_size // 2
        - pacman_size // 2
    )
    target_position = pacman.position
    next_direction = None
    game_started = False
    normal_pacgums = create_normal_pacgums(
        pacman, rows, level_index, config
    )
    super_pacgums = {
        Pacgum(Position(0, 0)),
        Pacgum(Position(width - 1, 0)),
        Pacgum(Position(0, height - 1)),
        Pacgum(Position(width - 1, height - 1)),
    }

    ghosts_data = [
        (
            Ghost(Position(1, 0), GhostName.BLINKY),
            ASSETS_DIR / "ghosts" / "blinky.png",
        ),
        (
            Ghost(Position(width - 1, 1), GhostName.CLYDE),
            ASSETS_DIR / "ghosts" / "clyde.png",
        ),
        (
            Ghost(Position(1, height - 1), GhostName.PINKY),
            ASSETS_DIR / "ghosts" / "pinky.png",
        ),
        (
            Ghost(Position(width - 2, height - 1), GhostName.INKY),
            ASSETS_DIR / "ghosts" / "inky.png",
        ),
    ]
    ghosts = [ghost for ghost, _ in ghosts_data]
    ghost_animations = {
        ghost: GhostAnimation.stationary(ghost.position, start_time)
        for ghost in ghosts
    }
    last_ghost_move = start_time
    frightened_until = 0

    pygame.display.set_caption("👾Pacman👾")
    start_sound.play()
    clock = pygame.time.Clock()
    pause_rect, cheats_rect = get_hud_button_rects(screen)

    while True:
        action = None
        next_direction, action, screen = handle_events(
            next_direction,
            screen,
            pause_rect,
            cheats_rect,
            config
        )
        """handle ghost position after we resize the screen, so he must has
        the same grid position"""
        if screen.get_size() != maze_screen_size:
            old_cell_size = cell_size
            old_center_x = (pacman.position.x + 0.5) * old_cell_size
            old_center_y = (pacman.position.y + 0.5) * old_cell_size
            progress_x = (
                pacman_x + pacman_size / 2 - old_center_x
            ) / old_cell_size
            progress_y = (
                pacman_y + pacman_size / 2 - old_center_y
            ) / old_cell_size

            """retaking the screen data fter we resize it (cell_size, speed,
            Hud menu)"""
            screen_width, screen_height = screen.get_size()
            config.screen_width = screen_width
            config.screen_height = screen_height
            maze_screen_size = (screen_width, screen_height)
            cell_size = calculate_cell_size(screen, rows)
            maze_surface = pygame.Surface(
                (width * cell_size, height * cell_size)
            )
            pacman_size = max(1, int(cell_size * 0.8))
            pacman_x = (
                (pacman.position.x + 0.5 + progress_x) * cell_size
                - pacman_size / 2
            )
            pacman_y = (
                (pacman.position.y + 0.5 + progress_y) * cell_size
                - pacman_size / 2
            )
            speed = cell_size * 0.1
            pause_rect, cheats_rect = get_hud_button_rects(screen)
        if action == "exit":
            return "exit"
        elif action == "pause_menu":
            pause_start = pygame.time.get_ticks()
            pause_action: str = pause_menu(config, screen)
            paused_duration = pygame.time.get_ticks() - pause_start

            start_time += paused_duration
            last_ghost_move += paused_duration
            if frightened_until:
                frightened_until += paused_duration
            for ghost in ghosts:
                if ghost.dead_until:
                    ghost.dead_until += paused_duration

            if pause_action in ("exit", "main_menu"):
                return pause_action
        elif action == "cheat_menu":
            cheat_start = pygame.time.get_ticks()
            cheat_action, cheats = cheat_menu(screen, cheats)
            paused_duration = pygame.time.get_ticks() - cheat_start

            start_time += paused_duration
            last_ghost_move += paused_duration
            if frightened_until:
                frightened_until += paused_duration
            for ghost in ghosts:
                if ghost.dead_until:
                    ghost.dead_until += paused_duration

            if cheat_action == "skip_level":
                return "level_complete"

            if cheat_action == "exit":
                return "exit"

        current_time = pygame.time.get_ticks()
        elapsed_seconds = (current_time - start_time) // 1000

        for ghost in ghosts:
            if (
                ghost.mode == GhostMode.DEAD
                and current_time >= ghost.dead_until
            ):
                ghost.mode = GhostMode.CHASE

        if (
            game_started
            and current_time - last_ghost_move >= GHOST_MOVE_INTERVAL
            and not cheats["Freeze Ghosts"]
        ):
            previous_positions = {
                ghost: ghost.position for ghost in ghosts
            }
            blinky, clyde, pinky, inky = ghosts

            for ghost in (blinky, inky):
                if ghost.mode == GhostMode.CHASE:
                    chase_pacman(ghost, pacman, maze, ghosts)
                elif ghost.mode == GhostMode.frightened:
                    walk_away(ghost, pacman, maze)

            for ghost in (pinky, clyde):
                if ghost.mode == GhostMode.CHASE:
                    move_ghost_randomly(ghost, maze)
                elif ghost.mode == GhostMode.frightened:
                    walk_away(ghost, pacman, maze)

            for ghost in ghosts:
                previous_position = previous_positions[ghost]
                if ghost.position != previous_position:
                    ghost_animations[ghost] = GhostAnimation.between(
                        previous_position,
                        ghost.position,
                        current_time,
                        GHOST_MOVE_INTERVAL,
                    )
            last_ghost_move = current_time

        pacman_rect = pygame.Rect(
            round(pacman_x),
            round(pacman_y),
            pacman_size,
            pacman_size,
        )
        collision_result: Optional[str] = None
        for ghost in ghosts:
            if ghost.mode == GhostMode.DEAD:
                continue
            if not pacman_rect.colliderect(
                ghost_rect(
                    ghost_animations[ghost],
                    cell_size,
                    current_time,
                )
            ):
                continue

            if ghost.mode == GhostMode.frightened:
                respawn_ghosts(ghost, width, height)
                ghost_animations[ghost] = GhostAnimation.stationary(
                    ghost.position,
                    current_time,
                )
                ghost.mode = GhostMode.DEAD
                ghost.dead_until = current_time + GHOST_DEAD_DURATION
                pacman.score += config.points_per_ghost
            elif (
                ghost.mode == GhostMode.CHASE
                and not cheats["Invincibility"]
            ):
                pacman.lives -= 1
                (pacman_x, pacman_y, target_position,
                 game_started, next_direction) = respawn_pacman(
                     pacman, pacman_x, pacman_y, cell_size, start_position,
                     game_started, pacman_size, target_position,
                     next_direction)

                # Reset Pac-Man position and direction.
                pacman.position = Position(4, 1)
                pacman.direction = Direction.NONE
                pacman.mode = GameStatus.READY

                got_eaten_sound.play()
                for other_ghost in ghosts:
                    respawn_ghosts(other_ghost, width, height)
                    ghost_animations[other_ghost] = (
                        GhostAnimation.stationary(
                            other_ghost.position,
                            current_time,
                        )
                    )

                if pacman.lives <= 0:
                    fail_sound.play()
                    print("GAME OVER reached!", pacman.lives)
                    collision_result = "game_over"
                break

        if collision_result is not None:
            return collision_result

        keys = pygame.key.get_pressed()
        (
            pacman.direction,
            game_started,
            next_direction,
        ) = move_only_center(
            pacman,
            game_started,
            pacman_x,
            pacman_y,
            cell_size,
            pacman_size,
            maze,
            keys,
            next_direction,
        )

        moving = maze.can_move(pacman.position, pacman.direction)
        if moving:
            if pacman.direction == Direction.EAST:
                target_position = Position(
                    pacman.position.x + 1,
                    pacman.position.y,
                )
            elif pacman.direction == Direction.WEST:
                target_position = Position(
                    pacman.position.x - 1,
                    pacman.position.y,
                )
            elif pacman.direction == Direction.NORTH:
                target_position = Position(
                    pacman.position.x,
                    pacman.position.y - 1,
                )
            elif pacman.direction == Direction.SOUTH:
                target_position = Position(
                    pacman.position.x,
                    pacman.position.y + 1,
                )

        target_x = (
            target_position.x * cell_size
            + cell_size // 2
            - pacman_size // 2
        )
        target_y = (
            target_position.y * cell_size
            + cell_size // 2
            - pacman_size // 2
        )
        current_speed = (
            speed * cheats["Speed Multiplier"]
            if cheats["Speed Boost"]
            else speed
        )
        if pacman_x < target_x:
            pacman_x = min(pacman_x + current_speed, target_x)
        elif pacman_x > target_x:
            pacman_x = max(pacman_x - current_speed, target_x)
        if pacman_y < target_y:
            pacman_y = min(pacman_y + current_speed, target_y)
        elif pacman_y > target_y:
            pacman_y = max(pacman_y - current_speed, target_y)
        if pacman_x == target_x and pacman_y == target_y:
            pacman.position = target_position

        image_path = (
            pacman_picture(pacman)
            if moving
            else ASSETS_DIR / "pacman-up" / "3.png"
        )
        pacman_image = pygame.image.load(image_path)
        pacman_image = pygame.transform.scale(
            pacman_image,
            (pacman_size, pacman_size),
        )

        screen.fill((0, 0, 0))
        maze_surface.fill((0, 0, 0))
        create_maze(rows, cell_size, maze_surface)
        maze_surface.blit(pacman_image, (pacman_x, pacman_y))

        super_pacgums_eaten = create_super_pacgums(
            width,
            height,
            cell_size,
            maze_surface,
            pacman,
            super_pacgums,
            config,
        )
        if super_pacgums_eaten:
            frightened_until = current_time + FRIGHTENED_DURATION
            for ghost in ghosts:
                if ghost.mode != GhostMode.DEAD:
                    ghost.mode = GhostMode.frightened
        if frightened_until > 0 and current_time >= frightened_until:
            for ghost in ghosts:
                if ghost.mode == GhostMode.frightened:
                    ghost.mode = GhostMode.CHASE
            frightened_until = 0

        eaten_pacgum = next(
            (
                pacgum
                for pacgum in normal_pacgums
                if pacgum.position == pacman.position
            ),
            None,
        )
        if eaten_pacgum is not None:
            eating_sound.play()
            normal_pacgums.remove(eaten_pacgum)
            pacman.score += config.points_per_pacgum
        for pacgum in normal_pacgums:
            gum_x = (
                pacgum.position.x * cell_size + cell_size // 2
            )
            gum_y = (
                pacgum.position.y * cell_size + cell_size // 2
            )
            pygame.draw.circle(
                maze_surface,
                (255, 255, 255),
                (gum_x, gum_y),
                max(1, cell_size // 10),
            )

        draw_ghosts(
            maze_surface,
            cell_size,
            ghosts_data,
            ghost_animations,
            current_time,
        )
        maze_offset = calculate_maze_offset(screen, maze_surface)
        screen.blit(maze_surface, maze_offset)

        if not normal_pacgums and not super_pacgums:
            return "level_complete"

        if elapsed_seconds >= level["time"]:
            fail_sound.play()
            print("Time Over!")
            return "game_over"

        pause_rect, cheats_rect = hud_menu(
            screen,
            pacman,
            elapsed_seconds,
            level_index,
            config,
            game_started,
        )
        pygame.display.update()
        clock.tick(60)
