from dataclasses import dataclass
from enum import Enum


class Difficulty(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class GameMode(str, Enum):
    NORMAL = "normal"
    TIMER = "timer"
    TIMER_BONUS = "timer_bonus"
    TASKS = "tasks"


@dataclass
class SessionOptions:
    duration_sec: int | None = None
    target_tasks: int | None = None
    initial_time_sec: int | None = None
    bonus_sec: int | None = None


SCHEMA_VERSION = 1
APP_VERSION = '0.3'
MAX_SESSIONS = 5000
STATS_FILENAME = "stats.json"
APP_DATA_SUBDIR = "numo"
RECENT_GAMES = 10

SCHEMA_ID = "io.github.Nu_nik_kak_nik.Numo"
RESOURCE_PATH_PREFIX = "/io/github/Nu_nik_kak_nik/Numo"

