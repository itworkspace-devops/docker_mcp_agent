from backend.compliance.policies import (
    COMPLIANCE_RULES
)


def evaluate_container(
    inspect_data
):

    violations = []

    host_config = inspect_data.get(
        "HostConfig",
        {}
    )

    restart_policy = (
        host_config
        .get(
            "RestartPolicy",
            {}
        )
        .get(
            "Name"
        )
    )

    if (
        restart_policy
        != COMPLIANCE_RULES[
            "restart_policy"
        ]
    ):

        violations.append(
            "restart policy mismatch"
        )

    if host_config.get(
        "Privileged"
    ):

        violations.append(
            "privileged container"
        )

    return violations