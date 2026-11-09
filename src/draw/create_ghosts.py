from dataclasses import dataclass
import pygame
from src.model.ghost import Ghost, GhostMode, GhostName
from src.model.direction import Direction
from src.model.position import Position
from src.model.maze import Maze
from src.model.pacman import Pacman
import heapq
from itertools import count
from pathlib import Path
import random
from typing import Optional

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ASSETS_DIR = PROJECT_ROOT / "assets"


@dataclass(frozen=True)
class GhostAnimation:
    start_x: float
    start_y: float
    end_x: float
    end_y: float
    started_at: int
    duration: int

    @classmethod
    def stationary(
        cls, position: Position, started_at: int
    ) -> "GhostAnimation":
        return cls(
            position.x,
            position.y,
            position.x,
            position.y,
            started_at,
            1,
        )

    @classmethod
    def between(
        cls,
        start: Position,
        end: Position,
        started_at: int,
        duration: int,
    ) -> "GhostAnimation":
        return cls(
            start.x,
            start.y,
            end.x,
            end.y,
            started_at,
            duration,
        )

    def position_at(self, now: int) -> tuple[float, float]:
        progress = min(1.0, max(0.0, (now - self.started_at) / self.duration))
        return (
            self.start_x + (self.end_x - self.start_x) * progress,
            self.start_y + (self.end_y - self.start_y) * progress,
        )


def draw_ghosts(
    screen: pygame.Surface,
    cell_size: int,
    ghosts_data: list[tuple[Ghost, Path]],
    animations: dict[Ghost, GhostAnimation],
    current_time: int,
) -> None:
    for ghost, image_path in ghosts_data:
        if ghost.mode == GhostMode.frightened:
            image_path = ASSETS_DIR / "ghosts" / "blue_ghost.png"
            image = pygame.image.load(image_path)
        else:
            image = pygame.image.load(image_path)
        ghost_bounds = ghost_rect(
            animations[ghost],
            cell_size,
            current_time,
        )
        image = pygame.transform.scale(
            image,
            ghost_bounds.size,
        )
        screen.blit(image, ghost_bounds)


def ghost_rect(
    animation: GhostAnimation,
    cell_size: int,
    current_time: int,
) -> pygame.Rect:
    ghost_size = max(1, int(cell_size * 0.6))
    grid_x, grid_y = animation.position_at(current_time)
    x = round(grid_x * cell_size + (cell_size - ghost_size) / 2)
    y = round(grid_y * cell_size + (cell_size - ghost_size) / 2)
    return pygame.Rect(x, y, ghost_size, ghost_size)


def heuristic(position: tuple[int, int], goal: tuple[int, int]) -> int:
    """Estimate the distance to the goal using Manhattan distance."""
    return (
        abs(position[0] - goal[0])
        + abs(position[1] - goal[1])
    )


def find_path_astar(
    start: Position, goal: Position, maze: Maze
) -> list[Direction]:
    """
    Find the shortest route from start to goal using A* search.

    The route is returned as directions. An empty list means the start is
    already at the goal or no route is available.
    """
    start_cell = (start.x, start.y)
    goal_cell = (goal.x, goal.y)

    if start_cell == goal_cell:
        return []

    directions = [
        (Direction.NORTH, (0, -1)),
        (Direction.EAST, (1, 0)),
        (Direction.SOUTH, (0, 1)),
        (Direction.WEST, (-1, 0)),
    ]

    # The frontier holds cells that still need to be checked.
    # Each entry is (estimated total distance, insertion order, cell).
    insertion_order = count()
    frontier: list[tuple[int, int, tuple[int, int]]] = []
    first_estimate = heuristic(start_cell, goal_cell)
    heapq.heappush(
        frontier, (first_estimate, next(insertion_order), start_cell)
    )

    # Remember the shortest distance found so far to each cell.
    distance_from_start: dict[tuple[int, int], int] = {
        start_cell: 0
    }

    # Remember how we reached each cell to build the route at the end.
    previous_step: dict[
        tuple[int, int], tuple[tuple[int, int], Direction]
    ] = {}

    while frontier:
        _, _, current_cell = heapq.heappop(frontier)

        if current_cell == goal_cell:
            # Follow the recorded steps backwards, then reverse the route.
            path: list[Direction] = []
            cell = current_cell

            while cell != start_cell:
                previous_cell, direction = previous_step[cell]
                path.append(direction)
                cell = previous_cell

            path.reverse()
            return path

        current_position = Position(*current_cell)

        for direction, (step_x, step_y) in directions:
            if not maze.can_move(current_position, direction):
                continue

            neighbor = (
                current_cell[0] + step_x,
                current_cell[1] + step_y,
            )
            tentative_distance = distance_from_start[current_cell] + 1
            best_known_distance = distance_from_start.get(
                neighbor, float("inf")
            )

            if tentative_distance < best_known_distance:
                distance_from_start[neighbor] = tentative_distance
                previous_step[neighbor] = (current_cell, direction)

                # Prefer cells that are close so far and look close to the
                # goal.
                estimate_to_goal = heuristic(neighbor, goal_cell)
                estimated_total_distance = (
                    tentative_distance + estimate_to_goal
                )
                heapq.heappush(
                    frontier,
                    (
                        estimated_total_distance,
                        next(insertion_order),
                        neighbor,
                    ),
                )

    return []


def chase_pacman(
    ghost: Ghost, pacman: Pacman, maze: Maze, ghosts: list[Ghost]
) -> Optional[list[Direction]]:
    path = find_path_astar(
        ghost.position,
        pacman.position,
        maze
    )

    if not path:
        return None
    occupied_positions = {
        other.position
        for other in ghosts
        if other != ghost and other.mode != GhostMode.DEAD
    }
    chosen_direction = path[0]

    if chosen_direction == Direction.NORTH:
        next_position = Position(
            ghost.position.x, ghost.position.y - 1
        )
    elif chosen_direction == Direction.EAST:
        next_position = Position(
            ghost.position.x + 1, ghost.position.y
        )
    elif chosen_direction == Direction.SOUTH:
        next_position = Position(
            ghost.position.x, ghost.position.y + 1
        )
    elif chosen_direction == Direction.WEST:
        next_position = Position(
            ghost.position.x - 1, ghost.position.y
        )
    if next_position in occupied_positions:
        return []
    ghost.position = next_position
    ghost.direction = chosen_direction
    return None


def walk_away(ghost: Ghost, pacman: Pacman, maze: Maze) -> None:
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


def move_ghost_randomly(ghost: Ghost, maze: Maze) -> None:
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


def respawn_ghosts(ghost: Ghost, width: int, height: int) -> Position:
    if ghost.name == GhostName.BLINKY:
        ghost.position = Position(1, 0)
    elif ghost.name == GhostName.CLYDE:
        ghost.position = Position(width - 1, 1)
    elif ghost.name == GhostName.PINKY:
        ghost.position = Position(1, height - 1)
    elif ghost.name == GhostName.INKY:
        ghost.position = Position(width - 1, height - 1)
    return ghost.position
