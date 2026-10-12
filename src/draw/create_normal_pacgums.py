from src.model.pacman import Pacman
from src.model.position import Position
from src.model.cell import Pacgum
from typing import List


def create_normal_pacgums(pacman: Pacman, rows) -> List[Pacgum]:
    normal_pacgums = set()
    width = len(rows[0])
    height = len(rows)
    super_pacgums = {
        Pacgum(Position(0, 0)),
        Pacgum(Position(width - 1, 0)),
        Pacgum(Position(0, height - 1)),
        Pacgum(Position(width - 1, height - 1))
    }
    for row in range(height):
        for column in range(width):
            if rows[row][column] == 15:
                continue
            position = Position(column, row)
            if pacman.position == position:
                continue
            has_super_pacgum = False
            for big in super_pacgums:
                if big.position == position:
                    has_super_pacgum = True
                    break
            if has_super_pacgum:
                continue
            normal_pacgums.add(Pacgum(position))
    return normal_pacgums
