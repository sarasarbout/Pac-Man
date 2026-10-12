"""This file represent what happens when Pac-max is in
the same position as something else(ghost)"""
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.model.pacman import Pacman
from src.model.ghost import Ghost


class Collision:
    def check(self, pacman: "Pacman", ghost: Ghost) -> bool:
        return pacman.position == ghost.position


# ==== Test ====
# pacman = Pacman(Direction.EAST, Position(4, 1))
# ghost = Ghost(GhostName.BLINKY, Position(0, 1), Direction.SOUTH, Color.RED, GhostMode.CHASE)

# collision = Collision()
# print(collision.check(pacman,  ghost))
