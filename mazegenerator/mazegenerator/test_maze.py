from mazegenerator import MazeGenerator
import pygame
from sys import exit


def create_the_maze() -> None:
    generator = MazeGenerator()
    for row in generator.maze:
        print(row)
    pygame.init()
    cell_size = 40
    rows = generator.maze
    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8
    width = len(rows[0])
    height = len(rows)
    screen = pygame.display.set_mode((width * cell_size, height * cell_size))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        screen.fill((0, 0, 0))
        for row in range(height):
            for column in range(width):
                x = column * cell_size
                y = row * cell_size
                if rows[row][column] & NORTH:
                    pygame.draw.line(
                        screen,
                        (0, 0, 255),
                        (x, y),
                        (x + cell_size, y),
                        8
                    )
                if rows[row][column] & EAST:
                    pygame.draw.line(
                        screen,
                        (0, 0, 255),
                        (x + cell_size, y),
                        (x + cell_size, y + cell_size),
                        8
                    )
                if rows[row][column] & SOUTH:
                    pygame.draw.line(
                        screen,
                        (0, 0, 255),
                        (x, y + cell_size),
                        (x + cell_size, y + cell_size),
                        8
                    )
                if rows[row][column] & WEST:
                    pygame.draw.line(
                        screen,
                        (0, 0, 255),
                        (x, y),
                        (x, y + cell_size),
                        8
                    )
        pygame.display.flip()

    pygame.quit()


create_the_maze()