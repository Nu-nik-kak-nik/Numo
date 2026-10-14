from dataclasses import dataclass
from enum import Enum

from numo.core.custom_errors import InvalidRangeError
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
class AdditionRange:
    min_first: int
    max_first: int
    min_second: int
    max_second: int
    keep_non_negative: bool = False

    def __post_init__(self) -> None:
        validate_range(self.min_first, self.max_first, "AdditionRange first")
        validate_range(self.min_second, self.max_second, "AdditionRange second")


@dataclass(frozen=True, slots=True)
class SubtractionRange:
    min_first: int
    max_first: int
    min_second: int
    max_second: int
    keep_non_negative: bool = False

    def __post_init__(self) -> None:
        validate_range(self.min_first, self.max_first, "SubtractionRange first")
        validate_range(self.min_second, self.max_second, "SubtractionRange second")


@dataclass(frozen=True, slots=True)
class MultiplicationRange:
    min_first: int
    max_first: int
    min_second: int
    max_second: int

    def __post_init__(self) -> None:
        validate_range(self.min_first, self.max_first, "MultiplicationRange first")
        validate_range(self.min_second, self.max_second, "MultiplicationRange second")


@dataclass(frozen=True, slots=True)
class DivisionRange:
    min_divisor: int
    max_divisor: int
    min_quotient: int
    max_quotient: int

    def __post_init__(self) -> None:
        validate_range(self.min_divisor, self.max_divisor, "DivisionRange divisor")
        validate_range(self.min_quotient, self.max_quotient, "DivisionRange quotient")


@dataclass(frozen=True, slots=True)
class IntDivRange:
    min_divisor: int
    max_divisor: int
    min_base: int
    max_base: int
    min_remainder: int = 0

    def __post_init__(self) -> None:
        validate_range(self.min_divisor, self.max_divisor, "IntDivRange divisor")
        validate_range(self.min_base, self.max_base, "IntDivRange base")
        validate_remainder(self.min_divisor, self.min_remainder, "IntDivRange")


@dataclass(frozen=True, slots=True)
class ModRange:
    min_divisor: int
    max_divisor: int
    min_base: int
    max_base: int
    min_remainder: int = 0

    def __post_init__(self) -> None:
        validate_range(self.min_divisor, self.max_divisor, "ModRange divisor")
        validate_range(self.min_base, self.max_base, "ModRange base")
        validate_remainder(self.min_divisor, self.min_remainder, "ModRange")


def validate_range(minimum: int, maximum: int, field_name: str) -> None:
    if minimum > maximum:
        raise InvalidRangeError(
            f"Invalid {field_name} range: "
            f"minimum ({minimum}) is greater than maximum ({maximum})"
        )

def validate_remainder(min_divisor: int, min_remainder: int, range_name: str) -> None:
    if min_divisor <= min_remainder:
        raise InvalidRangeError(
            f"{range_name}: minimum divisor ({min_divisor}) "
            f"must be greater than minimum remainder ({min_remainder})"
        )


@dataclass(frozen=True, slots=True)
class DifficultySettings:
    operations: tuple[Operation, ...]
    addition: AdditionRange | None = None
    subtraction: SubtractionRange | None = None
    multiplication: MultiplicationRange | None = None
    division: DivisionRange | None = None
    integer_division: IntDivRange | None = None
    mod: ModRange | None = None

    def __post_init__(self) -> None:
        if not self.operations:
            raise ValueError("At least one operation must be enabled")



DIFFICULTY_SETTINGS: dict[Difficulty, DifficultySettings] = {
    Difficulty.EASY: DifficultySettings(
        operations=(Operation.ADD, Operation.SUB, Operation.MUL,),

        addition = AdditionRange(
            min_first=1, max_first=50,
            min_second=1, max_second=50,
        ),
        subtraction = SubtractionRange(
            min_first=1, max_first=50,
            min_second=1, max_second=50,
            keep_non_negative=True,
        ),
        multiplication=MultiplicationRange(
            min_first=1, max_first=5,
            min_second=1, max_second=5,
        ),
    ),

    Difficulty.MEDIUM: DifficultySettings(
        operations=(
            Operation.ADD, Operation.SUB,
            Operation.MUL, Operation.DIV,
        ),

        addition=AdditionRange(
            min_first=-100, max_first=100,
            min_second=-100, max_second=100,
        ),
        subtraction=SubtractionRange(
            min_first=-100, max_first=100,
            min_second=-100, max_second=100,
        ),
        multiplication=MultiplicationRange(
            min_first=2, max_first=12,
            min_second=2, max_second=12,
        ),
        division=DivisionRange(
            min_divisor=-12, max_divisor=12,
            min_quotient=-12, max_quotient=12,
        ),
    ),

    Difficulty.HARD: DifficultySettings(
        operations=(
            Operation.ADD, Operation.SUB,
            Operation.MUL, Operation.DIV,
            Operation.INTEGER_DIV, Operation.MOD,
        ),

        addition=AdditionRange(
            min_first=-200, max_first=200,
            min_second=-200, max_second=200,
        ),
        subtraction=SubtractionRange(
            min_first=-200, max_first=200,
            min_second=-200, max_second=200,
        ),
        multiplication=MultiplicationRange(
            min_first=-20, max_first=20,
            min_second=-20, max_second=20,
        ),
        division=DivisionRange(
            min_divisor=-20, max_divisor=20,
            min_quotient=-20, max_quotient=20,
        ),
        integer_division=IntDivRange(
            min_divisor=3, max_divisor=20,
            min_base=3, max_base=20,
            min_remainder=1,
        ),
        mod=ModRange(
            min_divisor=3, max_divisor=20,
            min_base=3, max_base=20,
            min_remainder=1,
        ),
    ),
}


