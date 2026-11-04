from numo.core.core_settings import Difficulty, GameMode
from gettext import gettext as _
from numo.core.custom_errors import StatsError


DIFF_ORDER = tuple(d.value for d in Difficulty)

ACC_PERCENTAGE_SUCCESS = 85
ACC_PERCENTAGE_WARNING = 50

TICK_INTERVAL_MS = 200
FEEDBACK_DURATION_MS = 500
BONUS_FADE_MS = 400

MAX_LENGHT_ANSWER = 6

MODE_LABELS = {
    GameMode.SURVIVAL: "Survival",
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
    GameMode.SURVIVAL: "input-gaming-symbolic",
    GameMode.TIMER: "document-open-recent-symbolic",
    GameMode.TIMER_BONUS: "alarm-symbolic",
    GameMode.TASKS: "view-list-symbolic",
}

MODE_COLORS = {
    GameMode.SURVIVAL: "accent",
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


def stats_error_message(error: StatsError) -> str:
    messages = {
        "stats_read_error": _("Could not read statistics"),
        "stats_invalid_json": _("Statistics reset — file corrupted"),
        "stats_invalid_structure": _("Statistics reset — invalid structure"),
        "stats_directory_error": _("Could not create the statistics folder"),
        "stats_write_error": _("Could not save statistics"),
        "export_write_error": _("Could not export statistics"),
        "import_read_error": _("Could not read the import file"),
        "import_invalid_json": _("The import file is not valid JSON"),
        "import_invalid_structure": _("The import file has an invalid structure"),
    }
    return messages.get(error.code, _("An unknown statistics error occurred"))
