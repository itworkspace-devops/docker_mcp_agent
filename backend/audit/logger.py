import json
from datetime import datetime
from pathlib import Path


LOG_DIR = Path(
    "logs"
)

LOG_DIR.mkdir(
    exist_ok=True
)

AUDIT_FILE = (
    LOG_DIR /
    "audit.jsonl"
)


def audit_log(
    action,
    target,
    status,
):

    record = {

        "timestamp":
            datetime.utcnow().isoformat(),

        "action":
            action,

        "target":
            target,

        "status":
            status,
    }

    with open(
        AUDIT_FILE,
        "a",
        encoding="utf-8",
    ) as fp:

        fp.write(
            json.dumps(record)
            + "\n"
        )