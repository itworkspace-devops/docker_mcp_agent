from backend.remediation.planner import (
    remediation_plan
)

from backend.remediation.approval import (
    approve_remediation
)

from backend.remediation.executor import (
    execute_remediation
)

from backend.watcher.findings import (
    add_remediation
)


def create_remediation(
    finding
):

    plan = remediation_plan(
        finding
    )

    if not plan:

        return None

    remediation = add_remediation(
        finding,
        plan
    )

    approved = approve_remediation(
        remediation
    )

    if approved:

        execute_remediation(
            remediation
        )

    return remediation