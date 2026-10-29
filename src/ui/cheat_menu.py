import pygame

def draw_toggle(screen, rect, label, enabled, font):


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

def cheat_menu(screen):
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 30)
    title_font = pygame.font.Font(None, 48)

    cheats = {
        "Invincibility": False,
        "Freeze Ghosts": False,
        "Speed Boost": False,        
        }

    
    invincible_rect = pygame.Rect(300, 200, 600, 50)
    freeze_rect = pygame.Rect(300, 270, 600, 50)
    speed_rect = pygame.Rect(300, 340, 600, 50)
    resume_rect = pygame.Rect(450, 450, 300, 50)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit", cheats

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "resume", cheats

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if invincible_rect.collidepoint(event.pos):
                        cheats["Invincibility"] = not cheats["Invincibility"]

                    elif speed_rect.collidepoint(event.pos):
                        cheats["Speed Boost"] = not cheats["Speed Boost"]

                    elif freeze_rect.collidepoint(event.pos):
                        cheats["Freeze Ghosts"] = not cheats["Freeze Ghosts"]

                    elif resume_rect.collidepoint(event.pos):
                        return "resume", cheats
        screen.fill((8, 8, 23))

        title = title_font.render(
            "CHEAT MODE", True, (255, 230, 0)
        )

        screen.blit(
            title,
            title.get_rect(center=(screen.get_width() // 2, 120))
        )

        draw_toggle(
            screen,
            invincible_rect,
            "Invinsibility",
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
            




if __name__ == "__main__":
    pygame.init()

    screen = pygame.display.set_mode((1200, 800))
    pygame.display.set_caption("Pac-Man Cheat Mode")

    action, cheats = cheat_menu(screen)

    pygame.quit()