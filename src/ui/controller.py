from mazegenerator.maze_game import create_the_maze 
from model.pacman import Pacman
from model.position import Position
from model.direction import Direction
from model.game_state import GameStatus
from ui.menu import main_menu
import pygame
import sys
from src.parser.config_parser import GameConfig

def run_game(config: GameConfig, screen ):
    """initailize and run the maze"""
    pacman = Pacman(
        Direction.EAST,
        Position(4, 1),
        GameStatus.READY
    )
    return create_the_maze(pacman, 0.3, config, screen)


#State controller
def main(config, screen):
    state = "menu"
    while True:
        if state == "menu":
            state = main_menu(config, screen)
        elif state == "playing":
            state = run_game(config, screen)
        elif state == "highscores":
            state = "menu"
        elif state == "instructions":
            state = "menu"

        elif state == "exit":
            pygame.quit()
            sys.exit()