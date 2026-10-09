import pygame


def draw_ghosts(rows, width, height, screen, cell_size, ghosts_data) -> None:
    ghost_size = 30
    for ghost, image_path in ghosts_data:
        image = pygame.image.load(image_path)
        image = pygame.transform.scale(image, (ghost_size, ghost_size))
        x = ghost.position.x * cell_size + (cell_size - ghost_size) // 2
        y = ghost.position.y * cell_size + (cell_size - ghost_size) // 2

        screen.blit(image, (x, y))
