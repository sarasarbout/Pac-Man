*This project has been created as part of the 42 curriculum by sasarbou, iait-mou.*

# Pacman Ghosts! More ghosts!

## Description

Pacman Ghosts! More ghosts! is a Python game built with Pygame and the A-Maze-ing maze-generation package. Guide Pac-Man through a generated maze, collect Pac-Gums, avoid four ghosts, and try to finish each level before time runs out. Super Pac-Gums temporarily make the ghosts vulnerable, and eating them earns bonus points.

The project combines a configurable multi-level game, maze and character rendering, several ghost movement behaviors, sound effects, a heads-up display, menus, and a persistent high-score table.

## Features

- Ten configurable levels with different maze sizes and objectives.
- Keyboard-controlled Pac-Man, animated sprites, and four ghosts.
- Ghost behaviors that include pathfinding, random movement, and fleeing.
- Normal and super Pac-Gums, score, lives, and level timers.
- Pause, instructions, high-score, victory, game-over, and cheat menus.
- Sound effects and music.
- High scores saved locally in JSON.

## Instructions

Run these commands from the repository root:

```bash
make install
make run
```

`make install` creates the `.venv`, extracts the bundled A-Maze-ing wheel from `mazegenerator-00001.zip`, and installs the packages listed in `requirements.txt`. `make run` launches the game using `src/config.json`. To select another JSON file, run `.venv/bin/python pac-man.py path/to/config.json`.

The command-line entry point requires exactly one JSON config path. For example:

```bash
python3 pac-man.py src/config.json
```

To check static types:

```bash
cd src
../.venv/bin/mypy . --explicit-package-bases --warn-return-any \
  --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs \
  --check-untyped-defs
```

### Build a Linux release

From the repository root on a Linux machine, run:

```bash
make install
.venv/bin/python -m pip install pyinstaller
rm -rf build dist Pacman-Ghosts-linux Pacman-Ghosts-linux.zip
.venv/bin/pyinstaller --clean --noconfirm --windowed \
  --paths . \
  --name "Pacman Ghosts" \
  --add-data "assets:assets" \
  --add-data "src/config.json:." \
  pac-man.py
mv "dist/Pacman Ghosts" Pacman-Ghosts-linux
zip -r Pacman-Ghosts-linux.zip Pacman-Ghosts-linux
```

This rebuilds the PyInstaller Linux application bundle from the current source, then packages it as `Pacman-Ghosts-linux.zip` for distribution. The packaged executable uses the bundled config when opened directly; you can pass another config path to override it. This bundle is for Linux.

### Controls

| Action | Controls |
| --- | --- |
| Move Pac-Man | Arrow keys or W, A, S, D |
| Pause | Space or Escape |
| Open the cheat menu | F1 |
| Return from an information/menu screen | Escape or its on-screen button |

## Configuration

The game reads [`src/config.json`](./src/config.json). It is a JSON object with game-wide settings and a `levels` array. Each level specifies its name, maze width and height in cells, number of normal Pac-Gums, maze seed, and time limit in seconds.

The checked-in configuration uses these defaults:

| Setting | Default | Description |
| --- | ---: | --- |
| `highscore_filename` | `highscores.json` | High-score data file, resolved from the repository root. |
| `lives` | `3` | Starting lives. |
| `screen_width` | `1000` | Initial window width in pixels. |
| `screen_height` | `1000` | Initial window height in pixels. |
| `level_max_time` | `90` | General level-time setting. Individual levels have their own `time`. |
| `points_per_pacgum` | `10` | Points for a normal Pac-Gum. |
| `points_per_super_pacgum` | `50` | Points for a super Pac-Gum. |
| `points_per_ghost` | `200` | Points for eating a frightened ghost. |

The level-specific defaults are:

