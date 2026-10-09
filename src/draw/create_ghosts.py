import pygame
from model.direction import Direction
from model.position import Position


def draw_ghosts(rows, width, height, screen, cell_size, ghosts_data) -> None:
    ghost_size = 30
    for ghost, image_path in ghosts_data:
        image = pygame.image.load(image_path)
        image = pygame.transform.scale(image, (ghost_size, ghost_size))
        x = ghost.position.x * cell_size + (cell_size - ghost_size) // 2
        y = ghost.position.y * cell_size + (cell_size - ghost_size) // 2

        screen.blit(image, (x, y))


def chase_pacman(ghost, pacman, maze) -> None:
    possible_moves = [
        direction
        for direction in (
            Direction.NORTH,
            Direction.EAST,
            Direction.SOUTH,
            Direction.WEST
        )
        if maze.can_move(ghost.position, Direction)
    ]
    if not possible_moves:
        return
    best_distance = float("inf")
    best_moves = []
    for direction in possible_moves:
        if direction == Direction.NORTH:
            next_position = Position(ghost.position.x, ghost.position.y - 1)
        elif direction == Direction.EAST:
            next_position = Position(ghost.position.x + 1, ghost.position.y)
        elif direction == Direction.SOUTH:
            next_position = Position(ghost.position.x, ghost.position.y + 1)
        elif direction == Direction.WEST:
            next_position = Position(ghost.position.x - 1, ghost.position.y)
        