from backend.database.repository import (
    save_finding,
    close_finding_record,
    save_remediation,
    update_remediation_record,
)

from backend.notifications.service import (
    create_notification
)


def add_finding(
    severity: str,
    category: str,
    message: str,
):

    finding = save_finding(
        severity=severity,
        category=category,
        message=message,
    )

    create_notification(
        event_type="finding",
        title=f"{severity.upper()} Finding",
        message=message,
    )

    return finding


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

    remediation = save_remediation(
        finding_id=finding.id,
        tool_name=plan["tool_name"],
        tool_args=plan["tool_args"],
    )

    create_notification(
        event_type="remediation",
        title="Remediation Created",
        message=f"Remediation created for finding #{finding.id}",
    )

    return remediation


def update_remediation_status(
    remediation_id: int,
    status: str,
):

    remediation = update_remediation_record(
        remediation_id,
        status,
    )

    create_notification(
        event_type="remediation",
        title="Remediation Updated",
        message=f"Remediation #{remediation_id} status changed to {status}",
    )

    return remediation