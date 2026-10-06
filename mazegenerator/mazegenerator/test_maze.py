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


def create_the_maze(pacman: Pacman) -> None:
    generator = MazeGenerator()
    for row in generator.maze:
        print(row)
    pygame.init()
    cell_size = 80
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
    pacman_x = cell_size // 2 - pacman_size // 2
    pacman_y = cell_size // 2 - pacman_size // 2
    target_position = pacman.position
    screen = pygame.display.set_mode((width * cell_size + menu_width, height * cell_size))
    maze_color = (255, 0, 0)
    pacman_image = pygame.image.load('/home/sasarbou/Desktop/Pac-Man/pacman-art/pacman-down/3.png')
    pacman_image = pygame.transform.scale(pacman_image, (40, 40))
    moving = False
    pacgums = {
        Pacgum(Position(0, 0)),
        Pacgum(Position(width - 1, 0)),
        Pacgum(Position(0, height - 1)),
        Pacgum(Position(width - 1, height - 1))
    }
    # ====== Controlling pacman movements ======
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        keys = pygame.key.get_pressed()
        if not moving:
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                if maze.can_move(pacman.position, Direction.EAST):
                    target_position = Position(
                        pacman.position.x + 1,
                        pacman.position.y
                    )
                    moving = True
        if not moving:
            if keys[pygame.K_LEFT] or keys[pygame.K_l]:
                if maze.can_move(pacman.position, Direction.WEST):
                    target_position = Position(
                        pacman.position.x - 1,
                        pacman.position.y
                    )
        if not moving:
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                if maze.can_move(pacman.position, Direction.NORTH):
                    target_position = Position(
                        pacman.position.x,
                        pacman.position.y - 1
                    )
        if not moving:
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                if maze.can_move(pacman.position,   Direction.SOUTH):
                    target_position = Position(
                        pacman.position.x,
                        pacman.position.y + 1
                    )
        target_x = target_position.x * cell_size + cell_size // 2 - pacman_size // 2
        target_y = target_position.y * cell_size + cell_size // 2 - pacman_size // 2
        if pacman_x < target_x:
            pacman_x += 1
        elif pacman_x > target_x:
            pacman_x -= 1
        if pacman_y < target_y:
            pacman_y += 1
        elif pacman_y > target_y:
            pacman_y -= 1
        if pacman_x == target_x and pacman_y == target_y:
            pacman.position = target_position
            moving = False
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
        # ==== draw the pacgums ====
        eaten_pacgums = None
        for pacgum in pacgums:
            x = pacgum.position.x * cell_size + cell_size // 2
            y = pacgum.position.y * cell_size + cell_size // 2
            pygame.draw.circle(
                screen,
                (255, 255, 255),
                (x, y),
                10
            )
        for pacgum in pacgums:
            if pacgum.position == pacman.position:
                eaten_pacgums = pacgum
        if eaten_pacgums is not None:
            pacgums.remove(eaten_pacgums)
            pacman.score += 10
        pygame.display.flip()
    pygame.quit()


status = GameStatus.READY
mk = Pacman(Direction.EAST, Position(4, 1), status.READY)
create_the_maze(mk)
