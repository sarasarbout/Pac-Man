import pygame
from typing import TypedDict


CheatState = TypedDict(
    "CheatState",
    {
        "Invincibility": bool,
        "Freeze Ghosts": bool,
        "Speed Boost": bool,
        "Speed Multiplier": float,
    },
    total=False,
)


def update_speed_multiplier(
    mouse_x: int, slider_rect: pygame.Rect, cheats: CheatState
) -> None:
    relative_x = mouse_x - slider_rect.left

    ratio = relative_x / slider_rect.width
    ratio = max(0, min(1, ratio))

    multiplier = 1 + (ratio * 2)

    cheats["Speed Multiplier"] = round(multiplier, 1)


def draw_toggle(
    screen: pygame.Surface,
    rect: pygame.Rect,
    label: str,
    enabled: bool,
    font: pygame.font.Font,
) -> None:

    pygame.draw.rect(
        screen, (20, 20, 43), rect, border_radius=8
    )

    text = font.render(label, True, (255, 255, 255))
    screen.blit(text, (rect.x + 15, rect.y + 12))

    switch = pygame.Rect(
        rect.right - 75, rect.y + 8, 60, 30
    )
    color = (40, 200, 120) if enabled else (90, 90, 110)
    pygame.draw.rect(
        screen, color, switch, border_radius=15
    )

    knob_x = switch.right - 15 if enabled else switch.left + 15
    pygame.draw.circle(
        screen, (255, 255, 255),
        (knob_x, switch.centery), 11
    )


def cheat_menu(
    screen: pygame.Surface, cheats: CheatState
) -> tuple[str, CheatState]:
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 30)
    title_font = pygame.font.Font(None, 48)

    WIDTH = screen.get_width()
    HEIGHT = screen.get_height()

    button_width = min(600, WIDTH - 60)
    button_height = 50
    button_x = (WIDTH - button_width) // 2

    invincible_rect = pygame.Rect(
        button_x, int(HEIGHT * 0.25), button_width, button_height
    )
    freeze_rect = pygame.Rect(
        button_x, int(HEIGHT * 0.35), button_width, button_height
    )
    skip_level_rect = pygame.Rect(
        button_x, int(HEIGHT * 0.45), button_width, button_height
    )
    speed_rect = pygame.Rect(
        button_x, int(HEIGHT * 0.55), button_width, button_height
    )

    slider_rect = pygame.Rect(
        button_x,
        int(HEIGHT * 0.65),
        button_width - 40,
        6
    )
    dragging_slider = False
    cheats.setdefault("Speed Multiplier", 1.5)

    resume_rect = pygame.Rect(
        (WIDTH - 300) // 2,
        int(HEIGHT * 0.75),
        300,
        button_height
    )

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit", cheats

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "resume", cheats

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                if invincible_rect.collidepoint(event.pos):
                    cheats["Invincibility"] = not cheats["Invincibility"]
                elif freeze_rect.collidepoint(event.pos):
                    cheats["Freeze Ghosts"] = not cheats["Freeze Ghosts"]
                elif speed_rect.collidepoint(event.pos):
                    cheats["Speed Boost"] = not cheats["Speed Boost"]
                elif skip_level_rect.collidepoint(event.pos):
                    return "skip_level", cheats

                elif resume_rect.collidepoint(event.pos):
                    return "resume", cheats

                elif (
                        cheats["Speed Boost"]
                        and slider_rect.inflate(0, 25).collidepoint(event.pos)
                ):
                    dragging_slider = True
                    update_speed_multiplier(event.pos[0], slider_rect, cheats)

            if event.type == pygame.MOUSEMOTION and dragging_slider:
                update_speed_multiplier(event.pos[0], slider_rect, cheats)

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                dragging_slider = False

        screen.fill((8, 8, 23))

        title = title_font.render(
            "CHEAT MODE", True, (255, 230, 0)
        )

        screen.blit(
            title,
            title.get_rect(center=(WIDTH // 2, int(HEIGHT * 0.15)))
        )

        draw_toggle(
            screen,
            invincible_rect,
            "Invincibility",
            cheats["Invincibility"],
            font
        )
        draw_toggle(
            screen,
            freeze_rect,
            "Freeze Ghosts",
            cheats["Freeze Ghosts"],
            font
        )
        draw_toggle(
            screen,
            speed_rect,
            "Speed Boost",
            cheats["Speed Boost"],
            font
        )

        if cheats["Speed Boost"]:
            multiplier_text = font.render(
                f"Speed: {cheats['Speed Multiplier']:.1f}x",
                True,
                (255, 255, 255)
            )

            screen.blit(
                multiplier_text,
                multiplier_text.get_rect(
                    center=(WIDTH // 2, slider_rect.y - 20)
                )
            )

            pygame.draw.rect(
                screen,
                (90, 90, 110),
                slider_rect,
                border_radius=5
            )

            # Calculate knob position
            ratio = (cheats["Speed Multiplier"] - 1) / 2
            knob_x = slider_rect.left + int(ratio * slider_rect.width)

            # Slider knob
            pygame.draw.circle(
                screen,
                (255, 230, 0),
                (knob_x, slider_rect.centery),
                10
            )

        pygame.draw.rect(
            screen,
            (20, 20, 43),
            skip_level_rect,
            border_radius=10
        )

        skip_text = font.render(
            "Skip Level", True, (255, 255, 255)
        )

        screen.blit(
            skip_text,
            (skip_level_rect.x + 15, skip_level_rect.y + 12)
        )

        pygame.draw.rect(
            screen,
            (20, 20, 43),
            skip_level_rect,
            border_radius=10
        )

        skip_text = font.render(
            "Skip Level", True, (255, 255, 255)
        )

        screen.blit(
            skip_text,
            (skip_level_rect.x + 15, skip_level_rect.y + 12)
        )

        arrow_x = skip_level_rect.right - 45
        arrow_y = skip_level_rect.centery

        pygame.draw.polygon(
            screen,
            (255, 255, 255),
            [
                (arrow_x - 8, arrow_y - 10),
                (arrow_x + 5, arrow_y),
                (arrow_x - 8, arrow_y + 10)
            ]
        )

        pygame.draw.rect(
            screen, (53, 53, 255), resume_rect, border_radius=8
        )

        resume_text = font.render(
            "RESUME GAME", True, (255, 255, 255)
        )

        screen.blit(
            resume_text,
            resume_text.get_rect(center=resume_rect.center)
        )

        pygame.display.flip()
        clock.tick(60)
