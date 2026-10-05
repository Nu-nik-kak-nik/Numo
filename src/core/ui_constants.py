from numo.core.core_settings import Difficulty, GameMode
from gettext import gettext as _


DIFF_ORDER = ("easy", "medium", "hard")

ACC_PERCENTAGE_SUCCESS = 85
ACC_PERCENTAGE_WARNING = 50

TICK_INTERVAL_MS = 200
FEEDBACK_DURATION_MS = 500
BONUS_FADE_MS = 400

DIFF_TO_NICK = {
    Difficulty.EASY: "easy",
    Difficulty.MEDIUM: "medium",
    Difficulty.HARD: "hard",
}

NICK_TO_DIFF = {v: k for k, v in DIFF_TO_NICK.items()}


MODE_LABELS = {
    GameMode.NORMAL: _("Normal"),
    GameMode.TIMER: _("Timer"),
    GameMode.TIMER_BONUS: _("Timer + Bonus"),
    GameMode.TASKS: _("Task Count"),
}

DIFF_LABELS = {
    Difficulty.EASY: _("Easy"),
    Difficulty.MEDIUM: _("Medium"),
    Difficulty.HARD: _("Hard"),
}

MODE_ICONS = {
    GameMode.NORMAL: "input-gaming-symbolic",
    GameMode.TIMER: "document-open-recent-symbolic",
    GameMode.TIMER_BONUS: "alarm-symbolic",
    GameMode.TASKS: "view-list-symbolic",
}

MODE_COLORS = {
    GameMode.NORMAL: "accent",
    GameMode.TIMER: "warning",
    GameMode.TIMER_BONUS: "success",
    GameMode.TASKS: "error",
}

DIFFICULTY_LABELS = {
    Difficulty.EASY: _("Easy"),
    Difficulty.MEDIUM: _("Medium"),
    Difficulty.HARD: _("Hard"),
}

DIFFICULTY_ICONS = {
    Difficulty.EASY: "starred-symbolic",
    Difficulty.MEDIUM: "starred-symbolic",
    Difficulty.HARD: "starred-symbolic",
}

