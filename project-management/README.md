# Project Management

## Team responsibilities

The project was developed collaboratively, with responsibilities divided between me and my teammate to allow parallel development and easier integration.

| Contributor | Work |
|---|---|
| sasarbou | Maze generation, Pac-Man and ghost visuals, Pac-Gum drawing, movement behaviors for two ghosts, and sound integration. |
| iait-mou | Movement behaviors for the other two ghosts, game menus, cheat mode, configuration parsing, and game flow integration. |

We both participated in integrating our work, debugging issues, and testing the overall game.

## Planning and progress

We organized development into several phases, starting with the core gameplay mechanics before moving on to the user interface and additional features.

Tasks were divided according to each contributor's responsibilities. We coordinated through discussions and used Git and GitHub to share code, review changes, track contributions, and resolve merge conflicts.

| Milestone | Work completed | Status or evidence |
|---|---|---|
| Core game | Maze generation, Pac-Man movement, ghost behaviors, Pac-Gum collection, and collision detection. | Implemented. See the `src/` directory and Git commit history. |
| Game flow | Main menu, instructions, pause menu, HUD, cheat menu, game-over screen, and victory screen. | Implemented. See the `src/ui/` directory. |
| Scoring system | Score calculation, player name input, high-score saving, and leaderboard display. | Implemented. See the high-score and game-over modules. |
| Configuration | JSON configuration file, validation, default values, and support for multiple levels. | Implemented. See `src/parser/` and `src/config.json`. |
| Release preparation | Linux packaging and preparation of the downloadable game archive. | Linux ZIP tested by the team. |

## Acceptance review

The main features we reviewed before considering the project complete.

| Feature | Result | Notes |
|---|---|---|
| Game starts with the supplied configuration | Passed | the game loads the configuration correctly. |
| Pac-Man movement and wall collisions | Passed | Verified that movement in all directions and collision with walls. |
| Ghost movement and collisions | Passed | Verified ghost behaviors and collision effects. |
| Pac-Gums, scoring, and level progression | Passed | Verified score updates and progression between levels. |
| Cheat mode and pause menu | Passed | Verified cheat options and the ability to resume gameplay. |
| High-score entry and persistence | Passed | Verified that player names and scores are saved and displayed correctly. |
| Linux package launches after extraction | Passed | ZIP tested by the team. |

## Decisions and issues

### Maze generation

We used the assigned A-Maze-ing package for maze generation rather than implementing the entire generation algorithm ourselves. This allowed us to focus more on gameplay mechanics and integration.

### Configuration management

We used a JSON configuration file to centralize game settings, including screen dimensions, lives, scoring values, and level information. We implemented validation and default values to handle missing or invalid configuration entries.

### Game architecture

We separated the project into modules for models, drawing, user interface, and configuration parsing. This made responsibilities clearer and allowed different features to be developed independently.

### Game flow

We used a controller to manage transitions between the main menu, gameplay, pause menu, game-over screen, and victory screen. The same Pac-Man instance is maintained throughout level progression to preserve the player's score and remaining lives.

### Version control and integration

We used Git and GitHub to collaborate, share changes, and integrate the work of both contributors. Merge conflicts were resolved during integration to keep the project consistent.

### Linux packaging

We prepared a Linux ZIP archive containing the packaged game and tested it after extraction to verify that it could be launched.