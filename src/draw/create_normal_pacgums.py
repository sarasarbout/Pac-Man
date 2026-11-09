from src.model.pacman import Pacman
from src.model.position import Position
from src.model.cell import Pacgum
import random
from src.parser.config_parser import GameConfig


def create_normal_pacgums(
        pacman: Pacman, rows: list[list[int]], level_index: int,
        config: GameConfig
) -> set[Pacgum]:
    normal_pacgums = set()
    width = int(len(rows[0]))
    height = len(rows)

    pacgums_number = config.levels[level_index]["pacgum"]

    super_pacgums = {
        Position(0, 0),
        Position(width - 1, 0),
        Position(0, height - 1),
        Position(width - 1, height - 1)
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
        pacgums_number = len(eligible_cells)
        print("Warning: fallback to the eligible_cells!")

    selected_cells = random.sample(eligible_cells, pacgums_number)

    normal_pacgums = {
        Pacgum(position) for position in selected_cells
    }

    return normal_pacgums
