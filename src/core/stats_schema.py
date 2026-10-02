from dataclasses import dataclass, asdict, field
from datetime import datetime
from numo.core.core_settings import Difficulty, GameMode, SCHEMA_VERSION


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
        return datetime.fromisoformat(self.timestamp)

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "Session":
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
    ) -> "Session":
        return cls(
            timestamp=datetime.now().isoformat(timespec="seconds"),
            mode=GameMode(mode),
            difficulty=Difficulty(difficulty),
            correct=correct,
            wrong=wrong,
            elapsed_sec=round(elapsed_sec, 2),
            duration_sec=duration_sec,
            target_tasks=target_tasks,
            initial_time_sec=initial_time_sec,
            bonus_sec=bonus_sec,
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
    def from_dict(cls, d: dict) -> "StatsFile":
        return cls(
            version=d.get("version", SCHEMA_VERSION),
            app_version=d.get("app_version", ""),
            sessions=[Session.from_dict(s) for s in d.get("sessions", [])],
        )
