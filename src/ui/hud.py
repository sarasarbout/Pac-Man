import pygame
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ASSETS_DIR = PROJECT_ROOT / "assets"

def hud_menu(
    screen: pygame.Surface,
    pacman,
    elapsed_seconds,
    level_index,
    config,
    game_started,
) -> None:
    hud_height = 100
    margin_x = 4

    button_score = pygame.Rect(
        margin_x,
        screen.get_height() - hud_height,
        screen.get_width() - 2 * margin_x,
        hud_height,
    )

    level_time = config.levels[level_index]["time"]

    pygame.draw.rect(screen, "Black", button_score)

    score_font = pygame.font.Font(None, 32)
    score_text = score_font.render(
        f"Score: {pacman.score}", True, "White"
    )

    lives_font = pygame.font.Font(None, 32)
    lives_text = lives_font.render(
        f"Lives: {pacman.lives}", True, "White"
    )

    remaining_seconds = max(0, level_time - elapsed_seconds) \
        if game_started else level_time

    time_font = pygame.font.Font(None, 32)
    time_text = time_font.render(
        f"Time: {remaining_seconds}s", True, "White"
    )

    text1_x = button_score.x + 30
    text1_y = button_score.y + (
        button_score.height - score_text.get_height()
    ) // 2

    text2_x = button_score.right - lives_text.get_width() - 30
    text2_y = button_score.y + (
        button_score.height - lives_text.get_height()
    ) // 2

    text3_x = button_score.centerx - time_text.get_width() // 2
    text3_y = button_score.y + (
        button_score.height - time_text.get_height()
    ) // 2

    screen.blit(score_text, (text1_x, text1_y))
    screen.blit(lives_text, (text2_x, text2_y))
    screen.blit(time_text, (text3_x, text3_y))