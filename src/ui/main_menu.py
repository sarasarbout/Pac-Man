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


def main_menu(
    config: GameConfig,
    screen: pygame.Surface
) -> str:

    intro = False
    WIDTH = config.screen_width
    HEIGHT = config.screen_height

    pygame.display.set_caption("Main Menu")
    clock = pygame.time.Clock()

    WHITE = (255, 255, 255)
    BUTTON_COLOR = ("Blue")
    HOVER_COLOR = (100, 200, 100)

    bg_img = pygame.image.load(
        ASSETS_DIR / "main_menu.png"
    ).convert()
    intro_sound = pygame.mixer.Sound(ASSETS_DIR / "sounds" / "intro.mp3")
    bg_img = pygame.transform.scale(
        bg_img, (WIDTH, HEIGHT)
    )

    logo_img = pygame.image.load(
        ASSETS_DIR / "pacman_logo.png"
    ).convert_alpha()

    logo_img = pygame.transform.scale(logo_img, (300, 120))

    font = pygame.font.SysFont("Arial", 32)

    button_width = 300
    button_height = 50
    button_x = (WIDTH - button_width) // 2

    # Position the buttons relative to the window height.
    button_positions = [
        int(HEIGHT * 0.42),
        int(HEIGHT * 0.54),
        int(HEIGHT * 0.66),
        int(HEIGHT * 0.78)
    ]

    start_button = pygame.Rect(
        button_x, button_positions[0], button_width, button_height
    )
    highscores_button = pygame.Rect(
        button_x, button_positions[1], button_width, button_height
    )
    instructions_button = pygame.Rect(
        button_x, button_positions[2], button_width, button_height
    )
    exit_button = pygame.Rect(
        button_x, button_positions[3], button_width, button_height
    )

    buttons = [
        (start_button, "Start Game", "playing"),
        (highscores_button, "View Highscores", "highscores"),
        (instructions_button, "Instructions", "instructions"),
        (exit_button, "Exit", "exit")
    ]

    while True:
        mouse_pos = pygame.mouse.get_pos()
        if not intro:
            intro_sound.play()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"

            if (
                event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
            ):
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for button, label, next_state in buttons:
                        if button.collidepoint(event.pos):
                            intro_sound.stop()
                            return next_state

        screen.blit(bg_img, (0, 0))

        # Cheat mode instruction
        hint_font = pygame.font.SysFont("Arial", 24, bold=True)

        hint_text = "F1 - CHEAT MODE"
        hint_surface = hint_font.render(
            hint_text, True, (255, 230, 0)
        )

        hint_rect = hint_surface.get_rect(
            bottomright=(WIDTH - 25, HEIGHT - 25)
        )

        # Dark background behind the text
        panel = hint_rect.inflate(30, 18)
        pygame.draw.rect(
            screen, (5, 5, 35), panel, border_radius=10
        )

        # Blue border for the Pac-Man theme
        pygame.draw.rect(
            screen, (0, 70, 255), panel, width=2, border_radius=10
        )

        screen.blit(hint_surface, hint_rect)
        

        logo_rect = logo_img.get_rect(
            center=(WIDTH // 2, int(HEIGHT * 0.16))
        )
        screen.blit(logo_img, logo_rect)

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
