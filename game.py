import pygame
import random

# Screen settings
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720

# Initialize Pygame and the sound mixer
pygame.init()
pygame.mixer.init()

bitconnect_sound = pygame.mixer.Sound("static/bitconnect.wav")  # Make sure you have this file
cash_sound = pygame.mixer.Sound("static/cash.wav")  # Make sure you have this file
flap_sound = pygame.mixer.Sound("static/flapp.wav")  # Make sure you have this file

# Set sound volumes
bitconnect_sound.set_volume(0.05)
cash_sound.set_volume(0.18)  # Adjust the volume for the cash sound if necessary
flap_sound.set_volume(0.3)  # Adjust the volume for the flap sound

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
    score_text = font.render(f"Wallet: {score} BTC", True, (255, 255, 255))
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))

    # Display the best score
    best_score_text = font.render(f"Most BTC mined: {best_score} BTC", True, (255, 255, 255))
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


def load_custom_font(size):
    """Loads a custom font from the static folder."""
    try:
        # Load a custom font. Make sure you have 'cool_font.ttf' in your 'static' folder.
        return pygame.font.Font("static/Ubuntu-BoldItalic.ttf", size)
    except:
        # Fallback to default font if the custom font is not found
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



def main_game():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    # Load a custom font
    font = load_custom_font(54)  # Adjust font size as needed

    base_speed = 3
    speed_increase_factor = 1.4
    current_speed = base_speed

    background = Background(current_speed)
    bitcoin, pipes, score = reset_game(current_speed)
    best_score = 0

    # Variables for score animation
    score_animation_time = 0
    score_animation_factor = 1.0

    # List to store floating bitcoins
    floating_bitcoins = []

    # Play the Bitconnect sound at the start of the game
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
        background.update(current_speed, bitcoin.velocity)

        if pipes[-1].x < SCREEN_WIDTH - 500:
            pipes.append(Pipe(current_speed))

        for pipe in pipes:
            pipe.update()

        pipes = [pipe for pipe in pipes if pipe.x + pipe.width > 0]

        bitcoin_rect = bitcoin.get_rect()
        collision = False
        for pipe in pipes:
            top_rect, bottom_rect = pipe.get_rects()
            pipe_midpoint_x = pipe.x + (pipe.width // 2)  # Calculate midpoint of the pipe width

            # Check for collisions if the bird's x position is near the midpoint of the pipe
            if bitcoin_rect.colliderect(top_rect) or bitcoin_rect.colliderect(bottom_rect):
                collision = True

            # Update score if the bird has passed the midpoint of the pipe and hasn't already scored for it
            if not pipe.passed and bitcoin.x > pipe_midpoint_x:
                score += 1
                pipe.passed = True
                # Play cash sound when the score increases
                cash_sound.play()
                # Trigger score animation
                score_animation_time = pygame.time.get_ticks()
                score_animation_factor = 1.3

                # Add a floating Bitcoin image above the bird
                floating_bitcoin = FloatingBitcoin(bitcoin.x, bitcoin.y - 20)
                floating_bitcoins.append(floating_bitcoin)

        # Animate score text for 0.3 seconds when it increases
        if pygame.time.get_ticks() - score_animation_time < 300:
            score_animation_factor = 1.3 - ((pygame.time.get_ticks() - score_animation_time) / 300) * 0.3
        else:
            score_animation_factor = 1.0

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

        # Update and render floating bitcoins
        for fb in floating_bitcoins[:]:
            fb.update()
            if fb.is_expired():
                floating_bitcoins.remove(fb)
            else:
                fb.render(screen)

        # Display the animated, glowing score
        display_score(screen, score, font, score_animation_factor)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

