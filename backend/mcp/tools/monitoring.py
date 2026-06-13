from backend.mcp.docker_client import (
    get_docker
)

from backend.mcp.tools.base import (
    success,
    failure
)


def docker_metrics(arguments):

    try:

        client = get_docker()

        containers = (
            client.containers.list()
        )

        results = []

        for container in containers:

            stats = container.stats(
                stream=False
            )

            results.append({

                "container":
                    container.name,

                "status":
                    container.status,

                "cpu":
                    stats.get(
                        "cpu_stats",
                        {}
                    ),

                "memory":
                    stats.get(
                        "memory_stats",
                        {}
                    ),
            })

        return success(
            results
        )

    except Exception as ex:

        return failure(
            str(ex)
        )


def docker_top(arguments):

    try:

        client = get_docker()

        containers = (
            client.containers.list()
        )

        results = []

        for container in containers:

            stats = container.stats(
                stream=False
            )

            memory_usage = (
                stats
                .get(
                    "memory_stats",
                    {}
                )
                .get(
                    "usage",
                    0
                )
            )

            results.append({

                "container":
                    container.name,

                "memory_usage":
                    memory_usage,
            })

        results = sorted(

            results,

            key=lambda x:
                x["memory_usage"],

            reverse=True,
        )

        return success(
            results[:10]
        )

    except Exception as ex:

        return failure(
            str(ex)
        )


def docker_unhealthy(arguments):

    try:

        client = get_docker()

        containers = (
            client.containers.list(
                all=True
            )
        )

        unhealthy = []

        for container in containers:

            state = (
                container.attrs
                .get(
                    "State",
                    {}
                )
            )

            health = (
                state
                .get(
                    "Health",
                    {}
                )
                .get(
                    "Status"
                )
            )

            if health in [

                "unhealthy",

                "starting",
            ]:

                unhealthy.append({

                    "container":
                        container.name,

                    "health":
                        health,
                })

        return success(
            unhealthy
        )

    except Exception as ex:

        return failure(
            str(ex)
        )