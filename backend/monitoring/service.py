from backend.monitoring.collector import (
    collect_metrics
)

from backend.monitoring.alerts import (
    evaluate_metric
)

from backend.database.repository import (
    get_latest_metrics
)

from backend.audit.logger import (
    audit_log
)

from backend.remediation.planner import (
    create_plan
)

from backend.watcher.findings import (
    add_remediation
)


def run_monitoring():

    try:

        # Collect fresh metrics
        collect_metrics()

        # Load latest metrics from DB
        metrics = get_latest_metrics()

        findings = []

        for metric in metrics:

            metric_findings = evaluate_metric(
                metric
            )
            for finding in metric_findings:

                plan = create_plan(
                    finding
                )

                if plan:

                    add_remediation(
                        finding,
                        plan
                    )
            findings.extend(
                metric_findings
            )

        audit_log(
            action="monitoring",
            target="docker_metrics",
            status=(
                f"success: "
                f"{len(findings)} findings"
            ),
        )

        return {

            "success": True,

            "metrics_count":
                len(metrics),

            "findings_count":
                len(findings),

            "findings":
                findings,
        }

    except Exception as ex:

        audit_log(
            action="monitoring",
            target="docker_metrics",
            status=f"failed: {str(ex)}",
        )

        return {

            "success": False,

            "error": str(ex),
        }