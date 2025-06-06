# Tetris Game in Python

A simple implementation of the classic Tetris game using Python and Pygame, with an additional upside-down mode for an added challenge.

## Description

This project is a fully functional Tetris game with all the standard features of the classic game plus a unique upside-down mode. The game is built with Python using the Pygame library for graphics and user interactions.

## Features

- Classic Tetris gameplay
- Upside-down mode where pieces rise from the bottom
- Score tracking with level progression
- Next piece preview
- Increasing difficulty as you level up

## Requirements

- Python 3.x
- Pygame library

## Installation

1. Ensure you have Python installed on your system
2. Install Pygame if you don't have it already:

```bash
pip install pygame
```

3. Clone or download this repository
4. Navigate to the project directory and run the game:

```bash
python main.py
```

## How to Play

### Regular Mode
- **Left/Right Arrow Keys**: Move the piece horizontally
- **Down Arrow Key**: Move the piece down faster (soft drop)
- **Up Arrow Key**: Rotate the piece
- **Spacebar**: Hard drop (instantly drops the piece to the bottom)
- **P Key**: Pause/Resume game
- **R Key**: Restart game (when game over)
- **Esc Key**: Quit game

### Upside-Down Mode
- **Left/Right Arrow Keys**: Move the piece horizontally
- **Up Arrow Key**: Move the piece upward
- **Down Arrow Key**: Rotate the piece
- **Spacebar**: Hard drop (instantly moves the piece to the top)
- **P Key**: Pause/Resume game
- **R Key**: Restart game (when game over)
- **Esc Key**: Quit game

## Project Structure

- `main.py`: The entry point for the game, handles the game loop and user input
- `tetris.py`: Contains the main game logic and mechanics
- `tetromino.py`: Defines the Tetromino class and the shapes of the tetromino pieces
- `colors.py`: Defines the colors used throughout the game

## Scoring

- Points are awarded for completing lines
- Clearing multiple lines at once gives a multiplier bonus
- Level increases after every 10 lines cleared
- Game speed increases with each level

## Acknowledgements

This game is inspired by the classic Tetris game created by Alexey Pajitnov in 1984.

## License

Feel free to use, modify, and distribute this code for personal and educational purposes.

## Future Enhancements

Some potential features to add in the future:
- High score tracking
- Different game modes (e.g., marathon, sprint)
- Sound effects and music
- Customizable controls
- Multiplayer mode
