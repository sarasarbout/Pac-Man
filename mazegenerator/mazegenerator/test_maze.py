from mazegenerator import MazeGenerator
import pygame
from sys import exit
from model.maze import Maze
from model.position import Position
from model.direction import Direction
from model.pacman import Pacman
from model.game_state import GameStatus
from model.cell import Pacgum
from pathlib import Path
from create_super_pacgums import create_super_pacgums
from create_normal_pacgums import create_normal_pacgums
from create_the_maze import create_maze
from pacman_directions_path import pacman_picture
from src.config_parser import ConfigParser


def create_the_maze(pacman: Pacman) -> None:
    parser = ConfigParser("/home/sasarbou/Desktop/pacman/src/config.json")
    config = parser.config_data
    level1 = config.levels[0]
    w = level1["width"]
    h = level1["height"]
    generator = MazeGenerator(size=(w, h), perfect=False, seed=42)
    rows = generator.maze
    maze = Maze(rows)
    pygame.init()
    speed = (1.8) + (w + h - 38) * 0.1
    clock = pygame.time.Clock()
    start_sound = pygame.mixer.Sound('/home/sasarbou/Desktop/pacman/pacman-art/sounds/starting.wav')
    eating_sound = pygame.mixer.Sound('/home/sasarbou/Desktop/pacman/pacman-art/sounds/eat_dot.wav')
    game_started = False
    cell_size = 50
    maze = Maze(generator.maze)
    rows = generator.maze
    width = len(rows[0])
    height = len(rows)

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
    # print(config.score)
    # ====== Controlling pacman movements ======
    normal_pacgums = create_normal_pacgums(pacman, rows)
    super_pacgums = {
        Pacgum(Position(0, 0)),
        Pacgum(Position(width - 1, 0)),
        Pacgum(Position(0, height - 1)),
        Pacgum(Position(width - 1, height - 1))
    }
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        keys = pygame.key.get_pressed()
        # ===== Allow Pacman to move to his next direction only if he's in the center of the current cell =====
        at_cell_center = (
            pacman_x == pacman.position.x * cell_size + cell_size // 2 - pacman_size // 2
            and
            pacman_y == pacman.position.y * cell_size + cell_size // 2 - pacman_size // 2
        )
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
        if not game_started:
            start_sound.play(loops=-1)
        if game_started:
            start_sound.stop()
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
            path = Path('/home/sasarbou/Desktop/pacman/pacman-art/pacman-up/3.png')  # trying to fix this move
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
        pygame.display.update()
        clock.tick(60)
    pygame.quit()


status = GameStatus.READY
mk = Pacman(Direction.EAST, Position(0, 0), status.READY)
create_the_maze(mk)
