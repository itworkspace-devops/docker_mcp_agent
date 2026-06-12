from backend.database.repository import (
    save_audit_log
)


def audit_log(
    action,
    target,
    status,
):

    save_audit_log(
        action,
        target,
        status,
    )