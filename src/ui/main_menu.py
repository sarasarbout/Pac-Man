import pygame
from pygame.font import Font
from src.parser.config_parser import GameConfig
from pathlib import Path
from src.ui.cheat_menu import CheatState, cheat_menu


"""generate.py is in project_root/src/draw/"""
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
    screen: pygame.Surface,
    cheats: CheatState,
) -> tuple[str, CheatState]:
    intro = False
    pygame.display.set_caption("Main Menu")
    clock = pygame.time.Clock()

    WHITE = (255, 255, 255)
    BUTTON_COLOR = ("Blue")
    HOVER_COLOR = (100, 200, 100)

    background_image = pygame.image.load(
        ASSETS_DIR / "main_menu.png"
    ).convert()
    intro_sound = pygame.mixer.Sound(ASSETS_DIR / "sounds" / "intro.mp3")

    logo_image = pygame.image.load(
        ASSETS_DIR / "pacman_logo.png"
    ).convert_alpha()

    def layout_for(
        current_screen: pygame.Surface,
    ) -> tuple[
        int,
        int,
        pygame.Surface,
        pygame.Surface,
        list[tuple[pygame.Rect, str, str]],
        Font,
    ]:
        width, height = current_screen.get_size()
        background = pygame.transform.scale(
            background_image, (width, height)
        )
        logo = pygame.transform.scale(
            logo_image,
            (min(300, max(1, width - 40)), min(120, max(1, height // 4))),
        )
        button_width = max(1, min(300, width - 40))
        button_height = max(1, min(50, height // 12))
        button_x = (width - button_width) // 2
        pygame.font.init()
        font = pygame.font.SysFont(
            "Arial",
            max(1, min(32, button_height - 8, button_width // 8)),
        )
        buttons = [
            (
                pygame.Rect(
                    button_x,
                    int(height * fraction),
                    button_width,
                    button_height,
                ),
                label,
                state,
            )
            for fraction, label, state in (
                (0.42, "Start Game", "playing"),
                (0.54, "View Highscores", "highscores"),
                (0.66, "Instructions", "instructions"),
                (0.78, "Exit", "exit"),
            )
        ]
        return width, height, background, logo, buttons, font

    WIDTH, HEIGHT, bg_img, logo_img, buttons, font = layout_for(
        screen
    )

    cheats = {
        "Invincibility": False,
        "Freeze Ghosts": False,
        "Speed Boost": False,
        "Speed Multiplier": 1.5
    }

    while True:
        mouse_pos = pygame.mouse.get_pos()
        if not intro:
            intro_sound.play()
        for event in pygame.event.get():
            if event.type == pygame.VIDEORESIZE:
                screen = pygame.display.get_surface()
                config.screen_width, config.screen_height = event.size
                WIDTH, HEIGHT, bg_img, logo_img, buttons, font = layout_for(
                    screen
                )
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F1:
                    intro_sound.stop()
                    action, cheats = cheat_menu(screen, cheats)

                    if action == "exit":
                        return "exit", cheats
                    intro = True
                    intro_sound.play(-1)

            if event.type == pygame.QUIT:
                return "exit", cheats

            if (
                event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
            ):
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for button, label, next_state in buttons:
                        if button.collidepoint(event.pos):
                            intro_sound.stop()
                            return next_state, cheats

        screen.blit(bg_img, (0, 0))

        """Cheat mode instruction"""
        hint_font = pygame.font.SysFont(
            "Arial",
            max(12, min(24, HEIGHT // 24, WIDTH // 35)),
            bold=True,
        )

        hint_text = "F1 - CHEAT MODE"
        hint_surface = hint_font.render(
            hint_text, True, (255, 230, 0)
        )

        hint_rect = hint_surface.get_rect(
            bottomright=(WIDTH - 25, HEIGHT - 25)
        )

        """ Dark background behind the text"""
        panel = hint_rect.inflate(30, 18)
        pygame.draw.rect(
            screen, (5, 5, 35), panel, border_radius=10
        )

        """Blue border for the Pac-Man theme"""
        pygame.draw.rect(
            screen, (0, 70, 255), panel, width=2, border_radius=10
        )

        screen.blit(hint_surface, hint_rect)

        hint_font = pygame.font.SysFont(
            "Arial",
            max(12, min(24, HEIGHT // 24, WIDTH // 35)),
            bold=True,
        )

        hint_text = "F1 - CHEAT MODE"
        hint_surface = hint_font.render(
            hint_text, True, (255, 230, 0)
        )

        hint_rect = hint_surface.get_rect(
            bottomright=(WIDTH - 25, HEIGHT - 25)
        )

        panel = hint_rect.inflate(30, 18)
        pygame.draw.rect(
            screen, (5, 5, 35), panel, border_radius=10
        )

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
