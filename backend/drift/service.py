from backend.client.mcp_client import (
    MCPClient
)

from backend.database.repository import (
    get_baselines
)

from backend.drift.detector import (
    detect_drift
)

mcp = MCPClient()


def run_drift_scan():

    findings = []

    for baseline in get_baselines():

        result = mcp.call(

            "docker_inspect",

            {
                "container":
                    baseline.container_name
            }
        )

        if not result.get(
            "success"
        ):
            continue

        findings.extend(

            detect_drift(

                baseline,

                result["data"]
            )
        )

    return findings