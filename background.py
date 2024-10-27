import pygame


SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720

class Background:
    def __init__(self, speed):
        # Load and scale the background image to fit the screen size
        self.image = pygame.image.load("static/background.png")
        self.image = pygame.transform.scale(self.image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.x1 = 0  # Initial position of the first image
        self.x2 = SCREEN_WIDTH  # Initial position of the second image for looping
        self.speed = speed * 1.1  # Set background speed 10% faster than initial speed

    def update(self, pipe_speed, bird_speed):
        # Update the background speed to be 10% faster than the pipe speed + some factor of bird speed
        self.speed = pipe_speed * 1.2 + abs(bird_speed) * 0.05

        # Move both background images to the left
        self.x1 -= self.speed
        self.x2 -= self.speed

        # Reset the positions to create a seamless loop
        if self.x1 <= -SCREEN_WIDTH:
            self.x1 = SCREEN_WIDTH
        if self.x2 <= -SCREEN_WIDTH:
            self.x2 = SCREEN_WIDTH

    def render(self, screen):
        # Draw both images to create the looping effect
        screen.blit(self.image, (self.x1, 0))
        screen.blit(self.image, (self.x2, 0))
