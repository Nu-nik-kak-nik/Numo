import time

from numo.core.core_settings import TaskRecord
from numo.core.ui_constants import MAX_TASK_RECORDS
from numo.game.task import Task


class TaskRecorder:
    def __init__(self, enabled: bool) -> None:
        self._enabled = enabled
        self._records: list[TaskRecord] = []
        self._task_start: float | None = None

    @property
    def enabled(self) -> bool:
        return self._enabled

    def on_task_show(self) -> None:
        if not self._enabled:
            return
        self._task_start = time.monotonic()

    def record(self, task: Task, user_answer: int, is_correct: bool) -> None:
        if not self._enabled or self._task_start is None:
            return
        if len(self._records) >= MAX_TASK_RECORDS:
            self._task_start = None
            return

        elapsed = int(time.monotonic() - self._task_start)
        self._records.append(TaskRecord(
            number=len(self._records) + 1,
            expression=task.expression,
            user_answer=str(user_answer),
            time_seconds=elapsed,
            is_correct=is_correct,
        ))
        self._task_start = None

    def get_records(self) -> list[TaskRecord]:
        return list(self._records)

    def has_records(self) -> bool:
        return bool(self._records)

    def clear(self) -> None:
        self._records.clear()
        self._task_start = None
