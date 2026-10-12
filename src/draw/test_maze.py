from src.mazegenerator.mazegenerator import MazeGenerator
import pygame
from sys import exit
from src.model.maze import Maze
from src.model.position import Position
from src.model.direction import Direction
from src.model.pacman import Pacman
from src.model.game_state import GameStatus
from src.model.cell import Pacgum
from pathlib import Path
from create_super_pacgums import create_super_pacgums
from create_normal_pacgums import create_normal_pacgums
from create_the_maze import create_maze
from pacman_directions_path import pacman_picture
from src.parser.config_parser import ConfigParser
from src.model.ghost import Ghost
from create_ghosts import draw_ghosts, chase_pacman


def create_the_maze(pacman: Pacman) -> None:
    parser = ConfigParser("/Users/sarasarbout/Desktop/Pac-Man/src/config.json")
    config = parser.config_data
    level1 = config.levels[0]
    width = level1["width"]
    height = level1["height"]
    generator = MazeGenerator(size=(width, height), perfect=False, seed=42)
    rows = generator.maze
    maze = Maze(rows)
    pygame.init()
    speed = (2.1) + (width + height - 38) * 0.1
    clock = pygame.time.Clock()
    last_ghost_move = pygame.time.get_ticks()
    ghost_move = 250
    start_sound = pygame.mixer.Sound('/Users/sarasarbout/Desktop/Pac-Man/assets/sounds/starting.wav')
    eating_sound = pygame.mixer.Sound('/Users/sarasarbout/Desktop/Pac-Man/assets/sounds/eat_dot.wav')
    game_started = False
    cell_size = 50
    maze = Maze(generator.maze)
    rows = generator.maze

    # ==== fix the problem of center position with collision with the 42 block =====
    center_x = width // 2
    center_y = height // 2
    x = center_x
    y = center_y
    while x >= 0:
        position = Position(x, y)
        cell = maze.get_cell(position)
        if cell.walls != 15:
            pacman.position = position
            break
        else:
            x -= 1
    pacman_size = 40
    pacman_x = (pacman.position.x * cell_size
                + cell_size // 2
                - pacman_size // 2)
    pacman_y = (pacman.position.y * cell_size
                + cell_size // 2
                - pacman_size // 2)
    target_position = pacman.position
    screen = pygame.display.set_mode((width * cell_size, height * cell_size))
    pygame.display.set_caption("👾Pacman👾")
    # print(config.score)
    # ====== Controlling pacman movements ======
    normal_pacgums = create_normal_pacgums(pacman, rows)
    super_pacgums = {
        Pacgum(Position(0, 0)),
        Pacgum(Position(width - 1, 0)),
        Pacgum(Position(0, height - 1)),
        Pacgum(Position(width - 1, height - 1))
    }
    ghosts_data = [
        (Ghost(Position(1, 0)), Path('/Users/sarasarbout/Desktop/Pac-Man/assets/ghosts/inky.png')),
        (Ghost(Position(width - 1, 1)), Path('/Users/sarasarbout/Desktop/Pac-Man/assets/ghosts/clyde.png')),
        (Ghost(Position(1, height - 1)), Path('/Users/sarasarbout/Desktop/Pac-Man/assets/ghosts/pinky.png')),
        (Ghost(Position(width - 1, height - 1)), Path('/Users/sarasarbout/Desktop/Pac-Man/assets/ghosts/blinky.png'))        
    ]
    game_started = False
    if not game_started:
        start_sound.play()
    else:
        start_sound.stop()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        keys = pygame.key.get_pressed()
        # ===== Allow Pacman to move to his next direction only if he's in the center of the current cell =====
        current_time = pygame.time.get_ticks()
        if game_started and current_time - last_ghost_move >= ghost_move:
            ghost1, image = ghosts_data[3]
            ghost2, image = ghosts_data[0]
            chase_pacman(ghost1, pacman, maze)
            chase_pacman(ghost2, pacman, maze)
            last_ghost_move = current_time
            if pacman.position == ghost1.position and pacman.lives > 0:
                pacman.lives -= 1
            if pacman.position == ghost2.position and pacman.lives > 0:
                pacman.lives -= 1
        at_cell_center = (
            pacman_x == pacman.position.x * cell_size + cell_size // 2 - pacman_size // 2
            and
            pacman_y == pacman.position.y * cell_size + cell_size // 2 - pacman_size // 2
        )
        print(pacman.lives)
        if at_cell_center:
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
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
            path = Path('/Users/sarasarbout/Desktop/Pac-Man/assets/pacman-up/3.png')  # trying to fix this move
        else:
            path = pacman_picture(pacman)
        pacman_image = pygame.image.load(path)
        pacman_image = pygame.transform.scale(pacman_image, (40, 40))

        screen.fill((0, 0, 0))
        create_maze(rows, cell_size, screen)
        screen.blit(pacman_image, (pacman_x, pacman_y))
        # ==== draw the super_pacgums ====
        create_super_pacgums(width, height, cell_size, screen, pacman, super_pacgums, config)
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

        # ===== draw the ghosts =====
        draw_ghosts(rows, width, height, screen, cell_size, ghosts_data)

        pygame.display.update()
        clock.tick(60)
    pygame.quit()


status = GameStatus.READY
mk = Pacman(Direction.EAST, Position(0, 0), status.READY)
create_the_maze(mk)
