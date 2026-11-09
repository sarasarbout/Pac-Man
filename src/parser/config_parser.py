from dataclasses import dataclass, field, fields
from typing import Any
import json
import os


class ConfigError(Exception):
    """Custom exception for configuration errors."""
    pass


@dataclass
class GameConfig:
    """Store validated configuration values for the game."""
    screen_width: int = 1000
    screen_height: int = 1000

    highscore_filename: str = "highscores.json"
    lives: int = 3

    points_per_pacgum: int = 10
    points_per_super_pacgum: int = 50
    points_per_ghost: int = 200
    levels: list[dict[str, Any]] = field(default_factory=lambda: [
        {"width": 21, "height": 17, "pacgum": 42, "seed": 42},
        {"width": 23, "height": 17, "pacgum": 48, "seed": 0},
        {"width": 25, "height": 19, "pacgum": 54, "seed": 0},
        {"width": 25, "height": 19, "pacgum": 55, "seed": 0},
        {"width": 27, "height": 21, "pacgum": 60, "seed": 0},
        {"width": 29, "height": 21, "pacgum": 66, "seed": 0},
        {"width": 31, "height": 23, "pacgum": 72, "seed": 0},
        {"width": 31, "height": 23, "pacgum": 73, "seed": 0},
        {"width": 33, "height": 25, "pacgum": 78, "seed": 0},
        {"width": 35, "height": 25, "pacgum": 84, "seed": 0},
    ])


