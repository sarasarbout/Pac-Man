"""This file represent what happens when Pac-max is in
the same position as something else(ghost)"""

from model.pacman import Pacman
from model.direction import Direction
from model.position import Position
from model.ghost import Ghost, Color, GhostMode, GhostName


class Collision:
    def check(self, pacman: Pacman, ghost: Ghost) -> bool:
        return pacman.position == ghost.position


# ==== Test ====
# pacman = Pacman(Direction.EAST, Position(4, 1))
# ghost = Ghost(GhostName.BLINKY, Position(0, 1), Direction.SOUTH, Color.RED, GhostMode.CHASE)

# collision = Collision()
# print(collision.check(pacman,  ghost))
