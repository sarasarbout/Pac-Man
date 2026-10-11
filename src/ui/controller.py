from mazegenerator.maze_game import create_the_maze 
from model.pacman import Pacman
from model.position import Position
from model.direction import Direction
from model.game_state import GameStatus
from ui.menu import main_menu
import pygame
import sys

def run_game():
    """initailize and run the maze"""
    pacman = Pacman(
        Direction.EAST,
        Position(4, 1),
        GameStatus.READY
    )
    return create_the_maze(pacman, 0.3)


#State controller
def main():
    state = "menu"
    while True:
        if state == "menu":
            state = main_menu()
        elif state == "playing":
            state = run_game()
        elif state == "highscores":
            state = "menu"
        elif state == "instructions":
            state = "menu"

        elif state == "exit":
            pygame.quit()
            sys.exit()

if __name__ == "__main__":
    main()