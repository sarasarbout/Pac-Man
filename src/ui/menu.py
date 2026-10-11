import pygame, sys
from pygame.font import Font

pygame.init()



def draw_text(text: str, font: Font, color: tuple[int, int, int], surface, x: int , y: int)-> None:
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_obj, text_rect)


def main_menu(config, screen):
    WIDTH = screen.get_width()
    HEIGHT = screen.get_height()
    
    #screen = pygame.display.set_mode((WIDTH, HEIGHT))

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

    # Define Button Rectangles (X, Y, Width, Height)
    start_button = pygame.Rect(WIDTH // 2 - 150, 250, 300, 50)
    highscores_button = pygame.Rect(WIDTH // 2 - 150, 325, 300, 50)
    instructions_button = pygame.Rect(WIDTH // 2 - 150, 400, 300, 50)
    Exit_button = pygame.Rect(WIDTH // 2 - 150, 475, 300, 50)

    while True:

        screen.blit(BG_IMG, (0,0))

        logo_rect = LOGO_IMG.get_rect(center = (WIDTH // 2, 100))
        screen.blit(LOGO_IMG, logo_rect)

        mouse_pos = pygame.mouse.get_pos()
        
        if start_button.collidepoint(mouse_pos):
            pygame.draw.rect(screen, HOVER_COLOR, start_button, border_radius=10)
        else:
            pygame.draw.rect(screen, BUTTON_COLOR, start_button, border_radius=10)

        if highscores_button.collidepoint(mouse_pos):
            pygame.draw.rect(screen, HOVER_COLOR, highscores_button, border_radius=10)
        else:
            pygame.draw.rect(screen, BUTTON_COLOR, highscores_button, border_radius=10)

        if instructions_button.collidepoint(mouse_pos):
            pygame.draw.rect(screen, HOVER_COLOR, instructions_button, border_radius=10)
        else:
            pygame.draw.rect(screen, BUTTON_COLOR, instructions_button, border_radius=10)

        if Exit_button.collidepoint(mouse_pos):
            pygame.draw.rect(screen, HOVER_COLOR, Exit_button, border_radius=10)
        else:
            pygame.draw.rect(screen, BUTTON_COLOR, Exit_button, border_radius=10)



        draw_text("Start Game", FONT, TEXT_COLOR, screen , start_button.centerx, start_button.centery)
        draw_text("View Highscores", FONT, TEXT_COLOR, screen , highscores_button.centerx, highscores_button.centery)
        draw_text("Instructions", FONT, TEXT_COLOR, screen , instructions_button.centerx, instructions_button.centery)
        draw_text("Exit", FONT, TEXT_COLOR, screen , Exit_button.centerx, Exit_button.centery)

        ##events handling for when we click a button we return a state to the controller 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"

            ##mouse event left click

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if start_button.collidepoint(event.pos):
                    return "playing"
                elif highscores_button.collidepoint(event.pos):
                    return "highscores"
                elif instructions_button.collidepoint(event.pos):
                    return "instructions"
                elif Exit_button.collidepoint(event.pos):
                    return "exit"
                
        pygame.display.flip()
        clock.tick(60)




