from datetime import datetime

from backend.database.repository import (
    save_finding,
    close_finding_record,
    save_remediation,
    update_remediation_record,
)


def add_finding(
    severity: str,
    category: str,
    message: str,
):

    return save_finding(
        severity=severity,
        category=category,
        message=message,
    )


def close_finding(
    finding_id: int
):

    return close_finding_record(
        finding_id
    )


def add_remediation(
    finding,
    plan,
):

    return save_remediation(
        finding_id=finding.id,
        tool_name=plan["tool_name"],
        tool_args=plan["tool_args"],
    )


def update_remediation_status(
    remediation_id: int,
    status: str,
):

    return update_remediation_record(
        remediation_id,
        status,
    )