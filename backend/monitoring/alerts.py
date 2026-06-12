from backend.watcher.findings import (
    add_finding
)


CPU_THRESHOLD = 80

MEMORY_THRESHOLD = 500


def evaluate_metric(metric):

    findings = []

    # High CPU

    if (
        metric.cpu_percent
        and metric.cpu_percent > CPU_THRESHOLD
    ):

        findings.append(

            add_finding(

                severity="high",

                category="cpu",

                message=(
                    f"{metric.container_name} "
                    f"CPU usage "
                    f"{metric.cpu_percent}%"
                ),
            )
        )

    # High Memory

    if (
        metric.memory_mb
        and metric.memory_mb > MEMORY_THRESHOLD
    ):

        findings.append(

            add_finding(

                severity="high",

                category="memory",

                message=(
                    f"{metric.container_name} "
                    f"memory usage "
                    f"{metric.memory_mb} MB"
                ),
            )
        )

    # Container Down

    if metric.status != "running":

        findings.append(

            add_finding(

                severity="critical",

                category="container",

                message=(
                    f"{metric.container_name} "
                    f"is not running"
                ),
            )
        )

    return findings