class ConfigParser:
    """Load, clean, validate and convert the configuration."""

    def __init__(self, config_path: str) -> None:
        self.config_data = self.load_config(config_path)

    def _read_file(self, path: str) -> str:
        """Read the configuration file."""

        if not path.endswith(".json"):
            raise ConfigError(
                f"Configuration file must have a .json extension: '{path}'"
            )

        if not os.path.exists(path):
            raise ConfigError(f"Configuration file not found: '{path}'")

        if not os.path.isfile(path):
            raise ConfigError(f"Expected a file, got a directory: '{path}'")

        try:
            with open(path, "r", encoding="utf-8") as file:
                content = file.read()
        except PermissionError as error:
            raise ConfigError(
                f"Permission denied: '{path}'"
            ) from error
        except UnicodeDecodeError as error:
            raise ConfigError(
                f"Configuration file is not valid UTF-8: '{path}'"
            ) from error
        except OSError as error:
            raise ConfigError(
                f"Could not read configuration file: '{path}'"
            ) from error

        if not content.strip():
            raise ConfigError("Configuration file is empty")

        return content

    def _remove_comments(self, content: str) -> str:
        """Remove lines beginning with # from the configuration."""

        cleaned_lines = []

        for line in content.splitlines():
            stripped = line.strip()

            if stripped.startswith("#"):
                continue

            cleaned_lines.append(line)

        return "\n".join(cleaned_lines)

    def _decode_json(self, content: str) -> dict[str, Any]:
        """Convert cleaned JSON text into a Python dictionary."""

        try:
            data = json.loads(content)
        except json.JSONDecodeError as error:
            raise ConfigError(
                f"Invalid JSON at line {error.lineno}, "
                f"column {error.colno}: {error.msg}"
            ) from error

        if not isinstance(data, dict):
            raise ConfigError(
                "Configuration must contain a JSON object"
            )

        return data

    def _normalize_keys(self, data: Any) -> Any:
        """Convert all configuration dictionary keys to lowercase."""

        if isinstance(data, dict):
            normalized = {}

            for key, value in data.items():
                new_key = key.lower()

                if new_key in normalized:
                    raise ConfigError(
                        f"Duplicate configuration key: '{key}'"
                    )

                normalized[new_key] = self._normalize_keys(value)

            return normalized

        if isinstance(data, list):
            return [self._normalize_keys(item) for item in data]

        return data

    def _check_keys(self, data: dict[str, Any]) -> None:
        """Warn about unknown configuration keys."""

        known_keys = {item.name for item in fields(GameConfig)}

        for key in data:
            if key.lower() not in known_keys:
                print(
                    f"Warning: unknown configuration key '{key}' "
                    f"will be ignored."
                )

    def _parse_string(
        self,
        data: dict[str, Any],
        key: str,
        default: str
    ) -> str:
        """Validate a string configuration value."""

        value = data.get(key)

        if not isinstance(value, str) or not value.strip():
            print(
                f"Warning: '{key}' is invalid. "
                f"Using default: {default}"
            )
            return default

        return value

    def _parse_integer(
        self,
        data: dict[str, Any],
        key: str,
        default: int,
        minimum: int = 0
    ) -> int:
        """Validate an integer configuration value."""

        value = data.get(key)

        # bool is technically an int in python
        # We do not want True/False accepted as configuration integers
        if (
            not isinstance(value, int)
            or isinstance(value, bool)
            or value < minimum
        ):
            print(
                f"Warning: '{key}' is invalid. "
                f"Using default: {default}"
            )
            return default

        return value

    def _parse_level(
        self,
        level_data: dict[str, Any],
        index: int
    ) -> dict[str, Any]:
        """Validate one level configuration."""

        default_width = 21
        default_height = 17
        default_pacgum = 42

        if not isinstance(level_data, dict):
            print(
                f"Warning: level[{index}] is not an object. "
                f"Skipping it."
            )
            return {}

        width = level_data.get("width")
        height = level_data.get("height")
        pacgum = level_data.get("pacgum")
        seed = level_data.get("seed")

        name = level_data.get("name", f"Level {index + 1}")

        if not isinstance(name, str) or not name.strip():
            print(
                f"Warning: level[{index}] 'name' is invalid. "
                f"Using default: Level {index + 1}"
            )
            name = f"Level {index + 1}"
        if (
            not isinstance(width, int)
            or isinstance(width, bool)
            or width < 5
        ):
            print(
                f"Warning: level[{index}] 'width' is invalid. "
                f"Using default: {default_width}"
            )
            width = default_width

        if (
            not isinstance(height, int)
            or isinstance(height, bool)
            or height < 5
        ):
            print(
                f"Warning: level[{index}] 'height' is invalid. "
                f"Using default: {default_height}"
            )
            height = default_height

        if (
            not isinstance(pacgum, int)
            or isinstance(pacgum, bool)
            or pacgum < 1
        ):
            print(
                f"Warning: level[{index}] 'pacgum' is invalid. "
                f"Using default: {default_pacgum}"
            )
            pacgum = default_pacgum

        if seed is not None and (
            not isinstance(seed, int)
            or isinstance(seed, bool)
        ):
            print(
                f"Warning: level[{index}] 'seed' is invalid. "
                f"Using random seed."
            )
            seed = None
        time = level_data.get("time", 90)

        if (
            not isinstance(time, int)
            or isinstance(time, bool)
            or time < 1
        ):
            print(
                f"Warning: level[{index}] 'time' is invalid. "
                f"Using default: 90"
            )
            time = 90
        return {
            "name": name,
            "width": width,
            "height": height,
            "pacgum": pacgum,
            "seed": seed,
            "time": time
        }

    def _parse_levels(
        self,
        data: dict[str, Any],
        default_levels: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        """Validate the complete levels configuration."""

        levels = data.get("levels")

        if levels is None:
            print(
                "Warning: 'levels' is missing. "
                "Using default levels."
            )
            return default_levels

        if not isinstance(levels, list) or not levels:
            print(
                "Warning: 'levels' is invalid. "
                "Using default levels."
            )
            return default_levels

        parsed_levels = []

        for index, level in enumerate(levels):
            parsed_level = self._parse_level(level, index)

            if parsed_level:
                parsed_levels.append(parsed_level)

        if not parsed_levels:
            print(
                "Warning: no valid levels found. "
                "Using default levels."
            )
            return default_levels

        if parsed_levels[0]["seed"] is None:
            print(
                "Warning: first level has no fixed seed. "
                "Using seed 42."
            )
            parsed_levels[0]["seed"] = 42
        return parsed_levels

    def _build_config(self, data: dict[str, Any]) -> GameConfig:
        """Build a validated GameConfig object."""

        default = GameConfig()
        return GameConfig(
            screen_height=self._parse_integer(
                data,
                "screen_height",
                default.screen_height,
                minimum=400),
            screen_width=self._parse_integer(
                data,
                "screen_width",
                default.screen_width,
                minimum=600
            ),
            highscore_filename=self._parse_string(
                data,
                "highscore_filename",
                default.highscore_filename
            ),
            lives=self._parse_integer(
                data,
                "lives",
                default.lives,
                minimum=1
            ),

            points_per_pacgum=self._parse_integer(
                data,
                "points_per_pacgum",
                default.points_per_pacgum,
                minimum=0
            ),

            points_per_super_pacgum=self._parse_integer(
                data,
                "points_per_super_pacgum",
                default.points_per_super_pacgum,
                minimum=0
            ),

            points_per_ghost=self._parse_integer(
                data,
                "points_per_ghost",
                default.points_per_ghost,
                minimum=0
            ),

            levels=self._parse_levels(
                data,
                default.levels
            )
        )

    def load_config(self, path: str) -> GameConfig:
        """Load and validate the complete configuration."""

        content = self._read_file(path)

        content = self._remove_comments(content)

        data = self._decode_json(content)
        data = self._normalize_keys(data)

        self._check_keys(data)

        return self._build_config(data)
