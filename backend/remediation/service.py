from backend.remediation.executor import (
    execute_plan
)

from backend.remediation.verifier import (
    verify_container_running
)


def execute_remediation(
    remediation
):

    result = execute_plan(
        remediation["plan"]
    )

    container = (
        remediation["plan"]
        ["tool_args"]
        .get("container")
    )

    verified = (
        verify_container_running(
            container
        )
    )

    return {

        "execution":
            result,

        "verified":
            verified,
    }