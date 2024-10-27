import pygame

SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720

def load_custom_font(size):
    try:
        return pygame.font.Font("static/Ubuntu-BoldItalic.ttf", size)
    except:
        return pygame.font.Font(None, size)

def draw_glowing_text(screen, text, font, x, y, glow_color, text_color, glow_radius=5):
    """Draws glowing text with a shadow/glow effect."""
    # Render the base text
    text_surface = font.render(text, True, text_color)

    # Draw the glow effect by rendering the text multiple times with an offset
    for i in range(glow_radius, 0, -1):
        glow_surface = font.render(text, True, glow_color)
        glow_surface.set_alpha(0.4)
        screen.blit(glow_surface, (x - i, y - i))
        screen.blit(glow_surface, (x + i, y - i))
        screen.blit(glow_surface, (x - i, y + i))
        screen.blit(glow_surface, (x + i, y + i))

    # Draw the main text on top of the glow
    screen.blit(text_surface, (x, y))


def display_score(screen, score, font, animation_factor=1.0):
    """Displays the score with a stylish look and animation."""
    score_text = f"Wallet: {score}.00 BTC"
    text_color = (255, 255, 255)  # Gold color for the score
    glow_color = (0, 0, 0)  # White glow

    # Create the glowing and animated score text
    text_surface = font.render(score_text, True, text_color)
    text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, 50))

    # Apply scaling animation to make the score grow when updated
    if animation_factor != 1.0:
        scaled_surface = pygame.transform.smoothscale(text_surface,
                                                      (int(text_rect.width * animation_factor),
                                                       int(text_rect.height * animation_factor)))
        text_rect = scaled_surface.get_rect(center=text_rect.center)
        screen.blit(scaled_surface, text_rect.topleft)
    else:
        draw_glowing_text(screen, score_text, font, text_rect.x, text_rect.y, glow_color, text_color)
