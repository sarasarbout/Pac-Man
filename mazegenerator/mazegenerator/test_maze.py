from mazegenerator import MazeGenerator
import pygame
from sys import exit


def create_the_maze() -> None:
    generator = MazeGenerator()
    for row in generator.maze:
        print(row)
    pygame.init()
    screen = pygame.display.set_mode((800, 800))
    cell_size = 50
    rows = generator.maze
    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8
    width = len(rows)
    height = len(rows[0])
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        screen.fill((0, 0, 0))
        for j in range(width):
            for i in range(height):
                current_x = j * cell_size
                current_y = i * cell_size
                if rows[i][j] & NORTH:
                    pygame.draw.line(
                        screen,
                        (255, 255, 255),
                        (current_x, current_y),
                        (current_x + cell_size, current_y)
                    )
                if rows[i][j] & EAST:
                    pygame.draw.line(
                        screen,
                        (255, 255, 255),
                        (current_x + cell_size, current_y),
                        (current_x + cell_size, current_y + cell_size)
                    )
                if rows[i][j] & SOUTH:
                    pygame.draw.line(
                        screen,
                        (255, 255, 255),
                        (current_x, current_y + cell_size),
                        (current_x + cell_size, current_y + cell_size)
                    )
                if rows[i][j] & WEST:
                    pygame.draw.line(
                        screen,
                        (255, 255, 255),
                        (current_x, current_y),
                        (current_x, current_y + cell_size)
                    )
        pygame.display.flip()

<<<<<<< HEAD:mazegenerator/mazegenerator/test_maze.py
print("Entry:", generator.maze_entry)
print("Exit:", generator.maze_exit)
print("Shortest path:", generator.shortest_path)
=======
    pygame.quit()


create_the_maze()
>>>>>>> 983078d (visualize the maze):mazegenerator/test_maze.py
