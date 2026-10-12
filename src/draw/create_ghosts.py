import pygame
from src.model.direction import Direction
from src.model.position import Position
import random


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
        if maze.can_move(ghost.position, direction)
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
        distance = (abs(next_position.x - pacman.position.x)
                    + (abs(next_position.y - pacman.position.y)))
        if distance < best_distance:
            best_distance = distance
            best_moves = [direction]
        elif distance == best_distance:
            best_moves.append(direction)
    chosen_direction = random.choice(best_moves)
    if chosen_direction == Direction.NORTH:
        ghost.position = Position(ghost.position.x, ghost.position.y - 1)
    elif chosen_direction == Direction.EAST:
        ghost.position = Position(ghost.position.x + 1, ghost.position.y)
    elif chosen_direction == Direction.SOUTH:
        ghost.position = Position(ghost.position.x, ghost.position.y + 1)
    elif chosen_direction == Direction.WEST:
        ghost.position = Position(ghost.position.x - 1, ghost.position.y)
    ghost.direction = chosen_direction
