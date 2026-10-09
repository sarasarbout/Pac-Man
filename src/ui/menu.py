import pygame, sys
from pygame.font import Font
pygame.init()

WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Main Menu")
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
GREEN = (50, 200, 50)



BG_IMG = pygame.image.load("/home/iait-mou/Desktop/Pac-Man/assets/Background.png")
#BG_IMG = pygame.transform.scale(BG_IMG, (800, 600))
#convert_alpha preserves transparent parts of the img 
LOGO_IMG = pygame.image.load("/home/iait-mou/Desktop/Pac-Man/assets/pacman_logo.png").convert_alpha()
#scale resize to 300*120 [ixels]
LOGO_IMG = pygame.transform.scale(LOGO_IMG, (300, 120))

BG_COLOR = (0, 0, 0)
BUTTON_COLOR = (0, 0, 0)
HOVER_COLOR = (100, 200, 100)
TEXT_COLOR = (255, 255, 255)

#fonts
FONT = pygame.font.SysFont("Arial", 40)


def draw_text(text: str, font: Font, color: tuple[int, int, int], surface, x: int , y: int)-> None:
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_obj, text_rect)


def main_menu():

    # Define Button Rectangles (X, Y, Width, Height)
    start_button = pygame.Rect(WIDTH // 2 - 100, 250, 200, 50)
    highscores_button = pygame.Rect(WIDTH // 2 - 100, 325, 200, 50)
    instructions_button = pygame.Rect(WIDTH // 2 - 100, 400, 200, 50)
    Exit_button = pygame.Rect(WIDTH // 2 - 100, 475, 200, 50)

    while True:

        SCREEN.blit(BG_IMG, (0,0))

        logo_rect = LOGO_IMG.get_rect(center = (WIDTH // 2, 100))
        SCREEN.blit(LOGO_IMG, logo_rect)

        mouse_pos = pygame.mouse.get_pos()
        
        if start_button.collidepoint(mouse_pos):
            pygame.draw.rect(SCREEN, HOVER_COLOR, start_button, border_radius=10)
        else:
            pygame.draw.rect(SCREEN, BUTTON_COLOR, start_button, border_radius=10)

        if highscores_button.collidepoint(mouse_pos):
            pygame.draw.rect(SCREEN, HOVER_COLOR, highscores_button, border_radius=10)
        else:
            pygame.draw.rect(SCREEN, BUTTON_COLOR, highscores_button, border_radius=10)

        if instructions_button.collidepoint(mouse_pos):
            pygame.draw.rect(SCREEN, HOVER_COLOR, instructions_button, border_radius=10)
        else:
            pygame.draw.rect(SCREEN, BUTTON_COLOR, instructions_button, border_radius=10)

        if Exit_button.collidepoint(mouse_pos):
            pygame.draw.rect(SCREEN, HOVER_COLOR, Exit_button, border_radius=10)
        else:
            pygame.draw.rect(SCREEN, BUTTON_COLOR, Exit_button, border_radius=10)



        draw_text("Start Game", FONT, TEXT_COLOR, SCREEN , start_button.centerx, start_button.centery)
        draw_text("View Highscores", FONT, TEXT_COLOR, SCREEN , highscores_button.centerx, highscores_button.centery)
        draw_text("Instructions", FONT, TEXT_COLOR, SCREEN , instructions_button.centerx, instructions_button.centery)
        draw_text("Exit", FONT, TEXT_COLOR, SCREEN , Exit_button.centerx, Exit_button.centery)


        pygame.display.flip()
        clock.tick(60)


def run_game():
    """Placeholder for gameplay loop."""
    while True:
        
        draw_text("Playing the Game", FONT, WHITE, SCREEN, WIDTH // 2, HEIGHT // 2)
        draw_text("Press ESC to return to Menu", FONT, WHITE, SCREEN, WIDTH // 2, HEIGHT // 2 + 100)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "menu"  # Return to menu state

        pygame.display.flip()
        clock.tick(60)





#State controller
def main():
    state = "menu"
    while True:
        if state == "menu":
            state = main_menu()
        elif state == "playing":
            state = run_game()

if __name__ == "__main__":
    main()

