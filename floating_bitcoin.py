import pygame


SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720

class FloatingBitcoin:
    def __init__(self, x, y):
        """Initialize the floating Bitcoin image."""
        self.image = pygame.image.load("static/bitcoin.png").convert_alpha()
        scaled_width = int(SCREEN_WIDTH * 0.045)
        scaled_height = int(scaled_width * self.image.get_height() / self.image.get_width())
        self.image = pygame.transform.smoothscale(self.image, (scaled_width, scaled_height))

        self.x = x
        self.y = y - 40
        self.start_time = pygame.time.get_ticks()  # Record the start time
        self.duration = 1000  # Duration in milliseconds (1 second)
        self.alpha = 255  # Initial alpha value for full opacity

    def update(self):
        """Move the floating Bitcoin image upwards and decrease alpha for fade effect."""
        self.y -= 2  # Move the image upwards

        # Calculate the fade-out effect based on time
        elapsed_time = pygame.time.get_ticks() - self.start_time
        if elapsed_time > self.duration:
            self.alpha = 0
        else:
            self.alpha = max(0, 255 - int((elapsed_time / self.duration) * 255))

    def is_expired(self):
        """Check if the floating Bitcoin should disappear."""
        return self.alpha == 0

    def render(self, screen):
        """Render the floating Bitcoin on the screen with fading effect."""
        if self.alpha > 0:
            faded_image = self.image.copy()
            faded_image.set_alpha(self.alpha)
            screen.blit(faded_image, (self.x, self.y))
