from backend.policies.risk import (
    RISK_LEVELS
)

from backend.policies.approval_policy import (
    APPROVAL_POLICIES
)


def requires_approval(
    tool_name
):

    risk = RISK_LEVELS.get(
        tool_name,
        "medium"
    )

    return APPROVAL_POLICIES[
        risk
    ]