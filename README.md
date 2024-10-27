
<img src="static/bitcoin.png" alt="Gameplay Screenshot" width="250"/>

# Bitcoin Bird Game

#### Video Demo:  https://youtu.be/G-_m9q0EqyY
#### Description

Bitcoin Bird is a 2D side-scrolling game inspired by the classic Flappy Bird. In this game, you control a Bitcoin Bird, and the objective is to navigate through a series of obstacles while accumulating BTC. The game includes dynamic lighting effects, wind particles, and a stylish score display. As you play, the bird generates wind trails and floating Bitcoin coins appear when you score, adding to the game's visual appeal. This game was programmed as final project for the Harvard CS50P course.

## Table of Contents
- [Description](#description)
- [Table of Contents](#table-of-contents)
- [Features](#features)
- [Installation](#installation)
- [Gameplay Instructions](#gameplay-instructions)
- [File Structure](#file-structure)
- [Tests](#tests)
- [Dependencies](#dependencies)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Smooth Gameplay:** Control the bird with the space key to make it jump and avoid obstacles.
- **Dynamic Visuals:** Motion blur, particle effects, and dynamic lighting to make the game visually interesting.
- **Stylish Scoring:** Earn points by passing through pipes, accompanied by special effects and sounds.
- **Floating Bitcoin Rewards:** Bitcoin icons float up whenever you score.
- **Tests:** A suite of test functions using `pytest` to ensure the game's core functions work correctly.

## Installation

### Prerequisites
- **Python 3.12**
- **Pygame library**

### Steps to Install

1. **Clone the Repository:**
   ```bash
   git clone <repository_url>
   cd bitcoin_bird_game
   ```

2. **Install Dependencies:**
   Install the necessary dependencies listed in the `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Game:**
   ```bash
   python project.py
   ```

## Gameplay Instructions

1. Press **SPACE** to make the bird jump.
2. Navigate through pipes to earn points.
3. Avoid colliding with the pipes to keep playing.
4. The game gets harder as the bird gains speed after every 15 points.

## File Structure

```
.
|── background.py          # Contains the Background class
|── bitcoin.py             # Contains the Bitcoin (Bird) class
|── floating_bitcoin.py    # Contains the FloatingBitcoin class
|── game.py                # Contains the main_game logic and game loop
|── lighting_effect.py     # Contains the LightingEffect class
|── pipe.py                # Contains the Pipe class for creating obstacles
|── project.py             # Main entry point for the game
|── test_project.py        # Contains test cases for the game's core functions
|── utils.py               # Contains utility functions and helper classes
|── wind_particle.py       # Contains WindParticle class for visual effects
|── static/                # Folder containing image and sound assets
    ├── bird.png
    ├── bird_rising.png
    ├── bird_falling.png
    ├── top_pipe.png
    ├── bottom_pipe.png
    ├── bitcoin.png
    ├── background.png
    ├── flapp.wav
    ├── bitconnect.wav
    ├── cash.wav
    ├── Ubuntu-BoldItalic.ttf
```

## Tests

### Running Tests
Tests are included to verify the core functions of the game. The test cases are written in `test_project.py` using the `pytest` framework.

1. **To run all tests**, simply run the following command:
   ```bash
   pytest test_project.py
   ```

## Dependencies

The game relies on the following dependencies, which are listed in `requirements.txt`:

- **Pygame 2.1.2**
- **Pytest 7.4.2**
## Visual Assets
The bird, bitcoin, background and pipe textures were created using Dalle 2 https://openai.com/index/dall-e-2/.
## Sound and Music
The music used was generated with the use of https://www.udio.com/.
The sound effects were generated with the use of https://elevenlabs.io/app/sound-effects/generate.
