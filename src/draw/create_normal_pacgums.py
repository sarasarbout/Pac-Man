from src.model.pacman import Pacman
from src.model.position import Position
from src.model.cell import Pacgum
from typing import List
import random


def create_normal_pacgums(pacman: Pacman, rows, level_index, config) -> List[Pacgum]:
    normal_pacgums = set()
    width = len(rows[0])
    height = len(rows)

    pacgums_number = config.levels[level_index]["pacgum"]
    super_pacgums = {
        Pacgum(Position(0, 0)),
        Pacgum(Position(width - 1, 0)),
        Pacgum(Position(0, height - 1)),
        Pacgum(Position(width - 1, height - 1))
    }
    eligible_cells = []

    for row in range(height):
        for column in range(width):
            if rows[row][column] == 15:
                continue

            position = Position(column, row)
    
            if pacman.position == position:
                continue

            if position in super_pacgums:
                continue

            eligible_cells.append(position)

    if pacgums_number > len(eligible_cells):
        raise ValueError("Not enough eligible cells for Pac-Gums")

    selected_cells = random.sample(eligible_cells, pacgums_number)

    normal_pacgums = {
        Pacgum(position) for position in selected_cells
    }

    return normal_pacgums
