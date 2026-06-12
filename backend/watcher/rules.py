from backend.watcher.findings import (
    add_finding
)

from backend.watcher.docker_health import (
    check_stopped_containers
)

from backend.remediation.engine import (
    create_remediation
)


def evaluate_rules():

    stopped = (
        check_stopped_containers()
    )

    for item in stopped:

        finding = add_finding(

            severity="high",

            category="container",

            message=
            (
                f"Container "
                f"{item['container']} "
                f"is stopped"
            ),
        )

        create_remediation(
            finding
        )