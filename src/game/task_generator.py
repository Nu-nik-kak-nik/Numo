import random
from numo.core.core_settings import Difficulty, DifficultySettings, DIFFICULTY_SETTINGS
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
            case Operation.ADD | Operation.SUB:
                return self._add_sub(operation)
            case Operation.MUL:
                return self._multiplication()
            case Operation.DIV:
                return self._division()
            case Operation.FLOOR_DIV | Operation.MOD:
                return self._div_mod(operation)
            case _:
                raise ValueError(f"Unexpected operation: {operation}")

    def _add_sub(self, operation: Operation) -> Task:
        data = self._settings.add_sub
        first = random.randint(data.min_first, data.max_first)

        if operation is Operation.SUB and data.keep_non_negative:
            second = random.randint(data.min_second, first)
        else:
            second = random.randint(data.min_second, data.max_second)

        return Task(first, second, operation)

    def _multiplication(self) -> Task:
        data = self._settings.multiplication
        return Task(
            random.randint(data.min_first, data.max_first),
            random.randint(data.min_second, data.max_second),
            Operation.MUL,
        )

    def _division(self) -> Task:
        data = self._settings.division
        divisor = random.randint(data.min_divisor, data.max_divisor)
        quotient = random.randint(data.min_quotient, data.max_quotient)
        return Task(quotient * divisor, divisor, Operation.DIV)

    def _div_mod(self, operation: Operation) -> Task:
        data = self._settings.div_mod
        divisor = random.randint(data.min_divisor, data.max_divisor)
        base = random.randint(data.min_base, data.max_base)
        remainder = random.randint(data.min_remainder, divisor - 1)
        sign = random.choice((-1, 1))
        dividend = base * divisor + remainder * sign
        return Task(dividend, divisor, operation)
