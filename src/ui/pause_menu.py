import pygame
from pygame.font import Font
from src.parser.config_parser import GameConfig
from pathlib import Path



# generate.py is in project_root/src/draw/
PROJECT_ROOT = Path(__file__).resolve().parents[2]
ASSETS_DIR = PROJECT_ROOT / "assets"


def draw_text(
    text: str,
    font: Font,
    color: tuple[int, int, int],
    surface: pygame.Surface,
    x: int,
    y: int
) -> None:
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)


##Resume the game - Allows the player to return to the ongoing game.
##Return to the main menu - Allows the player to exit the current game and go
##back to the main menu.

def pause_menu(config: GameConfig, screen) -> str:
    WIDTH = config.screen_width
    HEIGHT = config.screen_height

    HOVER_COLOR = (100, 200, 100)
    WHITE = (255, 255, 255)
    BUTTON_COLOR = (0, 0, 0)

    pygame.display.set_caption("Pause Menu")
    clock = pygame.time.Clock()

    bg_img = pygame.image.load(
        ASSETS_DIR / "Background.png"
    ).convert()

    bg_img = pygame.transform.scale(
        bg_img, (WIDTH, HEIGHT)
    )

    logo_img = pygame.image.load(
        ASSETS_DIR / "pacman_logo.png"
    ).convert_alpha()

    logo_img = pygame.transform.scale(logo_img, (300, 120))

    font = pygame.font.SysFont("Arial", 26)

    button_width = 300
    button_height = 50
    button_x = (WIDTH - button_width) // 2

    button_positions = [
        int(HEIGHT * 0.42),
        int(HEIGHT * 0.54)
    ]

    resume_button = pygame.Rect(
        button_x, button_positions[0], button_width, button_height
    )

    main_button = pygame.Rect(
        button_x, button_positions[1], button_width, button_height
    )
    buttons = [
        (resume_button, "Resume", "playing"),
        (main_button, "Main menu", "main_menu")
    ]

    while True:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"

            if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
                for button, label, next_state in buttons:
                    if button .collidepoint(event.pos):
                        return next_state
        # screen.blit(bg_img, (0, 0))

        logo_rect = logo_img.get_rect(
            center=(WIDTH // 2, int(HEIGHT * 0.16))
        )

        screen.blit(logo_img, logo_rect)

        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        screen.blit(overlay, (0, 0))

        for button, label, next_state in buttons:
            color = (
                HOVER_COLOR
                if button.collidepoint(mouse_pos)
                else BUTTON_COLOR
            )

            pygame.draw.rect(
                screen, color, button, border_radius=10
            )

            draw_text(
                label, 
                font,
                WHITE,
                screen,
                button.centerx,
                button.centery
            )
        pygame.display.flip()
        clock.tick(60)
