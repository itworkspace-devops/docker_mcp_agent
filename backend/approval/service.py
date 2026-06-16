import os
import sys
import select
import threading
import time

from backend.config.settings import (
    settings
)

from backend.approval.engine import (
    create_execution_id,
)

from backend.approval.store import (
    PENDING_APPROVALS,
    PENDING_APPROVAL_EVENTS,
)


def create_pending_approval(
    tool_name,
    tool_args,
    origin="cli",
    host_name=None,
):

    execution_id = create_execution_id()

    PENDING_APPROVALS[execution_id] = {
        "tool_name": tool_name,
        "tool_args": tool_args,
        "host_name": host_name,
        "approved": None,
        "origin": origin,
        "status": "pending",
    }

    if origin == "cli":
        PENDING_APPROVAL_EVENTS[execution_id] = threading.Event()

    return execution_id


def resolve_pending_approval(
    execution_id,
    approved,
    resolved_by,
):

    approval = PENDING_APPROVALS.get(
        execution_id
    )

    if approval is None:
        return None

    approval["approved"] = approved
    approval["status"] = (
        "approved"
        if approved
        else "rejected"
    )
    approval["resolved_by"] = resolved_by

    event = PENDING_APPROVAL_EVENTS.get(
        execution_id
    )

    if event is not None:
        event.set()

    return approval


def remove_pending_approval(
    execution_id,
):

    PENDING_APPROVALS.pop(
        execution_id,
        None,
    )

    event = PENDING_APPROVAL_EVENTS.pop(
        execution_id,
        None,
    )

    if event is not None:
        event.set()


def _input_with_event(
    prompt,
    stop_event,
):

    sys.stdout.write(prompt)
    sys.stdout.flush()

    if os.name == "nt":
        import msvcrt

        line = ""
        while True:
            if stop_event is not None and stop_event.is_set():
                return None

            if msvcrt.kbhit():
                ch = msvcrt.getwch()

                if ch in ("\r", "\n"):
                    print()
                    return line

                if ch == "\x08":
                    if line:
                        line = line[:-1]
                        sys.stdout.write("\b \b")
                        sys.stdout.flush()
                    continue

                line += ch
                sys.stdout.write(ch)
                sys.stdout.flush()

            time.sleep(0.05)

        return None

    while True:
        if stop_event is not None and stop_event.is_set():
            return None

        readable, _, _ = select.select(
            [sys.stdin],
            [],
            [],
            0.1,
        )

        if readable:
            line = sys.stdin.readline()

            if line == "":
                return None

            return line.rstrip("\n")


def request_approval(
    tool_name,
    tool_args,
    execution_id=None,
):

    if settings.approval_mode != "cli":
        return False

    if execution_id is None:
        execution_id = create_pending_approval(
            tool_name,
            tool_args,
            origin="cli",
        )

    approval = PENDING_APPROVALS.get(
        execution_id
    )

    if approval is not None and approval["approved"] is not None:
        remove_pending_approval(execution_id)
        return approval["approved"]

    print()
    print("=" * 60)
    print(f"Execution ID : {execution_id}")
    print(f"Action       : {tool_name}")
    print(f"Arguments    : {tool_args}")
    print()
    print(
        "You can approve or reject this request from the UI while the CLI prompt is open."
    )
    print()

    event = PENDING_APPROVAL_EVENTS.get(
        execution_id
    )

    answer = _input_with_event(
        "Approve? (y/n): ",
        event,
    )

    approval = PENDING_APPROVALS.get(
        execution_id
    )

    if approval is not None and approval["approved"] is not None:
        remove_pending_approval(execution_id)
        return approval["approved"]

    approved = False
    if answer is not None:
        approved = answer.strip().lower() == "y"

    resolve_pending_approval(
        execution_id,
        approved,
        "cli",
    )
    remove_pending_approval(execution_id)

    return approved