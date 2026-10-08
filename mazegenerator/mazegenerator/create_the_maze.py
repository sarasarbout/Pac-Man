from mazegenerator import MazeGenerator
import pygame
from model.maze import Maze


def create_maze(rows, cell_size: int, screen):
    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8
    maze_color = (0, 0, 255)
    width = len(rows[0])
    height = len(rows)
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
