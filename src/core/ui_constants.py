from numo.core.core_settings import Difficulty, GameMode
from gettext import gettext as _


DIFF_ORDER = tuple(d.value for d in Difficulty)

ACC_PERCENTAGE_SUCCESS = 85
ACC_PERCENTAGE_WARNING = 50

TICK_INTERVAL_MS = 200
FEEDBACK_DURATION_MS = 500
BONUS_FADE_MS = 400

MAX_LENGHT_ANSWER = 6

MODE_LABELS = {
    GameMode.NORMAL: "Normal",
    GameMode.TIMER: "Timer",
    GameMode.TIMER_BONUS: "Timer + Bonus",
    GameMode.TASKS: "Task Count",
}

DIFF_LABELS = {
    Difficulty.EASY: "Easy",
    Difficulty.MEDIUM: "Medium",
    Difficulty.HARD: "Hard",
    Difficulty.CUSTOM: "Custom"
}

def mode_label(mode: GameMode) -> str:
    return _(MODE_LABELS[mode])

def diff_label(d: Difficulty) -> str:
    return _(DIFF_LABELS[d])

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

DIFFICULTY_ICONS = {
    Difficulty.EASY: "leaves-symbolic",
    Difficulty.MEDIUM: "tree-circle-symbolic",
    Difficulty.HARD: "skull-symbolic",
    Difficulty.CUSTOM: "sliders-symbolic",
}

