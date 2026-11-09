import pygame
from src.parser.config_parser import GameConfig


def instructions(config: GameConfig, screen: pygame.Surface) -> str:
    clock = pygame.time.Clock()

    BACKGROUND = (10, 15, 45)
    PANEL_COLOR = (20, 25, 65)
    YELLOW = (255, 230, 0)
    WHITE = (255, 255, 255)
    part_1_coral = (240, 113, 120)  # Soft warm coral-red
    part_2_orange = (247, 140, 108)  # Pastel amber-orange
    part_3_yellow = (255, 203, 107)  # Creamy terminal yellow
    part_4_emerald = (145, 190, 114)  # Soft sage-emerald green
    part_5_mint = (137, 221, 255)  # Crisp minty cyan-blue
    part_6_indigo = (130, 170, 255)  # Clear sky indigo-blue
    part_7_lavender = (199, 146, 234)  # Softer lavender-purple

    title_font = pygame.font.Font(None, 55)
    heading_font = pygame.font.Font(None, 30)
    text_font = pygame.font.Font(None, 24)
    button_font = pygame.font.Font(None, 30)
    running = True

    while running:
        screen_width = screen.get_width()
        screen_height = screen.get_height()

        panel_width = min(650, screen_width * 0.85)
        panel_height = min(650, screen_height * 0.90)

        panel = pygame.Rect(
            0, 0,
            panel_width,
            panel_height
        )
        panel.center = (screen_width // 2, screen_height // 2)

        back_button = pygame.Rect(
            0, 0, 200, 40
        )
        back_button.center = (
            panel.centerx,
            panel.bottom - 45
        )

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return "exit"

            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode(
                    event.size,
                    pygame.RESIZABLE
                )

            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_BACKSPACE):
                    return "main_menu"

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and back_button.collidepoint(event.pos):
                    return "main_menu"

        screen.fill(BACKGROUND)

        pygame.draw.rect(
            screen, PANEL_COLOR, panel, border_radius=15
        )
        pygame.draw.rect(
            screen, YELLOW, panel, 3, border_radius=15
        )

        title = title_font.render("HOW TO PLAY", True, YELLOW)

        screen.blit(
            title,
            (
                panel.centerx - title.get_width() // 2,
                panel.top + 25
            )
        )

        # Instructions
        instructions_text = [
            (
                "OBJECTIVE",
                "Collect all Pac-Gums to complete the level.",
                part_1_coral,
            ),
            (
                "MOVEMENT",
                "Use arrow keys or WASD keys to move Pac-Man.",
                part_2_orange,
            ),
            (
                "SUPER PAC-GUM",
                "Eat it to frighten ghosts temporarily.",
                part_3_yellow,
            ),
            (
                "GHOSTS",
                "Avoid ghosts unless they are frightened.",
                part_4_emerald,
            ),
            (
                "SCORING",
                "Collect Pac-Gums and eat frightened ghosts.",
                part_5_mint,
            ),
            (
                "PAUSE",
                "Press SPACE or click the Pause button.",
                part_6_indigo,
            ),
            (
                "CHEATS",
                "Press F1 to open the cheat menu.",
                part_7_lavender,
            ),
        ]

        content_top = panel.top + 100
        content_bottom = back_button.top - 20

        section_height = 55
        section_gap = 12

        total_content_height = (
            len(instructions_text) * section_height
            + (len(instructions_text) - 1) * section_gap
        )

        y = content_top

        # Center the instructions vertically in the available space
        if total_content_height < content_bottom - content_top:
            y += ((content_bottom - content_top) - total_content_height) // 2

        for heading, description, color in instructions_text:

            heading_surface = heading_font.render(
                heading, True, color
            )

            description_surface = text_font.render(
                description, True, WHITE
            )

            screen.blit(
                heading_surface,
                (panel.left + 35, y)
            )

            screen.blit(
                description_surface,
                (panel.left + 35, y + 27)
            )

            y += section_height + section_gap

        pygame.draw.rect(
            screen, YELLOW, back_button, border_radius=8
        )

        back_text = button_font.render(
            "BACK TO MENU", True, BACKGROUND
        )

        screen.blit(
            back_text,
            (
                back_button.centerx - back_text.get_width() // 2,
                back_button.centery - back_text.get_height() // 2
            )
        )

        pygame.display.flip()
        clock.tick(60)

    return "main_menu"
