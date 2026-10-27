import pygame
from src.model.ghost import GhostMode, GhostName
from src.model.direction import Direction
from src.model.position import Position
import heapq
from itertools import count
from pathlib import Path
import random

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ASSETS_DIR = PROJECT_ROOT / "assets"


def draw_ghosts(rows, width, height, screen, cell_size, ghosts_data) -> None:
    ghost_size = 30
    for ghost, image_path in ghosts_data:
        if ghost.mode == GhostMode.frightened:
            image_path = ASSETS_DIR / "ghosts" / "blue_ghost.png"
            image = pygame.image.load(image_path)
        else:
            image = pygame.image.load(image_path)
        image = pygame.transform.scale(image, (ghost_size, ghost_size))
        x = ghost.position.x * cell_size + (cell_size - ghost_size) // 2
        y = ghost.position.y * cell_size + (cell_size - ghost_size) // 2

        screen.blit(image, (x, y))


def heuristic(position, goal):
    """Estimate the distance to the goal using Manhattan distance."""
    return (
        abs(position[0] - goal[0])
        + abs(position[1] - goal[1])
    )


def find_path_astar(start, goal, maze):
    """
    Return a list of directions from start to goal.
    Return [] if no path exists.
    """

    start = (start.x, start.y)
    goal = (goal.x, goal.y)

    if start == goal:
        return []

    directions = [
        Direction.NORTH,
        Direction.EAST,
        Direction.SOUTH,
        Direction.WEST,
    ]
    occupied_paths = []

    counter = count()
    open_set = [
        (heuristic(start, goal), next(counter), start)
    ]

    g_score = {start: 0}
    came_from = {}

    while open_set:
        _, _, current = heapq.heappop(open_set)

        if current == goal:
            path = []

            while current != start:
                previous, direction = came_from[current]
                path.append(direction)
                current = previous

            path.reverse()
            return path

        current_position = Position(*current)

        for direction in directions:
            if not maze.can_move(current_position, direction):
                continue

            if direction == Direction.NORTH:
                neighbor = (current[0], current[1] - 1)
            elif direction == Direction.EAST:
                neighbor = (current[0] + 1, current[1])
            elif direction == Direction.SOUTH:
                neighbor = (current[0], current[1] + 1)
            else:
                neighbor = (current[0] - 1, current[1])

            tentative_g = g_score[current] + 1

            if tentative_g < g_score.get(
                neighbor, float("inf")
            ):
                g_score[neighbor] = tentative_g
                came_from[neighbor] = (current, direction)

                f_score = (
                    tentative_g + heuristic(neighbor, goal)
                )

                heapq.heappush(
                    open_set,
                    (f_score, next(counter), neighbor)
                )
    return []


def chase_pacman(ghost, pacman, maze) -> None:
    path = find_path_astar(
        ghost.position,
        pacman.position,
        maze
    )

    if not path:
        return

    chosen_direction = path[0]

    if chosen_direction == Direction.NORTH:
        ghost.position = Position(
            ghost.position.x, ghost.position.y - 1
        )
    elif chosen_direction == Direction.EAST:
        ghost.position = Position(
            ghost.position.x + 1, ghost.position.y
        )
    elif chosen_direction == Direction.SOUTH:
        ghost.position = Position(
            ghost.position.x, ghost.position.y + 1
        )
    elif chosen_direction == Direction.WEST:
        ghost.position = Position(
            ghost.position.x - 1, ghost.position.y
        )

    ghost.direction = chosen_direction


def walk_away(ghost, pacman, maze) -> None:
    possible_moves = [
        direction
        for direction in
        (
            Direction.NORTH,
            Direction.EAST,
            Direction.SOUTH,
            Direction.WEST
        )
        if maze.can_move(ghost.position, direction)
    ]
    if not possible_moves:
        return
    best_distance = -1
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
                    + abs(next_position.y - pacman.position.y))
        if distance > best_distance:
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


def move_ghost_randomly(ghost, maze) -> None:
    directions = [
        Direction.NORTH,
        Direction.EAST,
        Direction.SOUTH,
        Direction.WEST,
    ]

    valid_directions = [
        direction
        for direction in directions
        if maze.can_move(ghost.position, direction)
    ]

    if not valid_directions:
        return

    chosen_direction = random.choice(valid_directions)

    if chosen_direction == Direction.NORTH:
        ghost.position = Position(
            ghost.position.x, ghost.position.y - 1
        )
    elif chosen_direction == Direction.EAST:
        ghost.position = Position(
            ghost.position.x + 1, ghost.position.y
        )
    elif chosen_direction == Direction.SOUTH:
        ghost.position = Position(
            ghost.position.x, ghost.position.y + 1
        )
    elif chosen_direction == Direction.WEST:
        ghost.position = Position(
            ghost.position.x - 1, ghost.position.y
        )
    ghost.direction = chosen_direction


def respawn_ghosts(ghost, width, height) -> None:
    if ghost.name == GhostName.BLINKY:
        ghost.position = Position(1, 0)
    elif ghost.name == GhostName.CLYDE:
        ghost.position = Position(width - 1, 1)
    elif ghost.name == GhostName.PINKY:
        ghost.position = Position(1, height - 1)
    elif ghost.name == GhostName.INKY:
        ghost.position = Position(width - 1, height - 1)
    return ghost.position