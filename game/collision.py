"""This file represent what happens when Pac-max is in
the same position as something else(ghost)"""

from model.ghost import Ghost
from model.pacman import Pacman


class Collision:
    def check(self, pacman: Pacman, ghost: Ghost) -> None:
        pass