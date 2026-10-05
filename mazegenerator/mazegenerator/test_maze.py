from mazegenerator import MazeGenerator
import pygame
from sys import exit
import math
from model.maze import Maze
from model.position import Position
from model.direction import Direction


def create_the_maze() -> None:
    generator = MazeGenerator()
    for row in generator.maze:
        print(row)
    pygame.init()
    cell_size = 60
    maze = Maze(generator.maze)
    rows = generator.maze
    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8
    menu_width = 400
    width = len(rows[0])
    height = len(rows)
    pacman_position = Position(0, 0)
    pacman_x = pacman_position.x
    pacman_y = pacman_position.y
    screen = pygame.display.set_mode((width * cell_size + menu_width, height * cell_size))
    maze_color = (255, 0, 0)
    pacman = pygame.image.load('/home/sasarbou/Desktop/Pac-Man/pacman-art/pacman-down/3.png')
    pacman = pygame.transform.scale(pacman, (40, 40))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        keys = pygame.key.get_pressed()
        pacman_position = Position(
            int(pacman_x // cell_size),
            int(pacman_y // cell_size)
        )
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and maze.can_move(
            pacman_position, Direction.EAST
        ):
            pacman_x += 1
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and maze.can_move(
            pacman_position, (Direction.WEST)
        ):
            pacman_x -= 1
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and maze.can_move(
            pacman_position, (Direction.SOUTH)
        ):
            pacman_y += 1
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and maze.can_move(
            pacman_position, (Direction.NORTH)
        ):
            pacman_y -= 1
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
        screen.blit(pacman, (pacman_x, pacman_y))
        pygame.display.flip()

    pygame.quit()


create_the_maze()
