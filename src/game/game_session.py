import time
from dataclasses import dataclass

from numo.core.core_settings import GameMode, Difficulty, SessionOptions
from numo.core.stats_schema import Session
from numo.game.task import Task
from numo.game.task_generator import TaskGenerator



class GameSession:
    def __init__(
        self,
        mode: GameMode,
        difficulty: Difficulty,
        options: SessionOptions,
    ):
        self._mode = mode
        self._difficulty = difficulty
        self._options = options
        self._generator = TaskGenerator(difficulty)
        self._current = self._generator.next_task()
        self._correct = 0
        self._wrong = 0
        self._finished = False
        self._start = time.monotonic()
        self._time_left: float | None = None
        if mode == GameMode.TIMER:
            self._time_left = float(options.duration_sec)
        elif mode == GameMode.TIMER_BONUS:
            self._time_left = float(options.initial_time_sec)

    @property
    def mode(self) -> GameMode: return self._mode
    @property
    def difficulty(self) -> Difficulty: return self._difficulty
    @property
    def current_task(self) -> Task: return self._current
    @property
    def correct(self) -> int: return self._correct
    @property
    def wrong(self) -> int: return self._wrong
    @property
    def finished(self) -> bool: return self._finished
    @property
    def elapsed_sec(self) -> float: return time.monotonic() - self._start
    @property
    def time_left(self) -> float | None: return self._time_left

    def status_text(self) -> str:
        if self._mode == GameMode.NORMAL:
            return str(self._correct + self._wrong + 1)
        if self._mode == GameMode.TASKS:
            if self._finished:
                return f"{self._options.target_tasks} / {self._options.target_tasks}"
            current = self._correct + self._wrong + 1
            return f"{current} / {self._options.target_tasks}"
        return _format_time(self._time_left or 0)

    def submit(self, user_answer: int) -> bool:
        if self._finished:
            return False

        is_correct = self._current.check(user_answer)
        if is_correct:
            self._correct += 1

            if self._mode == GameMode.TIMER_BONUS:
                self._time_left += self._options.bonus_sec

        else:
            self._wrong += 1

        if self._should_finish():
            self._finished = True
            return is_correct

        self._current = self._generator.next_task()
        return is_correct

    def tick(self, delta: float) -> bool:
        if self._finished or self._time_left is None:
            return False

        self._time_left -= delta
        if self._time_left <= 0:
            self._time_left = 0
            self._finished = True
            return True
        return False

    def _should_finish(self) -> bool:
        if self._mode == GameMode.NORMAL:
            return self._wrong > 0
        if self._mode == GameMode.TASKS:
            return self._correct + self._wrong >= self._options.target_tasks
        return False

    def to_record(self) -> Session:
        return Session.create(
            mode=self._mode,
            difficulty=self._difficulty,
            correct=self._correct,
            wrong=self._wrong,
            elapsed_sec=self.elapsed_sec,
            duration_sec=self._options.duration_sec,
            target_tasks=self._options.target_tasks,
            initial_time_sec=self._options.initial_time_sec,
            bonus_sec=self._options.bonus_sec,
        )

    def result_data(self) -> dict[str, int | float | list[int]]:
        dict_data = {
            "mode" : self._mode,
            "difficulty" : self._difficulty,
            "correct" : self._correct,
            "wrong" : self._wrong,
            "duration" : _format_time(self.elapsed_sec),
            "accuracy" : self._accuracy(),
        }

        match self._mode:
            case GameMode.NORMAL:
                dict_data["mode_data"] = self._correct

            case GameMode.TIMER:
                dict_data["mode_data"] = self._options.duration_sec // 60

            case GameMode.TIMER_BONUS:
                dict_data["mode_data"] = [
                    self._options.initial_time_sec,
                    self._options.bonus_sec
                ]

            case GameMode.TASKS:
                dict_data["mode_data"] = self._options.target_tasks

            case _:
                dict_data["mode_data"] = 0

        return dict_data

    def _accuracy(self) -> float:
        total = self._correct + self._wrong
        return round(self._correct / total * 100.0, 1) if total else 0.0



def _format_time(seconds: float) -> str:
    total = int(seconds)
    minutes, secs = divmod(total, 60)
    return f"{minutes}:{secs:02d}"
