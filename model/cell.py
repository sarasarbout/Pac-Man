from model.direction import Direction


class Cell:
    def __init__(self, walls: int):
        self.walls = walls

    def has_Wall(self, direction: Direction) -> bool:
        return (self.walls & direction.value) != 0


cell = Cell(13)
print(cell.has_Wall(Direction.NORTH))