from src.mazegenerator.mazegenerator import MazeGenerator
import pygame
from src.model.maze import Maze
from src.model.position import Position
from src.model.direction import Direction
from src.model.pacman import Pacman
from src.model.cell import Pacgum
from src.ui.hud import hud_menu
from pathlib import Path
from src.draw.create_super_pacgums import create_super_pacgums
from src.draw.create_normal_pacgums import create_normal_pacgums
from src.draw.create_the_maze import create_maze
from src.draw.pacman_utils import pacman_picture, respawn_pacman
from src.parser.config_parser import GameConfig
from src.model.ghost import Ghost, GhostMode, GhostName
from src.draw.create_ghosts import (
    draw_ghosts, chase_pacman, move_ghost_randomly, walk_away, respawn_ghosts)

# generate.py is in project_root/src/draw/
PROJECT_ROOT = Path(__file__).resolve().parents[2]
ASSETS_DIR = PROJECT_ROOT / "assets"


def create_the_maze(
    pacman: Pacman,
    speed: float,
    config: GameConfig,
    screen: pygame.Surface,
    level: dict,
    level_index: int,
) -> str:
    width = level["width"]
    height = level["height"]
    generator = MazeGenerator(
        size=(width, height),
        perfect=False,
        seed=42,
    )

    pygame.init()
    rows = generator.maze
    maze = Maze(rows)
    speed = (4) + (width + height - 38) * 0.1
    clock = pygame.time.Clock()
    last_ghost_move = pygame.time.get_ticks()
    start_time = pygame.time.get_ticks()

    ghost_move = 300
    start_sound = pygame.mixer.Sound(ASSETS_DIR / "sounds"/"starting.wav")
    eating_sound = pygame.mixer.Sound(ASSETS_DIR / "sounds"/"eat_dot.wav")
    fail_sound = pygame.mixer.Sound(ASSETS_DIR / "sounds" / "fail.flac")
    game_started = False
    cell_size = 50
    maze = Maze(generator.maze)
    rows = generator.maze
    # ==== fix the problem of center position with collision with the 42 block =====
    center_x = width // 2
    center_y = height // 2
    x = center_x
    y = center_y
    frightened_until = 0
    while x >= 0:
        position = Position(x, y)
        cell = maze.get_cell(position)
        if cell.walls != 15:
            pacman.position = position
            break
        else:
            x -= 1

    start_position = Position(pacman.position.x, pacman.position.y)
    pacman_size = 40
    pacman_x = (pacman.position.x * cell_size
                + cell_size // 2
                - pacman_size // 2)
    pacman_y = (pacman.position.y * cell_size
                + cell_size // 2
                - pacman_size // 2)
    target_position = pacman.position
    next_direction = None
    pygame.display.set_caption("👾Pacman👾")
    # ====== Create normal pacgums ======
    normal_pacgums = create_normal_pacgums(pacman, rows)

    super_pacgums = {
        Pacgum(Position(0, 0)),
        Pacgum(Position(width - 1, 0)),
        Pacgum(Position(0, height - 1)),
        Pacgum(Position(width - 1, height - 1))
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
            Ghost(Position(width - 1, height - 1), GhostName.INKY),
            ASSETS_DIR / "ghosts" / "inky.png",
        ),
    ]

    game_started = False
    if not game_started:
        start_sound.play()
    else:
        start_sound.stop()
    frightened_until = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "menu"
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    next_direction = Direction.EAST
                elif event.key in (pygame.K_LEFT, pygame.K_l):
                    next_direction = Direction.WEST
                elif event.key in (pygame.K_UP, pygame.K_w):
                    next_direction = Direction.NORTH
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    next_direction = Direction.SOUTH
                elif event.key == pygame.K_SPACE:
                    return "pause_menu"

        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()
        # working on chasing logic until a super pacgum
        if game_started and current_time - last_ghost_move >= ghost_move:
            ghost1, image = ghosts_data[3]
            ghost2, image = ghosts_data[0]
            ghost3, image = ghosts_data[1]
            ghost4, image = ghosts_data[2]
            algo_ghosts = [ghost1, ghost2]
            random_ghosts = [ghost3, ghost4]
            for ghost in algo_ghosts:
                if ghost.mode == GhostMode.CHASE:
                    chase_pacman(ghost, pacman, maze)
        # handle random ghosts
            for ghost in random_ghosts:
                if ghost.mode == GhostMode.CHASE:
                    move_ghost_randomly(ghost, maze)
            
            for ghost, image_path in ghosts_data:
                if ghost.position == pacman.position:
                    if ghost.mode == GhostMode.frightened:
                        # Return the eaten ghost to its starting position
                        speed += 0.3
                        respawn_ghosts(ghost, width, height)
                        pacman.score += config.points_per_ghost
                    else:
                        pacman.lives -= 1
                        print("Lives remaining:", pacman.lives)

                        (
                            pacman_x,
                            pacman_y,
                            target_position,
                            game_started,
                            next_direction,
                        ) = respawn_pacman(
                            pacman,
                            pacman_x,
                            pacman_y,
                            cell_size,
                            start_position,
                            game_started,
                            pacman_size,
                            target_position,
                            next_direction,
                        )

                        if pacman.lives <= 0:
                            fail_sound.play()
                            print("GAME OVER reached!", pacman.lives)
                            return "game_over"

                        break

                elif ghost.mode == GhostMode.frightened:
                    walk_away(ghost, pacman, maze)

            last_ghost_move = current_time


    # ===== Allow Pacman to move to his next direction only if he's in the center of the current cell =====
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
            elif keys[pygame.K_LEFT] or keys[pygame.K_l]:
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
        moving = False
        if maze.can_move(pacman.position, pacman.direction):
            moving = True
            if pacman.direction == Direction.EAST:
                target_position = Position(
                    pacman.position.x + 1,
                    pacman.position.y
                )

            elif pacman.direction == Direction.WEST:
                target_position = Position(
                    pacman.position.x - 1,
                    pacman.position.y
                )

            elif pacman.direction == Direction.NORTH:
                target_position = Position(
                    pacman.position.x,
                    pacman.position.y - 1
                )

            elif pacman.direction == Direction.SOUTH:
                target_position = Position(
                    pacman.position.x,
                    pacman.position.y + 1
                )
        target_x = target_position.x * cell_size + cell_size // 2 - pacman_size // 2
        target_y = target_position.y * cell_size + cell_size // 2 - pacman_size // 2

        if pacman_x < target_x:
            pacman_x = min(pacman_x + speed, target_x)
        elif pacman_x > target_x:
            pacman_x = max(pacman_x - speed, target_x)
        if pacman_y < target_y:
            pacman_y = min(pacman_y + speed, target_y)
        elif pacman_y > target_y:
            pacman_y = max(pacman_y - speed, target_y)
        if pacman_x == target_x and pacman_y == target_y:
            pacman.position = target_position

        # ===== Changing Pacman picture depending on his Direction ====
        if moving is False:
            path = Path(ASSETS_DIR / "pacman-up" / "3.png")
        else:
            path = pacman_picture(pacman)
        pacman_image = pygame.image.load(path)
        pacman_image = pygame.transform.scale(pacman_image, (40, 40))

        screen.fill((0, 0, 0))
        pygame.draw.rect(
            screen,
            (0, 0, 0),
            (0, 0, config.screen_width, config.screen_height)
        )
        create_maze(rows, cell_size, screen)
        screen.blit(pacman_image, (pacman_x, pacman_y))
        # ==== draw the super_pacgums ====
        super_pacgums_eaten = create_super_pacgums(width, height, cell_size, screen, pacman, super_pacgums, config)
        if super_pacgums_eaten:
            frightened_until = pygame.time.get_ticks() + 6000
            for ghost, image_path in ghosts_data:
                ghost.mode = GhostMode.frightened
        if frightened_until > 0 and pygame.time.get_ticks() >= frightened_until:
            for ghost, image_path in ghosts_data:
                ghost.mode = GhostMode.CHASE
            frightened_until = 0
        # ===== draw the normal_pacgums =====
        eaten_small_pacgums = None
        for normal in normal_pacgums:
            if normal.position == pacman.position:
                eaten_small_pacgums = normal
                break
        if eaten_small_pacgums is not None:
            eating_sound.play()
            normal_pacgums.remove(eaten_small_pacgums)
            pacman.score += (config.points_per_pacgum)
        for normal in normal_pacgums:
            x = normal.position.x * cell_size + cell_size // 2
            y = normal.position.y * cell_size + cell_size // 2
            pygame.draw.circle(screen, (255, 255, 255), (x, y), 5)
        if not normal_pacgums and not super_pacgums:
            return "level_complete"

        # ===== draw the ghosts =====
        draw_ghosts(rows, width, height, screen, cell_size, ghosts_data)

        elapsed_seconds = (pygame.time.get_ticks() - start_time) // 1000
        hud_menu(screen, pacman, elapsed_seconds, level_index, config)
        pygame.display.update()
        clock.tick(60)
    pygame.quit()