| Level | Maze size (width × height) | Pac-Gums | Seed | Time (seconds) |
| --- | ---: | ---: | ---: | ---: |
| 1 | 10 × 10 | 5 | 42 | 90 |
| 2 | 15 × 15 | 8 | 0 | 180 |
| 3 | 20 × 21 | 13 | 0 | 200 |
| 4 | 25 × 25 | 16 | 0 | 250 |
| 5 | 30 × 30 | 19 | 0 | 300 |
| 6 | 35 × 35 | 23 | 0 | 350 |
| 7 | 39 × 39 | 26 | 0 | 400 |
| 8 | 42 × 42 | 30 | 0 | 450 |
| 9 | 45 × 45 | 33 | 0 | 500 |
| 10 | 20 × 20 | 8 | 0 | 550 |

The configuration parser validates values and falls back to `GameConfig` defaults for invalid or missing settings. Keep the file valid JSON; full-line comments beginning with `#` are also ignored by the parser.

## Highscore

Scores are stored in the JSON file configured by `highscore_filename` (by default, `highscores.json` in the project root). After a game ends or is won, the player can enter a name of up to ten alphanumeric characters or spaces. The shared high-score module validates names and non-negative integer scores, sorts records from highest to lowest, and saves only the top ten entries. The high-score screen loads and displays those records.

JSON keeps the data human-readable and easy to edit without adding a database dependency. Keeping the file local also means scores remain available between runs without requiring a network connection.

## Maze Generation

Each level is generated with the bundled A-Maze-ing package. The game passes the configured dimensions, seed, and `perfect=False` option to `MazeGenerator`, then uses the generated grid to build its `Maze` model.

The grid encodes each cell's north, east, south, and west walls as bit flags. The renderer uses those flags to draw the maze, and the same cell data is used by movement and pathfinding to decide whether a direction is passable. The seed is a level setting, so a level can be configured to reproduce a generated layout.

## Implementation

The game is implemented in Python with Pygame for window management, input, drawing, fonts, and audio. Pac-Man and ghosts are modeled on a cell grid while their sprites are drawn in screen coordinates. Pac-Man's movement is constrained by maze walls; ghost behaviors include A*-style pathfinding, random legal moves, and selecting moves that increase their distance from Pac-Man when frightened.

Maze generation and drawing are separate: the A-Maze-ing package provides the grid, model and drawing code interpret it, and Pygame renders the maze, characters, collectibles, HUD, and screens. Game screens return state names to the controller, which coordinates transitions between menus and gameplay.

## General Software Architecture

- `pac-man.py` is the command-line entry point; it requires a JSON config path and delegates to `src/main.py`.
- `src/main.py` loads configuration, initializes Pygame, opens the window, and starts the controller.
- `src/model/highscores.py` validates and stores the top ten high scores for both victory and game-over screens.
- `src/parser/config_parser.py` defines `GameConfig` and validates the JSON configuration.
- `src/model/` contains the core data types: `Maze` and `Cell`, `Position`, `Direction`, `Pacman`, `Ghost`, `Pacgum`, and `GameStatus`.
- `src/draw/` creates levels, draws the maze and collectibles, renders Pac-Man and ghosts, processes gameplay input, and updates movement.
- `src/ui/` contains the state controller, HUD, menus, instructions, high-score screen, and victory/game-over screens.
- `assets/` contains character sprites, backgrounds, the logo, and sound files.

The controller calls the active screen or gameplay loop and uses the returned state to decide what to show next. The model supplies grid positions and game state to the drawing and movement code; the parser supplies settings to both.


## Resources

- [Pygame documentation](https://www.pygame.org/docs/) — graphics, events, display, and audio APIs.
- [Python documentation](https://docs.python.org/3/) — language and standard-library reference.
- [Red Blob Games: A* introduction](https://www.redblobgames.com/pathfinding/a-star/introduction.html) — explanation of grid pathfinding and the A* algorithm.
- A-Maze-ing — the maze-generation package supplied for the project and integrated through `MazeGenerator`.

### Use of AI

AI assistance was used to identify and resolve mypy errors with type annotations, and to help organize and write this README. The type-checking work preserves the existing gameplay algorithms and state flow; the AI was not used to create the game's sprites or audio assets.

# Project Management

We divided the game work between two contributors and integrated the gameplay, menus, and assets into one project. See the [project-management notes](project-management/README.md) for responsibilities, progress, and review records.


