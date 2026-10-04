from enum import Enum
from dataclasses import dataclass


class Operation(str, Enum):
    ADD = "add"
    SUB = "sub"
    MUL = "mul"
    DIV = "div_exact"
    FLOOR_DIV = "floor_div"
    MOD = "mod"

    @property
    def symbol(self) -> str:
        return {
            Operation.ADD: "+",
            Operation.SUB: "-",
            Operation.MUL: "×",
            Operation.DIV: "÷",
            Operation.FLOOR_DIV: "div",
            Operation.MOD: "mod",
        }[self]

    def apply(self, a: int, b: int) -> int:
        match self:
            case Operation.ADD:
                return a + b
            case Operation.SUB:
                return a - b
            case Operation.MUL:
                return a * b
            case Operation.DIV:
                return a // b
            case Operation.FLOOR_DIV:
                return a // b
            case Operation.MOD:
                return a % b
            case _:
                raise ValueError(f"Unknown operation: {self}")


@dataclass(frozen=True)
class Task:
    a: int
    b: int
    operation: Operation

    @property
    def answer(self) -> int:
        return self.operation.apply(self.a, self.b)

    @property
    def expression(self) -> str:
        b_str = f'({self.b})' if self.b < 0 else str(self.b)
        return f'{self.a} {self.operation.symbol} {b_str}'

    def check(self, user_answer: int) -> bool:
        return user_answer == self.answer
