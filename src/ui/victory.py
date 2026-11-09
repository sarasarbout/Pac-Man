import pygame
from pygame.font import Font
from src.model.highscores import (
    MAX_PLAYER_NAME_LENGTH,
    save_score,
)
from src.parser.config_parser import GameConfig


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


def victory(
    config: GameConfig, screen: pygame.Surface, final_score: int
) -> str:
    """Display the victory screen and allow the player to save their score."""

    pygame.display.set_caption("Victory")

    width, height = screen.get_size()

    BACKGROUND_COLOR = (15, 15, 35)
    BUTTON_COLOR = (0, 0, 0)
    HOVER_COLOR = (100, 200, 100)
    WHITE = (255, 255, 255)
    YELLOW = (255, 220, 0)
    RED = (255, 100, 100)

    title_font = pygame.font.Font(None, 65)
    font = pygame.font.SysFont("Arial", 26)
    message_font = pygame.font.Font(None, 24)

    clock = pygame.time.Clock()

    player_name = ""
    input_active = True
    message = ""

    input_rect = pygame.Rect(
        (width - 300) // 2,
        int(height * 0.52),
        300,
        45,
    )

    button_width = 300
    button_height = 45

    save_rect = pygame.Rect(
        (width - button_width) // 2,
        int(height * 0.62),
        button_width,
        button_height,
    )

    play_again_rect = pygame.Rect(
        (width - button_width) // 2,
        int(height * 0.73),
        button_width,
        button_height,
    )

    menu_rect = pygame.Rect(
        (width - button_width) // 2,
        int(height * 0.84),
        button_width,
        button_height,
    )

    buttons = [
        (save_rect, "SAVE SCORE"),
        (play_again_rect, "PLAY AGAIN"),
        (menu_rect, "MAIN MENU"),
    ]

    while True:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return "exit"

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    return "main_menu"

                if input_active:

                    if event.key == pygame.K_BACKSPACE:
                        player_name = player_name[:-1]

                    elif event.key in (
                        pygame.K_RETURN,
                        pygame.K_KP_ENTER,
                    ):
                        if player_name.strip():
                            try:
                                save_score(
                                    config,
                                    player_name.strip(),
                                    final_score,
                                )
                            except (OSError, ValueError) as error:
                                message = f"Could not save score: {error}"
                            else:
                                return "main_menu"
                        else:
                            message = "Please enter your name."

                    elif (
                        len(player_name) < MAX_PLAYER_NAME_LENGTH
                        and (event.unicode.isalnum() or event.unicode == " ")
                    ):
                        player_name += event.unicode

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:

                    if save_rect.collidepoint(event.pos):

                        if player_name.strip():
                            try:
                                save_score(
                                    config,
                                    player_name.strip(),
                                    final_score,
                                )
                            except (OSError, ValueError) as error:
                                message = f"Could not save score: {error}"
                            else:
                                return "main_menu"
                        else:
                            message = "Please enter your name."

                    elif play_again_rect.collidepoint(event.pos):
                        return "playing"

                    elif menu_rect.collidepoint(event.pos):
                        return "main_menu"

        screen.fill(BACKGROUND_COLOR)

        draw_text(
            "YOU WON!",
            title_font,
            YELLOW,
            screen,
            width // 2,
            int(height * 0.27),
        )

        draw_text(
            f"Final Score: {final_score}",
            font,
            WHITE,
            screen,
            width // 2,
            int(height * 0.40),
        )

        draw_text(
            "Enter your name:",
            font,
            WHITE,
            screen,
            width // 2,
            int(height * 0.48),
        )

        pygame.draw.rect(
            screen,
            WHITE,
            input_rect,
            2,
            border_radius=6,
        )

        name_surface = font.render(
            player_name,
            True,
            WHITE,
        )

        screen.blit(
            name_surface,
            (input_rect.x + 10, input_rect.y + 8),
        )

        for button, label in buttons:

            color = (
                HOVER_COLOR
                if button.collidepoint(mouse_pos)
                else BUTTON_COLOR
            )

            pygame.draw.rect(
                screen,
                color,
                button,
                border_radius=10,
            )

            draw_text(
                label,
                font,
                WHITE,
                screen,
                button.centerx,
                button.centery,
            )

        if message:
            message_surface = message_font.render(
                message,
                True,
                RED,
            )

            screen.blit(
                message_surface,
                message_surface.get_rect(
                    center=(width // 2, int(height * 0.94))
                ),
            )

        pygame.display.flip()
        clock.tick(60)
