from mazegenerator import MazeGenerator
import pygame
from sys import exit
import math


def create_the_maze() -> None:
    generator = MazeGenerator()
    for row in generator.maze:
        print(row)
    pygame.init()
    cell_size = 60
    rows = generator.maze
    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8
    menu_width = 400
    width = len(rows[0])
    height = len(rows)
    screen = pygame.display.set_mode((width * cell_size + menu_width, height * cell_size))
    maze_color = (255, 0, 0)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
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
        pygame.display.flip()

    pygame.quit()


create_the_maze()