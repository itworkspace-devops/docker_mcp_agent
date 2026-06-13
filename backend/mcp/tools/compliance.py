from backend.compliance.service import (
    run_compliance_scan
)

from backend.mcp.tools.base import (
    success,
    failure
)


def compliance_scan(arguments):

    try:

        return success(
            run_compliance_scan()
        )

    except Exception as ex:

        return failure(
            str(ex)
        )