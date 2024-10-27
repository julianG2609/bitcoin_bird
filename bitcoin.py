import pygame
import random
from wind_particle import WindParticle

SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
pygame.mixer.init()
flap_sound = pygame.mixer.Sound("static/flapp.wav")  # Make sure you have this file
class Bitcoin:
    def __init__(self):
        # Load and scale the Bitcoin images for both rising, neutral, and falling states
        self.rising_image = pygame.image.load("static/bird_rising.png").convert_alpha()
        self.falling_image = pygame.image.load("static/bird_falling.png").convert_alpha()
        self.neutral_image = pygame.image.load("static/bird.png").convert_alpha()

        # Scale all images proportionally
        scaled_width = int(SCREEN_WIDTH * 0.075)
        scaled_height = int(scaled_width * self.rising_image.get_height() / self.rising_image.get_width())
        self.rising_image = pygame.transform.smoothscale(self.rising_image, (scaled_width, scaled_height))
        self.falling_image = pygame.transform.smoothscale(self.falling_image, (scaled_width, scaled_height))
        self.neutral_image = pygame.transform.smoothscale(self.neutral_image, (scaled_width, scaled_height))

        # Set initial state and position
        self.image = self.neutral_image
        self.x = 50
        self.y = SCREEN_HEIGHT // 2
        self.gravity = 0.6
        self.lift = -8
        self.velocity = 0

        # Wind particles list
        self.wind_particles = []

        # Track history for motion blur effect
        self.history = []

        # Variables to track the state
        self.last_jump_time = None
        self.state_duration = 0.5  # 0.5 seconds duration for rising and neutral states

    def update(self):
        self.velocity += self.gravity
        self.y += self.velocity

        # Update history for motion blur
        if len(self.history) > 3:  # Reduce the number of blur copies for subtlety
            self.history.pop(0)
        self.history.append((self.x, self.y, self.velocity))

        # Generate wind particles based on bird movement
        if self.velocity < 0:  # If the bird is moving upwards, stronger wind
            self.wind_particles.append(WindParticle(self.x - 20, self.y + self.image.get_height() // 2))
        else:
            if random.random() < 0.3:  # Add fewer particles when falling
                self.wind_particles.append(WindParticle(self.x - 20, self.y + self.image.get_height() // 2))

        # Update each wind particle
        for particle in self.wind_particles:
            particle.update(speed_factor=self.velocity)

        # Remove particles that have shrunk too small
        self.wind_particles = [p for p in self.wind_particles if p.size > 0]

        # Get the current time
        current_time = pygame.time.get_ticks() / 1000  # Time in seconds

        if self.velocity < 0:
            if self.last_jump_time and current_time - self.last_jump_time < self.state_duration:
                self.image = self.rising_image
            elif self.last_jump_time and current_time - self.last_jump_time < 2 * self.state_duration:
                self.image = self.neutral_image
        else:
            self.image = self.falling_image

    def jump(self):
        self.velocity = self.lift
        self.last_jump_time = pygame.time.get_ticks() / 1000  # Record the jump time in seconds
        flap_sound.play()

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())

    def render(self, screen):
        # Render motion blur effect
        for i, (hx, hy, hvelocity) in enumerate(self.history[:-1]):
            # Calculate decreasing alpha for each older position
            alpha = int(100 * (i / len(self.history)))  # Lower the alpha for more subtlety
            temp_image = pygame.transform.scale(self.image, (int(self.image.get_width() * 1.1), self.image.get_height()))
            temp_image.set_alpha(alpha)
            screen.blit(temp_image, (hx - 25, hy))  # Draw even further behind the bird

        # Render the wind particles
        for particle in self.wind_particles:
            particle.render(screen)

        # Determine the rotation angle based on the velocity
        if self.velocity < 0:
            angle = max(30, self.velocity * 3)
        else:
            angle = min(-30, self.velocity * 3)

        # Rotate the image based on the calculated angle
        rotated_image = pygame.transform.rotate(self.image, angle)
        rotated_rect = rotated_image.get_rect(center=(self.x + self.image.get_width() // 2, self.y + self.image.get_height() // 2))

        # Render the rotated image on the screen
        screen.blit(rotated_image, rotated_rect.topleft)

