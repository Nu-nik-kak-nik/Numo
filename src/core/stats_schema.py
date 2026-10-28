from dataclasses import dataclass, asdict, field
from datetime import datetime
from typing import Self
from numo.core.core_settings import Difficulty, GameMode, SCHEMA_VERSION, MIGRATIONS
from numo.core.custom_errors import MigrationError
from numo.utils.formatting import datetime_from_iso, date_with_seconds


@dataclass
class Session:
    timestamp: str
    mode: GameMode
    difficulty: Difficulty
    correct: int
    wrong: int
    elapsed_sec: float
    duration_sec: int | None = None
    target_tasks: int | None = None
    initial_time_sec: int | None = None
    bonus_sec: int | None = None
    max_mistakes: int | None = None

    @property
    def total(self) -> int:
        return self.correct + self.wrong

    @property
    def accuracy(self) -> float | None:
        if self.total == 0:
            return None
        return round(self.correct / self.total * 100.0, 1)

    @property
    def dt(self) -> datetime:
        return datetime_from_iso(self.timestamp)

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "Session": # Self
        return cls(
            timestamp=d["timestamp"],
            mode=GameMode(d["mode"]),
            difficulty=Difficulty(d["difficulty"]),
            correct=d["correct"],
            wrong=d["wrong"],
            elapsed_sec=d["elapsed_sec"],
            duration_sec=d.get("duration_sec"),
            target_tasks=d.get("target_tasks"),
            initial_time_sec=d.get("initial_time_sec"),
            bonus_sec=d.get("bonus_sec"),
            max_mistakes=d.get("max_mistakes"),
        )

    @classmethod
    def create(
        cls,
        mode: GameMode,
        difficulty: Difficulty,
        correct: int,
        wrong: int,
        elapsed_sec: float,
        duration_sec: int | None = None,
        target_tasks: int | None = None,
        initial_time_sec: int | None = None,
        bonus_sec: int | None = None,
        max_mistakes: int | None = None,
    ) -> "Session": # Self
        return cls(
            timestamp=date_with_seconds(),
            mode=GameMode(mode),
            difficulty=Difficulty(difficulty),
            correct=correct,
            wrong=wrong,
            elapsed_sec=round(elapsed_sec, 2),
            duration_sec=duration_sec,
            target_tasks=target_tasks,
            initial_time_sec=initial_time_sec,
            bonus_sec=bonus_sec,
            max_mistakes=max_mistakes,
        )


@dataclass
class StatsFile:
    version: int = SCHEMA_VERSION
    app_version: str = ""
    sessions: list[Session] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "version": self.version,
            "app_version": self.app_version,
            "sessions": [s.to_dict() for s in self.sessions],
        }

    @classmethod
    def from_dict(cls, d: dict) -> "StatsFile": # Self
        current_version = d.get("version", 1)

        if current_version > SCHEMA_VERSION:
            raise MigrationError(f"Unsupported stats version {current_version}.")

        while current_version < SCHEMA_VERSION:
            migration = MIGRATIONS.get(current_version)
            if migration is None:
                raise MigrationError(f"No migration from version {current_version}")
            d = migration(d)
            current_version += 1
            d["version"] = current_version

        return cls(
            version=SCHEMA_VERSION,
            app_version=d.get("app_version", ""),
            sessions=[Session.from_dict(s) for s in d.get("sessions", [])],
        )

