import pygame
import sys

# 1. Initialize Pygame
pygame.init()

# 2. Set up the display window
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Smooth Movement Example")

# 3. Create a clock object to manage our Frame Rate (FPS)
clock = pygame.time.Clock()

# 4. Set up the shape's starting properties
# We use standard pixel coordinates: x, y, width, height
box_x = 50
box_y = 250
box_width = 60
box_height = 60
box_speed = 2  # How many pixels the box moves every single frame

# 5. Main Game Loop
running = True
while running:
    # --- Step A: Check for player input/events ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- Step B: Update game data/positions ---
    # Change the x-coordinate to move it right
    box_y += box_speed

    # If the box goes off the right edge, wrap it back around to the left
    if box_y > screen_height:
        box_y = -box_height

    # --- Step C: Draw everything onto the hidden canvas ---
    # Clear the screen with a dark blue background so old positions are erased
    screen.fill((20, 30, 45))

    # Draw our square directly onto the screen at its updated x position
    pygame.draw.rect(screen, (255, 60, 60), (box_x, box_y, box_width, box_height))

    # --- Step D: Publish the changes ---
    # Swap the hidden canvas to the screen so the player sees the new frame
    pygame.display.flip()

    # --- Step E: Control the speed ---
    # Force the loop to run at exactly 60 frames per second
    clock.tick(60)

# Clean up and exit
pygame.quit()
sys.exit()
