# Cubes 2048 Clone

This repository contains a small offline clone of **Cubes 2048.io** implemented with Pygame. The game combines the mechanics of Snake and 2048. Control your cube snake with the mouse, collect cubes and merge matching numbers to grow.

## Setup
1. Ensure Python 3.8+ is installed.
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. (Optional) Generate placeholder assets:
```bash
python -m src.generate_assets
```
4. Run the game:
```bash
python -m src.main
```

## Controls
- Move the mouse to steer the snake.
- Hold the left mouse button to boost.
- Press **R** after losing to restart.

## Project Structure
```
Cubes2048_Clone/
  assets/
    images/       # cube sprites
    sounds/       # (empty placeholder)
  src/
    config.py
    main.py
    objects.py
    snake.py
    generate_assets.py
  requirements.txt
  README.md
```
