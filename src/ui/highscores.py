import pygame
from src.parser.config_parser import GameConfig
from src.model.highscores import load_scores


def highscores(config: GameConfig, screen: pygame.Surface) -> str:
    pygame.display.set_caption("High Scores")

    width, height = screen.get_size()
    clock = pygame.time.Clock()

    title_font = pygame.font.Font(None, 64)
    header_font = pygame.font.Font(None, 30)
    row_font = pygame.font.Font(None, 32)
    button_font = pygame.font.Font(None, 32)

    BLACK = (5, 5, 5)
    BLUE = (35, 35, 255)
    YELLOW = (255, 230, 0)
    CYAN = (100, 245, 255)
    WHITE = (255, 255, 255)
    BUTTON = (32, 32, 80)
    HOVER = (70, 70, 145)

    scores = load_scores(config)

    button = pygame.Rect(
        width // 2 - 120,
        height - 90,
        240,
        50,
    )

    while True:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"

            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_RETURN):
                    return "main_menu"

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and button.collidepoint(event.pos):
                    return "main_menu"

        screen.fill(BLACK)

        pygame.draw.rect(
            screen,
            BLUE,
            (4, 4, width - 8, height - 8),
            width=4,
        )

        title = title_font.render("HIGH SCORES", True, YELLOW)

        screen.blit(
            title,
            title.get_rect(center=(width // 2, 75)),
        )

        table_top = 145
        rank_x = width // 2 - 280
        name_x = width // 2 - 170
        score_right = width // 2 + 280

        screen.blit(
            header_font.render("RANK", True, YELLOW),
            (rank_x, table_top),
        )
        screen.blit(
            header_font.render("PLAYER", True, YELLOW),
            (name_x, table_top),
        )

        score_header = header_font.render("SCORE", True, YELLOW)
        screen.blit(
            score_header,
            (score_right - score_header.get_width(), table_top),
        )

        if not scores:
            empty = row_font.render(
                "No scores yet! Be the first player.",
                True,
                WHITE,
            )
            screen.blit(
                empty,
                empty.get_rect(center=(width // 2, height // 2)),
            )

        for index, entry in enumerate(scores):
            y = table_top + 45 + index * 42

            pygame.draw.line(
                screen,
                (35, 35, 35),
                (width // 2 - 290, y + 32),
                (width // 2 + 290, y + 32),
                1,
            )

            rank_color = YELLOW if index == 0 else WHITE

            rank = row_font.render(
                f"{index + 1:02}",
                True,
                rank_color,
            )
            name = row_font.render(
                str(entry.get("name", "Player"))[:16],
                True,
                WHITE,
            )
            score = row_font.render(
                str(entry.get("score", 0)),
                True,
                CYAN,
            )

            screen.blit(rank, (rank_x, y))
            screen.blit(name, (name_x, y))
            screen.blit(
                score,
                (score_right - score.get_width(), y),
            )

        button_color = (
            HOVER if button.collidepoint(mouse_pos) else BUTTON
        )

        pygame.draw.rect(
            screen,
            button_color,
            button,
            border_radius=8,
        )

        label = button_font.render("MAIN MENU", True, WHITE)
        screen.blit(label, label.get_rect(center=button.center))

        pygame.display.flip()
        clock.tick(60)
