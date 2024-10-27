import unittest
import pygame
from bitcoin import Bitcoin
from pipe import Pipe
from background import Background
from floating_bitcoin import FloatingBitcoin
from project import *

SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720

class TestBitcoin(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.bitcoin = Bitcoin()

    def tearDown(self):
        pygame.quit()

class TestPipe(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.pipe = Pipe(speed=5)

    def tearDown(self):
        pygame.quit()

    def test_pipe_movement(self):
        initial_x = self.pipe.x
        self.pipe.update()
        self.assertLess(self.pipe.x, initial_x)  # Pipe should move to the left

    def test_pipe_off_screen(self):
        self.pipe.x = -self.pipe.width  # Simulate moving pipe completely off-screen
        self.pipe.update()
        self.assertLess(self.pipe.x, 0)  # Ensure it moves past 0 and is reset elsewhere in the game

class TestBackground(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.background = Background(speed=3)

    def tearDown(self):
        pygame.quit()

class TestFloatingBitcoin(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.floating_bitcoin = FloatingBitcoin(100, 200)

    def tearDown(self):
        pygame.quit()


class TestGameOverScreen(unittest.TestCase):

    def setUp(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        self.font = pygame.font.Font(None, 54)  # Use default font for testing

    def tearDown(self):
        pygame.quit()

    def test_game_over_screen(self):
        # Arrange: Set up the initial values for the score and best score
        score = 10
        best_score = 20

        # Act: Call the game_over_screen function
        try:
            game_over_screen(self.screen, self.font, score, best_score)
            success = True
        except Exception as e:
            success = False
            print(f"Error occurred: {e}")

        # Assert: Ensure the screen was updated without errors
        self.assertTrue(success)


class TestResetGame(unittest.TestCase):

    def setUp(self):
        # Setup any necessary initial conditions
        self.initial_speed = 5

    def test_reset_game_returns_correct_objects(self):
        # Act: Call the reset_game function
        bitcoin, pipes, score = reset_game(self.initial_speed)

        # Assert: Check if the returned objects are of the correct types
        self.assertIsInstance(bitcoin, Bitcoin)
        self.assertIsInstance(pipes, list)
        self.assertGreater(len(pipes), 0)
        self.assertIsInstance(pipes[0], Pipe)
        self.assertEqual(score, 0)

    def test_reset_game_initializes_pipe_with_correct_speed(self):
        # Act: Call the reset_game function
        bitcoin, pipes, _ = reset_game(self.initial_speed)

        # Assert: Check if the pipe's speed matches the initial speed
        self.assertEqual(pipes[0].speed, self.initial_speed)


if __name__ == '__main__':
    unittest.main()
