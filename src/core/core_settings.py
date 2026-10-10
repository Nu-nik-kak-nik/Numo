from dataclasses import dataclass
from enum import Enum

from numo.game.task import Operation


SCHEMA_VERSION = 1
APP_VERSION = '0.4'
MAX_SESSIONS = 5000
STATS_FILENAME = "stats.json"
APP_DATA_SUBDIR = "numo"
RECENT_GAMES = 10

SCHEMA_ID = "io.github.Nu_nik_kak_nik.Numo"
RESOURCE_PATH_PREFIX = "/io/github/Nu_nik_kak_nik/Numo"


class Difficulty(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class GameMode(str, Enum):
    NORMAL = "normal"
    TIMER = "timer"
    TIMER_BONUS = "timer_bonus"
    TASKS = "tasks"


@dataclass(frozen=True, slots=True)
class SessionOptions:
    duration_sec: int | None = None
    target_tasks: int | None = None
    initial_time_sec: int | None = None
    bonus_sec: int | None = None


@dataclass(frozen=True, slots=True)
class AddSubRange:
    min_first: int
    max_first: int
    min_second: int
    max_second: int
    keep_non_negative: bool = False


@dataclass(frozen=True, slots=True)
class MultiplicationRange:
    min_first: int
    max_first: int
    min_second: int
    max_second: int


@dataclass(frozen=True, slots=True)
class DivisionRange:
    min_divisor: int
    max_divisor: int
    min_quotient: int
    max_quotient: int


@dataclass(frozen=True, slots=True)
class DivModRange:
    min_divisor: int
    max_divisor: int
    min_base: int
    max_base: int
    min_remainder: int = 1


@dataclass(frozen=True, slots=True)
class DifficultySettings:
    operations: tuple[Operation, ...]
    add_sub: AddSubRange | None = None
    multiplication: MultiplicationRange | None = None
    division: DivisionRange | None = None
    div_mod: DivModRange | None = None


DIFFICULTY_SETTINGS: dict[Difficulty, DifficultySettings] = {
    Difficulty.EASY: DifficultySettings(
        operations=(Operation.ADD, Operation.SUB),
        add_sub=AddSubRange(
            min_first=1, max_first=50,
            min_second=1, max_second=50,
            keep_non_negative=True,
        ),
    ),

    Difficulty.MEDIUM: DifficultySettings(
        operations=(
            Operation.ADD, Operation.SUB,
            Operation.MUL, Operation.DIV,
        ),
        add_sub=AddSubRange(
            min_first=5, max_first=99,
            min_second=5, max_second=99,
        ),
        multiplication=MultiplicationRange(
            min_first=2, max_first=14,
            min_second=2, max_second=14,
        ),
        division=DivisionRange(
            min_divisor=2, max_divisor=15,
            min_quotient=2, max_quotient=20,
        ),
    ),

    Difficulty.HARD: DifficultySettings(
        operations=(
            Operation.ADD, Operation.SUB,
            Operation.MUL, Operation.DIV,
            Operation.FLOOR_DIV, Operation.MOD,
        ),
        add_sub=AddSubRange(
            min_first=-200, max_first=200,
            min_second=-200, max_second=200,
        ),
        multiplication=MultiplicationRange(
            min_first=-20, max_first=20,
            min_second=-20, max_second=20,
        ),
        division=DivisionRange(
            min_divisor=3, max_divisor=25,
            min_quotient=3, max_quotient=25,
        ),
        div_mod=DivModRange(
            min_divisor=3, max_divisor=25,
            min_base=3, max_base=25,
            min_remainder=1,
        ),
    ),
}


