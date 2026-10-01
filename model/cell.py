from model.direction import Direction


class Cell:
    def __init__(self, walls: int) -> None:
        self.walls = walls

    def has_wall(self, direction: Direction) -> bool:
        return (self.walls & direction.value) != 0


# cell = Cell(3)
# print(cell.has_Wall(Direction.NORTH))
# print(cell.has_Wall(Direction.EAST))
# print(cell.has_Wall(Direction.SOUTH))
# print(cell.has_Wall(Direction.WEST))
