import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((800, 600))

while True:
    # Look through all events that happened this frame
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        # Check for left click
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            print("Left mouse button clicked!")
            
            # Optional: Get the exact (x, y) coordinates of the click
            click_pos = event.pos
            print(f"Clicked at coordinates: {click_pos}")
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            print("Right mouse button clicked!")