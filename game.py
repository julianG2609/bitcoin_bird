import pygame
import random

# Screen settings
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720

# Initialize Pygame and the sound mixer
pygame.init()
pygame.mixer.init()

# Load the Bitconnect sound effect
bitconnect_sound = pygame.mixer.Sound("static/bitconnect.wav")  # Make sure you have this file

class Bitcoin:
    def __init__(self):
        # Load and scale the Bitcoin images for both rising, neutral, and falling states
        self.rising_image = pygame.image.load("static/bird_rising.png").convert_alpha()
        self.falling_image = pygame.image.load("static/bird_falling.png").convert_alpha()
        self.neutral_image = pygame.image.load("static/bird.png").convert_alpha()

        # Scale all images proportionally
        scaled_width = int(SCREEN_WIDTH * 0.065)
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

        # Variables to track the state
        self.last_jump_time = None
        self.state_duration = 0.5  # 0.5 seconds duration for rising and neutral states

    def update(self):
        self.velocity += self.gravity
        self.y += self.velocity

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

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())

    def render(self, screen):
        if self.velocity < 0:
            angle = max(30, self.velocity * 3)
        else:
            angle = min(-30, self.velocity * 3)

        rotated_image = pygame.transform.rotate(self.image, angle)
        rotated_rect = rotated_image.get_rect(center=(self.x + self.image.get_width() // 2, self.y + self.image.get_height() // 2))
        screen.blit(rotated_image, rotated_rect.topleft)



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
        top_rect = pygame.Rect(self.x, 0, self.width, self.top_height)
        bottom_rect = pygame.Rect(self.x, SCREEN_HEIGHT - self.bottom_height, self.width, self.bottom_height)
        return top_rect, bottom_rect

    def render(self, screen):
        # Draw the top pipe image
        top_pipe_rect = pygame.Rect(self.x, self.top_height - self.scaled_top_image.get_height(), self.width, self.scaled_top_image.get_height())
        screen.blit(self.scaled_top_image, top_pipe_rect)

        # Draw the bottom pipe image
        bottom_pipe_rect = pygame.Rect(self.x, SCREEN_HEIGHT - self.bottom_height, self.width, self.scaled_bottom_image.get_height())
        screen.blit(self.scaled_bottom_image, bottom_pipe_rect)

class Background:
    def __init__(self, speed):
        # Load and scale the background image to fit the screen size
        self.image = pygame.image.load("static/background.png")
        self.image = pygame.transform.scale(self.image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.x1 = 0  # Initial position of the first image
        self.x2 = SCREEN_WIDTH  # Initial position of the second image for looping
        self.speed = speed * 1.1  # Set background speed 10% faster than initial speed

    def update(self, pipe_speed):
        # Update the background speed to be 10% faster than the pipe speed
        self.speed = pipe_speed * 1.1

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


def reset_game(initial_speed):
    """Resets the game and returns a new Bitcoin, pipes, and initial score."""
    bitcoin = Bitcoin()
    pipes = [Pipe(initial_speed)]
    score = 0
    return bitcoin, pipes, score

def game_over_screen(screen, font, score, best_score):
    """Displays the game over screen with the current and best score, and waits for a key press to restart."""
    screen.fill((0, 0, 0))  # Clear the screen with a black background

    # Display "Game Over"
    game_over_text = font.render("Game Over", True, (255, 0, 0))
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 4))

    # Display the current score
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))

    # Display the best score
    best_score_text = font.render(f"Best Score: {best_score}", True, (255, 255, 255))
    screen.blit(best_score_text, (SCREEN_WIDTH // 2 - best_score_text.get_width() // 2, SCREEN_HEIGHT // 2))

    # Display "Press SPACE to Restart"
    restart_text = font.render("Press SPACE to Restart", True, (255, 255, 255))
    screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))

    pygame.display.flip()

    # Wait for the player to press the SPACE key to restart
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False

def main_game():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 54)

    base_speed = 3
    speed_increase_factor = 1.4
    current_speed = base_speed

    background = Background(current_speed)
    bitcoin, pipes, score = reset_game(current_speed)
    best_score = 0

    # Play the Bitconnect sound at the start of the game
    bitconnect_sound.set_volume(0.05)
    bitconnect_sound.play(1000)


    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bitcoin.jump()

        bitcoin.update()
        background.update(current_speed)

        if pipes[-1].x < SCREEN_WIDTH - 500:
            pipes.append(Pipe(current_speed))

        for pipe in pipes:
            pipe.update()

        pipes = [pipe for pipe in pipes if pipe.x + pipe.width > 0]

        bitcoin_rect = bitcoin.get_rect()
        collision = False
        for pipe in pipes:
            top_rect, bottom_rect = pipe.get_rects()
            if bitcoin_rect.colliderect(top_rect) or bitcoin_rect.colliderect(bottom_rect):
                collision = True

        for pipe in pipes:
            if not pipe.passed and pipe.x + pipe.width < bitcoin.x:
                score += 1
                pipe.passed = True

        if score % 15 == 0 and score != 0:
            if current_speed == base_speed or score % 15 == 0:
                current_speed = base_speed * (speed_increase_factor ** (score // 15))

        if bitcoin.y < 0 or bitcoin.y > SCREEN_HEIGHT or collision:
            if score > best_score:
                best_score = score
            game_over_screen(screen, font, score, best_score)
            current_speed = base_speed
            bitcoin, pipes, score = reset_game(current_speed)

        background.render(screen)
        bitcoin.render(screen)
        for pipe in pipes:
            pipe.render(screen)

        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (20, 20))

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
