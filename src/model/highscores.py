"""Load, validate, and save the game's persistent high scores."""

import json
from pathlib import Path
from typing import TypeGuard, TypedDict

from src.parser.config_parser import GameConfig


MAX_PLAYER_NAME_LENGTH = 10
MAX_HIGH_SCORES = 10
PROJECT_ROOT = Path(__file__).resolve().parents[2]


class ScoreEntry(TypedDict):
    """One validated high-score record."""

    name: str
    score: int


def is_valid_player_name(name: str) -> bool:
    """Return whether a name follows the game's high-score name rules."""
    cleaned_name = name.strip()
    return (
        bool(cleaned_name)
        and len(cleaned_name) <= MAX_PLAYER_NAME_LENGTH
        and all(
            character.isalnum() or character == " "
            for character in cleaned_name
        )
    )


def _is_valid_score(score: object) -> TypeGuard[int]:
    """Return whether a score is a non-negative integer, excluding bools."""
    return (
        isinstance(score, int)
        and not isinstance(score, bool)
        and score >= 0
    )


def _score_path(config: GameConfig) -> Path:
    """Resolve the configured score filename relative to the project root."""
    filename = Path(config.highscore_filename)
    if filename.is_absolute():
        return filename
    return PROJECT_ROOT / filename


def _validated_scores(data: object) -> list[ScoreEntry]:
    """Keep only valid records and return the ten highest scores."""
    if not isinstance(data, list):
        return []

    scores: list[ScoreEntry] = []
    for entry in data:
        if not isinstance(entry, dict):
            continue
        name = entry.get("name")
        score = entry.get("score")
        if (
            isinstance(name, str)
            and is_valid_player_name(name)
            and _is_valid_score(score)
        ):
            scores.append({"name": name.strip(), "score": score})

    return sorted(scores, key=lambda entry: entry["score"], reverse=True)[
        :MAX_HIGH_SCORES
    ]


def load_scores(config: GameConfig) -> list[ScoreEntry]:
    """Load valid high scores, returning an empty list for unreadable data."""
    filename = _score_path(config)
    try:
        with filename.open("r", encoding="utf-8") as score_file:
            return _validated_scores(json.load(score_file))
    except (OSError, json.JSONDecodeError):
        return []


def save_score(
    config: GameConfig,
    player_name: str,
    final_score: int,
) -> None:
    """Validate and save a player's score, retaining only the top ten."""
    cleaned_name = player_name.strip()
    if not is_valid_player_name(cleaned_name):
        raise ValueError(
            "Player name must be 1 to 10 alphanumeric characters or spaces."
        )
    if not _is_valid_score(final_score):
        raise ValueError("Score must be a non-negative integer.")

    filename = _score_path(config)
    try:
        with filename.open("r", encoding="utf-8") as score_file:
            existing_data = json.load(score_file)
    except FileNotFoundError:
        existing_data = []
    except json.JSONDecodeError:
        existing_data = []

    scores = _validated_scores(existing_data)
    scores.append({"name": cleaned_name, "score": final_score})
    scores.sort(key=lambda entry: entry["score"], reverse=True)
    scores = scores[:MAX_HIGH_SCORES]

    filename.parent.mkdir(parents=True, exist_ok=True)
    with filename.open("w", encoding="utf-8") as score_file:
        json.dump(scores, score_file, indent=4, ensure_ascii=False)
