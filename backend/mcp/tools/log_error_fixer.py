from __future__ import annotations

import re

from backend.mcp.tools.base import success, failure
from backend.mcp.tools.containers import container_logs, _find_container
from backend.mcp.docker_client import get_docker


ERROR_PATTERNS = [
    ("oom", re.compile(r"(oomkilled|out of memory|oom)", re.I), "Container may be hitting memory limits or being OOM-killed."),
    ("permission", re.compile(r"(permission denied|operation not permitted|readonly file system)", re.I), "File system or privilege issue detected."),
    ("port", re.compile(r"(address already in use|port is already allocated|bind: address already in use)", re.I), "Host port conflict detected."),
    ("crash", re.compile(r"(exited with code|segmentation fault|panic:|crashloopbackoff|fatal error)", re.I), "Process crash pattern detected."),
]


def _analyze_log(text: str):
    matches = []
    suggestions = []
    for key, pattern, suggestion in ERROR_PATTERNS:
        if pattern.search(text):
            matches.append(key)
            suggestions.append(suggestion)
    if not matches:
        suggestions.append("No common Docker failure pattern was detected. Check the log context and container config.")
    return matches, suggestions


def fix_log_text_errors(arguments):
    try:
        text = arguments.get("log_text", "")
        matches, suggestions = _analyze_log(text)
        return success(
            {
                "patterns": matches,
                "suggestions": suggestions,
            },
            message="Log analysis completed."
        )
    except Exception as ex:
        return failure(str(ex))


def fix_container_log_errors(arguments):
    try:
        host_name = arguments.get("host_name")
        container_name = arguments["container"]
        tail = arguments.get("tail", 200)
        logs = container_logs({"container": container_name, "tail": tail, "host_name": host_name})
        if not logs.get("success"):
            return logs
        text = logs["data"] if isinstance(logs["data"], str) else str(logs["data"])
        matches, suggestions = _analyze_log(text)
        return success(
            {
                "container": container_name,
                "patterns": matches,
                "suggestions": suggestions,
                "logs": text[-4000:],
            },
            message=f"Analyzed logs for {container_name}."
        )
    except Exception as ex:
        return failure(str(ex))


def detect_crash_loop(arguments):
    try:
        host_name = arguments.get("host_name")
        client = get_docker(host_name)
        results = []
        for container in client.containers.list(all=True):
            attrs = container.attrs or {}
            restart_count = int(((attrs.get("RestartCount") or 0)))
            oom_killed = bool(attrs.get("State", {}).get("OOMKilled"))
            if restart_count >= arguments.get("min_restarts", 3) or oom_killed:
                results.append(
                    {
                        "name": container.name,
                        "id": container.short_id,
                        "restart_count": restart_count,
                        "oom_killed": oom_killed,
                        "status": container.status,
                    }
                )
        return success(results, message="Crash-loop scan completed.")
    except Exception as ex:
        return failure(str(ex))


def fix_crash_loop(arguments):
    try:
        host_name = arguments.get("host_name")
        container_name = arguments["container"]
        action = arguments.get("action", "restart")
        container = _find_container(container_name, host_name)
        if action == "stop":
            container.stop()
        elif action == "remove":
            container.remove(force=True)
        else:
            container.restart()
        return success(
            {"container": container.name, "action": action},
            message=f"{action.title()} applied to {container.name}."
        )
    except Exception as ex:
        return failure(str(ex))
