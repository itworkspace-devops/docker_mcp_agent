from __future__ import annotations

from typing import Any


def success(data: Any, message: str | None = None):
    payload = {
        "success": True,
        "data": data,
        "error": None,
    }
    if message:
        payload["message"] = message
    return payload


def failure(error: str, message: str | None = None):
    payload = {
        "success": False,
        "data": None,
        "error": str(error),
    }
    if message:
        payload["message"] = message
    return payload


def format_kv_lines(items: dict[str, Any]) -> str:
    lines = []
    for key, value in items.items():
        if value is None or value == "":
            continue
        lines.append(f"- {key}: {value}")
    return "\n".join(lines)


def summarize_list(title: str, rows: list[dict[str, Any]], empty_text: str = "No results found.") -> str:
    if not rows:
        return empty_text
    lines = [title]
    for row in rows:
        name = row.get("name") or row.get("container") or row.get("image") or "item"
        details = ", ".join(f"{k}={v}" for k, v in row.items() if k not in {"name", "container", "image"} and v not in [None, ""])
        lines.append(f"- {name}" + (f" ({details})" if details else ""))
    return "\n".join(lines)
