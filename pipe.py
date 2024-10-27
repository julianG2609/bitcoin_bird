import pygame
import random


SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720

class Pipe:
    def __init__(self, speed):
        # Load and scale separate images for the top and bottom pipes
        self.top_image = pygame.image.load("static/top_pipe.png")
        self.bottom_image = pygame.image.load("static/bottom_pipe.png")

        self.width = int(SCREEN_WIDTH * 0.15)  # 10% of screen width for the pipe width
        self.gap = int(SCREEN_HEIGHT * 0.25)  # 25% of screen height for the gap between pipes

        # Scale the images based on the desired width and their original aspect ratios
        self.top_height = self.top_image.get_height()
        self.scaled_top_image = pygame.transform.scale(self.top_image, (self.width, self.top_height))

        self.bottom_height = self.bottom_image.get_height()
        self.scaled_bottom_image = pygame.transform.scale(self.bottom_image, (self.width, self.bottom_height))

        self.x = SCREEN_WIDTH
        self.speed = speed  # Set initial pipe speed

        # Set random top height and calculate bottom height dynamically
        self.top_height = random.randint(50, SCREEN_HEIGHT - self.gap - 50)
        self.bottom_height = SCREEN_HEIGHT - self.top_height - self.gap
        self.passed = False  # To check if the pipe has been passed by the player for scoring

    def update(self):
        self.x -= self.speed  # Move the pipes left based on the current speed

    def get_rects(self):
        """Returns the bounding rectangles of the top and bottom pipes."""
        top_rect = pygame.Rect(self.x, 0, self.width, self.top_height - 15)
        bottom_rect = pygame.Rect(self.x, SCREEN_HEIGHT - self.bottom_height, self.width, self.bottom_height - 25)
        return top_rect, bottom_rect

    def render(self, screen):
        # Draw the top pipe image
        top_pipe_rect = pygame.Rect(self.x, self.top_height - self.scaled_top_image.get_height(), self.width, self.scaled_top_image.get_height())
        screen.blit(self.scaled_top_image, top_pipe_rect)

        # Draw the bottom pipe image
        bottom_pipe_rect = pygame.Rect(self.x, SCREEN_HEIGHT - self.bottom_height, self.width, self.scaled_bottom_image.get_height())
        screen.blit(self.scaled_bottom_image, bottom_pipe_rect)
