
import json
import pygame
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def save_score(config, player_name: str, final_score: int) -> None:
    """Save the player's name and score to the highscores JSON file."""

    filename = Path(config.highscore_filename)

    if not filename.is_absolute():
        filename = PROJECT_ROOT / filename

    if filename.exists():
        try:
            with filename.open("r", encoding="utf-8") as file:
                scores = json.load(file)

            if not isinstance(scores, list):
                scores = []
        except (json.JSONDecodeError, OSError):
            scores = []
    else:
        scores = []

    scores.append({
        "name": player_name,
        "score": final_score,
    })

    scores.sort(key=lambda entry: entry["score"], reverse=True)

    with filename.open("w", encoding="utf-8") as file:
        json.dump(scores, file, indent=4, ensure_ascii=False)


def game_over(config, screen, final_score: int) -> str:
    """Display Game Over, collect the player's name, and save the score."""

    pygame.display.set_caption("Game Over")

    width, height = screen.get_size()

    title_font = pygame.font.Font(None, 80)
    text_font = pygame.font.Font(None, 38)
    button_font = pygame.font.Font(None, 32)

    background_color = (10, 10, 25)
    text_color = (255, 255, 255)
    button_color = (40, 40, 80)
    hover_color = (80, 80, 140)

    player_name = ""
    max_name_length = 16
    message = ""

    input_rect = pygame.Rect(
        (width - 360) // 2,
        height // 2 + 15,
        360,
        50,
    )

    save_button = pygame.Rect(
        (width - 220) // 2,
        height // 2 + 85,
        220,
        50,
    )

    menu_button = pygame.Rect(
        (width - 220) // 2,
        height // 2 + 150,
        220,
        50,
    )

    exit_button = pygame.Rect(
        (width - 220) // 2,
        height // 2 + 215,
        220,
        50,
    )

    input_active = True
    clock = pygame.time.Clock()

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
                            except OSError as error:
                                message = f"Could not save score: {error}"
                            else:
                                return "main_menu"
                        else:
                            message = "Please enter your name."

                    elif (
                        event.unicode.isprintable()
                        and not event.unicode.isspace()
                        or event.unicode == " "
                    ):
                        if len(player_name) < max_name_length:
                            player_name += event.unicode

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if save_button.collidepoint(event.pos):
                        if player_name.strip():
                            try:
                                save_score(
                                    config,
                                    player_name.strip(),
                                    final_score,
                                )
                            except OSError as error:
                                message = f"Could not save score: {error}"
                            else:
                                return "main_menu"
                        else:
                            message = "Please enter your name."

                    elif menu_button.collidepoint(event.pos):
                        return "main_menu"

                    elif exit_button.collidepoint(event.pos):
                        return "exit"

        screen.fill(background_color)

        title = title_font.render(
            "GAME OVER", True, (255, 60, 60)
        )
        screen.blit(
            title,
            title.get_rect(center=(width // 2, height // 5)),
        )

        score_text = text_font.render(
            f"Final Score: {final_score}",
            True,
            text_color,
        )
        screen.blit(
            score_text,
            score_text.get_rect(
                center=(width // 2, height // 2 - 45)
            ),
        )

        prompt = text_font.render(
            "Enter your name:", True, text_color
        )
        screen.blit(
            prompt,
            prompt.get_rect(
                center=(width // 2, height // 2 - 5)
            ),
        )

        pygame.draw.rect(
            screen, (255, 255, 255), input_rect, 2,
            border_radius=6,
        )

        name_surface = text_font.render(
            player_name, True, text_color
        )
        screen.blit(
            name_surface,
            (input_rect.x + 10, input_rect.y + 8),
        )

        buttons = [
            (save_button, "Save Score"),
            (menu_button, "Main Menu"),
            (exit_button, "Exit"),
        ]

        for button, label in buttons:
            color = (
                hover_color
                if button.collidepoint(mouse_pos)
                else button_color
            )

            pygame.draw.rect(
                screen, color, button, border_radius=8
            )

            label_surface = button_font.render(
                label, True, text_color
            )
            screen.blit(
                label_surface,
                label_surface.get_rect(center=button.center),
            )

        if message:
            message_surface = pygame.font.Font(
                None, 24
            ).render(message, True, (255, 100, 100))

            screen.blit(
                message_surface,
                message_surface.get_rect(
                    center=(width // 2, height - 25)
                ),
            )

        pygame.display.flip()
        clock.tick(60)
