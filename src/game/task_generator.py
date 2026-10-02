import random
from numo.core.core_settings import Difficulty
from numo.game.task import Operation, Task

class TaskGenerator:
    def __init__(self, difficulty: Difficulty):
        self._difficulty = difficulty

    def next_task(self):
        match self._difficulty:
            case Difficulty.EASY:
                return self._easy()
            case Difficulty.MEDIUM:
                return self._medium()
            case Difficulty.HARD:
                return self._hard()
            case _:
                raise ValueError(f"Unknown difficulty: {self._difficulty}")



    def _easy(self) -> Task:
        operation = random.choice((Operation.ADD, Operation.SUB))
        if operation == Operation.ADD:
            return Task(random.randint(1, 50), random.randint(1, 50), operation)

        a = random.randint(1, 50)
        b = random.randint(1, a)
        return Task(a, b, operation)

    def _medium(self) -> Task:
        operation = random.choice((Operation.ADD, Operation.SUB, Operation.MUL, Operation.DIV))
        match operation:
            case Operation.ADD | Operation.SUB:
                return Task(random.randint(5, 99), random.randint(5, 99), operation)

            case Operation.MUL:
                return Task(random.randint(2, 14), random.randint(2, 14), operation)

            case Operation.DIV:
                b = random.randint(2, 15)
                quotient = random.randint(2, 20)
                return Task(quotient * b, b, operation)

            case _:
                raise ValueError(f"Unexpected operation: {operation}")

    def _hard(self) -> Task:
        operation = random.choice((Operation.ADD,
                                Operation.SUB,
                                Operation.MUL,
                                Operation.DIV,
                                Operation.FLOOR_DIV,
                                Operation.MOD
                            ))
        match operation:
            case Operation.ADD | Operation.SUB:
                return Task(random.randint(-200, 200), random.randint(-200, 200), operation)

            case Operation.MUL:
                return Task(random.randint(-20, 20), random.randint(-20, 20), operation)

            case Operation.DIV:
                b = random.randint(3, 25)
                quotient = random.randint(3, 25)
                return Task(quotient * b, b, operation)

            case Operation.FLOOR_DIV | Operation.MOD:
                return self._hard_div_mod(operation)

            case _:
                raise ValueError(f"Unexpected operation: {operation}")

    @staticmethod
    def _hard_div_mod(operation) -> Task:
        b = random.randint(3, 25)
        base = random.randint(3, 25)
        displacement = random.randint(1, b - 1)
        if random.choice((0, 1)) == 1:
            a = base * b + displacement
        else:
            a = base * b - displacement
        return Task(a, b, operation)
