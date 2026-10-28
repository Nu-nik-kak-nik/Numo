from typing import Any


def migrate_v1_to_v2(data: dict[str, Any]) -> dict[str, Any]:
    for session in data.get("sessions", []):
        if session.get("mode") == "normal":
            session["mode"] = "survival"

        if "max_mistakes" not in session:
            session["max_mistakes"] = 1 if session.get("mode") == "survival" else None

    return data
