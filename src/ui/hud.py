import pygame
from src.model.pacman import Pacman
from src.parser.config_parser import GameConfig


HUD_HEIGHT = 110
BUTTON_HEIGHT = 32


def get_hud_button_rects(
    screen: pygame.Surface,
) -> tuple[pygame.Rect, pygame.Rect]:
    """Calculate the HUD button positions without drawing anything."""
    width = screen.get_width()
    height = screen.get_height()

    button_width = 125
    pause_width = 90
    gap = 12

    total_width = button_width + gap + pause_width
    start_x = (width - total_width) // 2
    button_y = height - HUD_HEIGHT + 68

    cheats_rect = pygame.Rect(
        start_x, button_y, button_width, BUTTON_HEIGHT
    )

    pause_rect = pygame.Rect(
        cheats_rect.right + gap, button_y,
        pause_width, BUTTON_HEIGHT
    )

    return pause_rect, cheats_rect


def draw_hud_button(
    screen: pygame.Surface,
    rect: pygame.Rect,
    text: str,
    font: pygame.font.Font,
    color: tuple[int, int, int],
) -> None:
    pygame.draw.rect(screen, color, rect, border_radius=8)

    button_text = font.render(text, True, (255, 255, 255))
    screen.blit(button_text, button_text.get_rect(center=rect.center))


def hud_menu(
    screen: pygame.Surface,
    pacman: Pacman,
    elapsed_seconds: int,
    level_index: int,
    config: GameConfig,
    game_started: bool,
) -> tuple[pygame.Rect, pygame.Rect]:
    width = screen.get_width()
    height = screen.get_height()

    hud_rect = pygame.Rect(
        0, height - HUD_HEIGHT, width, HUD_HEIGHT
    )

    pygame.draw.rect(screen, (15, 15, 35), hud_rect)

    info_font = pygame.font.Font(None, 27)

    level_time = config.levels[level_index]["time"]
    level_value = level_index + 1

    remaining_seconds = (
        max(0, level_time - elapsed_seconds)
        if game_started
        else level_time
    )

    information = [
        f"Score: {pacman.score}",
        f"Level: {level_value}",
        f"Lives: {pacman.lives}",
        f"Time: {remaining_seconds}s",
    ]

    column_width = width / 4
    info_y = height - HUD_HEIGHT + 25

    for index, text in enumerate(information):
        text_surface = info_font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(
            center=(
                int(column_width * (index + 0.5)),
                info_y,
            )
        )
        screen.blit(text_surface, text_rect)

    pause_rect, cheats_rect = get_hud_button_rects(screen)
    button_font = pygame.font.Font(None, 23)

    draw_hud_button(
        screen,
        cheats_rect,
        "CHEATS (F1)",
        button_font,
        (53, 53, 120),
    )

    draw_hud_button(
        screen,
        pause_rect,
        "PAUSE",
        button_font,
        (180, 120, 30),
    )

    return pause_rect, cheats_rect
