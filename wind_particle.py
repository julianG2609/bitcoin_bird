import pygame
import random


class WindParticle:
    def __init__(self, x, y):
        """Initialize a wind particle at a given position."""
        self.x = x
        self.y = y + random.randint(-2, 2)  # Slight random vertical offset for variation
        self.size = random.randint(2, 4)  # Make particles a bit smaller for more detail
        self.color = (255, 255, 255)  # White color for wind effect, you can customize it
        self.speed = random.uniform(4, 6)  # Increase the horizontal speed of particles
        self.lifetime = random.randint(30, 60)  # How long the particle will last

    def update(self, speed_factor=0):
        """Update the position and size of the wind particle."""
        self.x -= self.speed + abs(speed_factor) * 0.15  # Move the particle more horizontally
        self.y += random.uniform(-0.2, 0.2)  # Slight random vertical movement to add variation
        self.lifetime -= 1  # Decrease lifetime as the particle moves
        if self.lifetime < 0:
            self.size -= 0.1  # Shrink the particle

    def render(self, screen):
        """Render the wind particle on the screen."""
        if self.size > 0:  # Only draw if the particle still has a size
            pygame.draw.ellipse(screen, self.color, (int(self.x), int(self.y), int(self.size) * 2, int(self.size)))  # Draw elongated ellipse

