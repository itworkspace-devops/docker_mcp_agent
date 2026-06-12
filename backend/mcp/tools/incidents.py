from backend.incidents.service import (
    investigate_container
)

from backend.mcp.tools.base import (
    success,
    failure
)


def incident_investigate(arguments):

    try:

        container = arguments.get(
            "container"
        )

        if not container:

            return failure(
                "container is required"
            )

        report = investigate_container(
            container
        )

        return success(
            report
        )

    except Exception as ex:

        return failure(
            str(ex)
        )