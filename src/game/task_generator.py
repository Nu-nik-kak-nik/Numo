import random
from numo.core.core_settings import Difficulty, DifficultySettings, DIFFICULTY_SETTINGS, IntDivRange, ModRange
from numo.game.task import Operation, Task

class TaskGenerator:
    def __init__(self, difficulty: Difficulty):
        try:
            self._settings: DifficultySettings = DIFFICULTY_SETTINGS[difficulty]
        except KeyError as exc:
            raise ValueError(f"Unknown difficulty: {difficulty}") from exc

    def next_task(self) -> Task:
        operation = random.choice(self._settings.operations)
        match operation:
            case Operation.ADD:
                return self._addition(operation)
            case Operation.SUB:
                return self._subtraction(operation)
            case Operation.MUL:
                return self._multiplication(operation)
            case Operation.DIV:
                return self._division(operation)
            case Operation.INTEGER_DIV:
                return self._int_div(operation)
            case Operation.MOD:
                return self._mod(operation)
            case _:
                raise ValueError(f"Unexpected operation: {operation}")

    def _addition(self, operation: Operation) -> Task:
        data = self._settings.addition
        return Task(
            random.randint(data.min_first, data.max_first),
            random.randint(data.min_second, data.max_second),
            operation
        )

    def _subtraction(self, operation: Operation) -> Task:
        data = self._settings.subtraction
        first = random.randint(data.min_first, data.max_first)

        if data.keep_non_negative and data.min_first >= 0:
            second = random.randint(data.min_second, first)
        else:
            second = random.randint(data.min_second, data.max_second)

        return Task(first, second, operation)

    def _multiplication(self, operation: Operation) -> Task:
        data = self._settings.multiplication
        return Task(
            self._pick_non_zero(data.min_first, data.max_first),
            self._pick_non_zero(data.min_second, data.max_second),
            operation,
        )

    def _division(self, operation: Operation) -> Task:
        data = self._settings.division
        divisor = self._pick_non_zero(data.min_divisor, data.max_divisor)
        quotient = self._pick_non_zero(data.min_quotient, data.max_quotient)
        return Task(quotient * divisor, divisor, operation)

    def _int_div(self, operation: Operation) -> Task:
        data = self._settings.integer_division
        return self._div_mod(data, operation)

    def _mod(self, operation: Operation) -> Task:
        data = self._settings.mod
        return self._div_mod(data, operation)

    @staticmethod
    def _div_mod(data: IntDivRange | ModRange, operation: Operation) -> Task:
        divisor = random.randint(data.min_divisor, data.max_divisor)
        base = random.randint(data.min_base, data.max_base)
        remainder = random.randint(data.min_remainder, divisor - 1)

        dividend = base * divisor + remainder
        return Task(dividend, divisor, operation)

    @staticmethod
    def _pick_non_zero(min_val: int, max_val: int) -> int:
        if min_val <= 0 <= max_val:
            offset = random.randint(min_val, max_val - 1)
            return offset + 1 if offset >= 0 else offset
        else:
            return random.randint(min_val, max_val)
