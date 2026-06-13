from backend.mcp.tools.monitoring import (
    docker_metrics
)

from backend.database.repository import (
    save_container_metric
)


def collect_metrics():

    response = docker_metrics({})

    if not response["success"]:

        return response

    for item in response["data"]:

        memory_stats = item[
            "memory"
        ]

        memory_usage = (
            memory_stats
            .get(
                "usage",
                0
            )
        )

        memory_mb = round(
            memory_usage /
            1024 /
            1024,
            2
        )

        save_container_metric(

            container_name=
                item["container"],

            status=
                item["status"],

            cpu_percent=
                0,

            memory_mb=
                memory_mb,
        )

    return response