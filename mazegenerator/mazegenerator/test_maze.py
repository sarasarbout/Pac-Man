from mazegenerator import MazeGenerator
import pygame
from sys import exit
import math
from model.maze import Maze
from model.position import Position
from model.direction import Direction
from model.pacman import Pacman
from model.game_state import GameStatus
from model.cell import Pacgum
from pathlib import Path


def create_the_maze(pacman: Pacman, speed: float) -> None:
    generator = MazeGenerator()
    for row in generator.maze:
        print(row)
    pygame.init()
    cell_size = 50
    maze = Maze(generator.maze)
    rows = generator.maze
    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8
    menu_width = 400
    width = len(rows[0])
    height = len(rows)
    pacman.position = Position(width // 2, height // 2)
    pacman_size = 40
    pacman_x = (pacman.position.x * cell_size
                + cell_size // 2
                - pacman_size // 2)
    pacman_y = (pacman.position.y * cell_size
                + cell_size // 2
                - pacman_size // 2)
    target_position = pacman.position
    screen = pygame.display.set_mode((width * cell_size + menu_width, height * cell_size))
    maze_color = (255, 0, 0)
    super_pacgums = {
        Pacgum(Position(0, 0)),
        Pacgum(Position(width - 1, 0)),
        Pacgum(Position(0, height - 1)),
        Pacgum(Position(width - 1, height - 1))
    }
    # ====== Controlling pacman movements ======
    normal_pacgums = set()
    for row in range(height):
        for column in range(width):
            if rows[row][column] == 15:
                continue
            position = Position(column, row)
            if pacman.position == position:
                continue
            has_super_pacgum = False
            for big in super_pacgums:
                if big.position == position:
                    has_super_pacgum = True
                    break
            if has_super_pacgum:
                continue
            normal_pacgums.add(Pacgum(position))
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
                if maze.can_move(pacman.position, Direction.EAST):
                    pacman.direction = Direction.EAST
            elif keys[pygame.K_LEFT] or keys[pygame.K_l]:
                if maze.can_move(pacman.position, Direction.WEST):
                    pacman.direction = Direction.WEST
            elif keys[pygame.K_UP] or keys[pygame.K_w]:
                if maze.can_move(pacman.position, Direction.NORTH):
                    pacman.direction = Direction.NORTH
            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                if maze.can_move(pacman.position, Direction.SOUTH):
                    pacman.direction = Direction.SOUTH
        if maze.can_move(pacman.position, pacman.direction):
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
        if pacman.direction == Direction.NORTH:
            path = Path('/home/sasarbou/Desktop/Pac-Man/pacman-art/pacman-up/1.png')
        elif pacman.direction == Direction.EAST:
            path = Path('/home/sasarbou/Desktop/Pac-Man/pacman-art/pacman-right/1.png')
        elif pacman.direction == Direction.SOUTH:
            path = Path('/home/sasarbou/Desktop/Pac-Man/pacman-art/pacman-down/1.png')
        elif pacman.direction == Direction.WEST:
            path = Path('/home/sasarbou/Desktop/Pac-Man/pacman-art/pacman-left/1.png')
        pacman_image = pygame.image.load(path)
        pacman_image = pygame.transform.scale(pacman_image, (40, 40))

        # ===== adjusting maze colors =====
        if event.type == pygame.MOUSEBUTTONDOWN:
            distance1 = math.dist((width * cell_size + 75, 100), event.pos)
            if distance1 <= 25:
                maze_color = (255, 0, 0)
            distance2 = math.dist((width * cell_size + 140, 100), event.pos)
            if distance2 <= 25:
                maze_color = (0, 255, 0)
            distance3 = math.dist((width * cell_size + 210, 100), event.pos)
            if distance3 <= 25:
                maze_color = (0, 0, 255)
            distance4 = math.dist((width * cell_size + 280, 100), event.pos)
            if distance4 <= 25:
                maze_color = (255, 255, 0)
            distance4 = math.dist((width * cell_size + 350, 100), event.pos)
            if distance4 <= 25:
                maze_color = (255, 255, 255)
        screen.fill((0, 0, 0))
        pygame.draw.rect(
            screen,
            (30, 30, 30),
            (width * cell_size, 0, menu_width, height * cell_size)
        )
        # ===== Drawing the cells ======
        for row in range(height):
            for column in range(width):
                x = column * cell_size
                y = row * cell_size
                if rows[row][column] == 15:
                    pygame.draw.rect(
                        screen,
                        (255, 255, 255),
                        (x, y, cell_size, cell_size)
                    )
                if rows[row][column] & NORTH:
                    pygame.draw.line(
                        screen,
                        (maze_color),
                        (x, y),
                        (x + cell_size, y),
                        8
                    )
                if rows[row][column] & EAST:
                    pygame.draw.line(
                        screen,
                        (maze_color),
                        (x + cell_size, y),
                        (x + cell_size, y + cell_size),
                        8
                    )
                if rows[row][column] & SOUTH:
                    pygame.draw.line(
                        screen,
                        (maze_color),
                        (x, y + cell_size),
                        (x + cell_size, y + cell_size),
                        8
                    )
                if rows[row][column] & WEST:
                    pygame.draw.line(
                        screen,
                        (maze_color),
                        (x, y),
                        (x, y + cell_size),
                        8
                    )
        # ===== draw color circle =====
        pygame.draw.circle(
            screen,
            (255, 0, 0),
            (width * cell_size + 75, 100),
            25
        )
        pygame.draw.circle(
            screen,
            (0, 255, 0),
            (width * cell_size + 140, 100),
            25
        )
        pygame.draw.circle(
            screen,
            (0, 0, 255),
            (width * cell_size + 210, 100),
            25
        )
        pygame.draw.circle(
            screen,
            (255, 255, 0),
            (width * cell_size + 280, 100),
            25
        )
        pygame.draw.circle(
            screen,
            (255, 255, 255),
            (width * cell_size + 350, 100),
            25
        )
        screen.blit(pacman_image, (pacman_x, pacman_y))
        # ==== draw the super_pacgums ====
        eaten_pacgums = None
        for pacgum in super_pacgums:
            x = pacgum.position.x * cell_size + cell_size // 2
            y = pacgum.position.y * cell_size + cell_size // 2
            pygame.draw.circle(
                screen,
                (255, 255, 255),
                (x, y),
                10
            )
        for pacgum in super_pacgums:
            if pacgum.position == pacman.position:
                eaten_pacgums = pacgum
        if eaten_pacgums is not None:
            super_pacgums.remove(eaten_pacgums)
            pacman.score += 50
        # ===== draw the normal_pacgums =====
        eaten_small_pacgums = None
        for normal in normal_pacgums:
            if normal.position == pacman.position:
                eaten_small_pacgums = normal
                break
        if eaten_small_pacgums is not None:
            normal_pacgums.remove(eaten_small_pacgums)
            pacman.score += 10
        for normal in normal_pacgums:
            x = normal.position.x * cell_size + cell_size // 2
            y = normal.position.y * cell_size + cell_size // 2

            pygame.draw.circle(screen, (255, 255, 255), (x, y), 5)
        pygame.display.flip()
    pygame.quit()


status = GameStatus.READY
mk = Pacman(Direction.EAST, Position(4, 1), status.READY)
create_the_maze(mk, 0.3)
