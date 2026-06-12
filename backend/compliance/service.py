from backend.client.mcp_client import (
    MCPClient
)

from backend.database.repository import (
    get_baselines
)

from backend.compliance.evaluator import (
    evaluate_container
)

mcp = MCPClient()


def run_compliance_scan():

    results = []

    for baseline in get_baselines():

        inspect = mcp.call(

            "docker_inspect",

            {
                "container":
                    baseline.container_name
            }
        )

        if not inspect.get(
            "success"
        ):
            continue

        violations = evaluate_container(

            inspect["data"]
        )

        if violations:

            results.append({

                "container":
                    baseline.container_name,

                "violations":
                    violations
            })

    return results