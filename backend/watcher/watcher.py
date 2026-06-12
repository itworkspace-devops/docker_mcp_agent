from backend.watcher.rules import (
    evaluate_rules
)


def run_watcher():

    print(
        "[WATCHER] Running checks"
    )

    evaluate_rules()

    print(
        "[WATCHER] Completed"
    )