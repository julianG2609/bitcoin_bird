from bitcoin import Bitcoin
from pipe import Pipe
from floating_bitcoin import FloatingBitcoin
from background import Background
from utils import *


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

