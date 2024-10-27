import pygame
import random


SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720

class LightingEffect:
    def __init__(self):
        """Create a lighting effect overlay with a gradient."""
        self.overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        self.create_gradient()
        self.flicker_intensity = 0  # Variable to simulate dynamic lighting

    def create_gradient(self):
        """Create a radial gradient effect on the overlay surface."""
        center_x, center_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        max_radius = max(SCREEN_WIDTH, SCREEN_HEIGHT)

        for i in range(max_radius):
            alpha = max(0, 255 - (i // 2))  # Gradient effect
            color = (30, 30, 30, alpha)  # Dark gray with variable alpha
            pygame.draw.circle(self.overlay, color, (center_x, center_y), i)

    def update(self):
        """Update the overlay effect to simulate flickering."""
        self.flicker_intensity = random.randint(-10, 10)

    def render(self, screen):
        """Render the overlay with dynamic lighting effects on the screen."""
        # Apply flickering effect by modifying the alpha value
        flicker_alpha = max(0, min(255, 150 + self.flicker_intensity))
        self.overlay.set_alpha(flicker_alpha)
        screen.blit(self.overlay, (0, 0))
