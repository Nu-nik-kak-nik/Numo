import gi

gi.require_version("Gio", "2.0")

from gi.repository import Gio, GObject

from numo.core.core_settings import (
    Difficulty,
    GameMode,
    SessionOptions,
    SCHEMA_ID
)
from numo.game.task import Operation


class SettingsManager:
    def __init__(self):
        self._settings = Gio.Settings.new(SCHEMA_ID)

    @property
    def settings(self) -> Gio.Settings:
        return self._settings

    def get_difficulty(self) -> Difficulty:
        return Difficulty(self._settings.get_string("difficulty"))

    def set_difficulty(self, difficulty: Difficulty) -> None:
        self._settings.set_string("difficulty", difficulty.value)

    def get_timer_duration_min(self) -> int:
        return self._settings.get_int("timer-duration-min")

    def set_timer_duration_min(self, value: int) -> None:
        self._settings.set_int("timer-duration-min", value)

    def get_bonus_initial_sec(self) -> int:
        return self._settings.get_int("bonus-initial-sec")

    def set_bonus_initial_sec(self, value: int) -> None:
        self._settings.set_int("bonus-initial-sec", value)

    def get_bonus_per_correct_sec(self) -> int:
        return self._settings.get_int("bonus-per-correct-sec")

    def set_bonus_per_correct_sec(self, value: int) -> None:
        self._settings.set_int("bonus-per-correct-sec", value)

    def get_tasks_count(self) -> int:
        return self._settings.get_int("tasks-count")

    def set_tasks_count(self, value: int) -> None:
        self._settings.set_int("tasks-count", value)

    def session_options_for(self, mode: GameMode) -> SessionOptions:
        if mode == GameMode.TIMER:
            return SessionOptions(
                duration_sec=self.get_timer_duration_min() * 60,
            )
        if mode == GameMode.TIMER_BONUS:
            return SessionOptions(
                initial_time_sec=self.get_bonus_initial_sec(),
                bonus_sec=self.get_bonus_per_correct_sec(),
            )
        if mode == GameMode.TASKS:
            return SessionOptions(
                target_tasks=self.get_tasks_count(),
            )
        return SessionOptions()

    def get_recent_sessions(self) -> int:
        return self._settings.get_int("recent-sessions")

    def set_recent_sessions(self, value: int) -> None:
        self._settings.set_int("recent-sessions", value)

    def get_custom_add_enabled(self) -> bool:
        return self._settings.get_boolean("custom-add-enabled")

    def set_custom_add_enabled(self, value: bool) -> None:
        self._settings.set_boolean("custom-add-enabled", value)

    def get_custom_sub_enabled(self) -> bool:
        return self._settings.get_boolen("custom-sub-enabled")

    def set_custom_sub_enabled(self, value: bool) -> None:
        self._settings.set_boolean("custom-sub-enabled", value)

    def get_custom_mul_enabled(self) -> bool:
        return self._settings.get_boolen("custom-mul-enabled")

    def set_custom_mul_enabled(self, value: bool) -> None:
        self._settings.set_boolean("custom-mul-enabled", value)

    def get_custom_div_enabled(self) -> bool:
        return self._settings.get_boolen("custom-div-enabled")

    def set_custom_div_enabled(self, value: bool) -> None:
        self._settings.set_boolean("custom-div-enabled", value)

    def get_custom_intdiv_enabled(self) -> bool:
        return self._settings.get_boolen("custom-intdiv-enabled")

    def set_custom_intdiv_enabled(self, value: bool) -> None:
        self._settings.set_boolean("custom-intdiv-enabled", value)

    def get_custom_mod_enabled(self) -> bool:
        return self._settings.get_boolen("custom-mod-enabled")

    def set_custom_mod_enabled(self, value: bool) -> None:
        self._settings.set_boolean("custom-mod-enabled", value)

    def get_custom_sub_non_negative(self) -> bool:
        return self._settings.get_boolean("custom-sub-non-negative")

    def set_custom_sub_non_negative(self, value: bool) -> None:
        self._settings.set_boolean("custom-sub-non-negative", value)

    def get_custom_add_range(self) -> tuple[int, int]:
        return (
            self._settings.get_int("custom-add-min"),
            self._settings.get_int("custom-add-max"),
        )

    def set_custom_add_range(self, min_val: int, max_val: int) -> None:
        self._settings.set_int("custom-add-min", min_val)
        self._settings.set_int("custom-add-max", max_val)

    def get_custom_sub_range(self) -> tuple[int, int]:
        return (
            self._settings.get_int("custom-sub-min"),
            self._settings.get_int("custom-sub-max"),
        )

    def set_custom_sub_range(self, min_val: int, max_val: int) -> None:
        self._settings.set_int("custom-sub-min", min_val)
        self._settings.set_int("custom-sub-max", max_val)

    def get_custom_mul_range(self) -> tuple[int, int]:
        return (
            self._settings.get_int("custom-mul-min"),
            self._settings.get_int("custom-mul-max"),
        )

    def set_custom_mul_range(self, min_val: int, max_val: int) -> None:
        self._settings.set_int("custom-mul-min", min_val)
        self._settings.set_int("custom-mul-max", max_val)

    def get_custom_div_range(self) -> tuple[int, int]:
        return (
            self._settings.get_int("custom-div-min"),
            self._settings.get_int("custom-div-max"),
        )

    def set_custom_div_range(self, min_val: int, max_val: int) -> None:
        self._settings.set_int("custom-div-min", min_val)
        self._settings.set_int("custom-div-max", max_val)

    def get_custom_intdiv_range(self) -> tuple[int, int]:
        return (
            self._settings.get_int("custom-intdiv-min"),
            self._settings.get_int("custom-intdiv-max"),
        )

    def set_custom_intdiv_range(self, min_val: int, max_val: int) -> None:
        self._settings.set_int("custom-intdiv-min", min_val)
        self._settings.set_int("custom-intdiv-max", max_val)

    def get_custom_mod_range(self) -> tuple[int, int]:
        return (
            self._settings.get_int("custom-mod-min"),
            self._settings.get_int("custom-mod-max"),
        )

    def set_custom_mod_range(self, min_val: int, max_val: int) -> None:
        self._settings.set_int("custom-mod-min", min_val)
        self._settings.set_int("custom-mod-max", max_val)

    def reset_custom_to_medium(self) -> None:
        self.set_custom_add_enabled(True)
        self.set_custom_sub_enabled(True)
        self.set_custom_mul_enabled(True)
        self.set_custom_div_enabled(True)
        self.set_custom_intdiv_enabled(False)
        self.set_custom_mod_enabled(False)

        self.set_custom_sub_non_negative(False)

        self.set_custom_add_range(-100, 100)
        self.set_custom_sub_range(-100, 100)
        self.set_custom_mul_range(2, 12)
        self.set_custom_div_range(-12, 12)

        self.set_custom_intdiv_range(1, 12)
        self.set_custom_mod_range(1, 121)

    def get_custom_difficulty(self):
        operattions: lest[Operation] = []

        addition: AdditionRange | None = None
        subtraction: SubtractionRange | None = None
        multiplication: MultiplicationRange | None = None
        division: DivisionRange | None = None
        integer_division: IntDivRange | None = None
        mod: ModRange | None = None

        if self.get_custom_add_enabled():
            operations.append(Operation.ADD)
            min_val, max_val = self.get_custom_add_range()
            addition = AdditionRange(
                min_first=min_val, max_first=max_val,
                min_second=min_val, max_second=max_val,
            )

        if self.get_custom_sub_enabled():
            operations.append(Operation.SUB)
            min_val, max_val = self.get_custom_sub_range()
            subtraction = SubtractionRange(
                min_first=min_val, max_first=max_val,
                min_second=min_val, max_second=max_val,
                keep_non_negative=self.get_custom_sub_non_negative(),
            )

        if self.get_custom_mul_enabled():
            operations.append(Operation.MUL)
            min_val, max_val = self.get_custom_mul_range()
            multiplication = MultiplicationRange(
                min_first=min_val, max_first=max_val,
                min_second=min_val, max_second=max_val,
            )

        if self.get_custom_div_enabled():
            operations.append(Operation.DIV)
            min_val, max_val = self.get_custom_div_range()
            division = DivisionRange(
                min_divisor=min_val, max_divisor=max_val,
                min_quotient=min_val, max_quotient=max_val,
            )

        if self.get_custom_intdiv_enabled():
            operations.append(Operation.INTEGER_DIV)
            min_val, max_val = self.get_custom_intdiv_range()
            integer_division = IntDivRange(
                min_divisor=min_val, max_divisor=max_val,
                min_base=min_val, max_base=max_val,
            )

        if self.get_custom_mod_enabled():
            operations.append(Operation.MOD)
            min_val, max_val = self.get_custom_mod_range()
            mod = ModRange(
                min_divisor=min_val, max_divisor=max_val,
                min_base=min_val, max_base=max_val,
            )

        return DifficultySettings(
            operations=tuple(operations),
            addition=addition,
            subtraction=subtraction,
            multiplication=multiplication,
            division=division,
            integer_division=integer_division,
            mod=mod,
        )
