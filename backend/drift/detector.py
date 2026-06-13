from backend.watcher.findings import (
    add_finding
)


def detect_drift(
    baseline,
    inspect_data,
):

    findings = []

    image = inspect_data.get(
        "Config",
        {}
    ).get(
        "Image"
    )

    if image != baseline.image:

        findings.append(

            add_finding(

                severity="high",

                category="drift",

                message=(
                    f"{baseline.container_name} "
                    f"image drift detected"
                )
            )
        )

    running = inspect_data.get(
        "State",
        {}
    ).get(
        "Running"
    )

    if (
        baseline.expected_status
        == "running"
        and not running
    ):

        findings.append(

            add_finding(

                severity="critical",

                category="drift",

                message=(
                    f"{baseline.container_name} "
                    f"is not running"
                )
            )
        )

    return findings