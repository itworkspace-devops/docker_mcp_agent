from backend.drift.service import (
    run_drift_scan
)

from backend.mcp.tools.base import (
    success,
    failure
)


def drift_scan(arguments):

    try:

        return success(
            run_drift_scan()
        )

    except Exception as ex:

        return failure(
            str(ex)
        )