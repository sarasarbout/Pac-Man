import pygame


def create_maze(
    rows: list[list[int]], cell_size: int, screen: pygame.Surface
) -> None:
    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8
    maze_color = (0, 0, 255)
    wall_width = max(1, cell_size // 10)
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
                    wall_width
                )
            if rows[row][column] & EAST:
                pygame.draw.line(
                    screen,
                    (maze_color),
                    (x + cell_size, y),
                    (x + cell_size, y + cell_size),
                    wall_width
                )
            if rows[row][column] & SOUTH:
                pygame.draw.line(
                    screen,
                    (maze_color),
                    (x, y + cell_size),
                    (x + cell_size, y + cell_size),
                    wall_width
                )
            if rows[row][column] & WEST:
                pygame.draw.line(
                    screen,
                    (maze_color),
                    (x, y),
                    (x, y + cell_size),
                    wall_width
                )
