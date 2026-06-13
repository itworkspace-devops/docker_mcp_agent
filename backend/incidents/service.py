from backend.incidents.diagnostics import (
    collect_diagnostics
)

from backend.incidents.analyzer import (
    analyze_incident
)

from backend.incidents.report import (
    build_report
)


def investigate_container(
    container
):

    diagnostics = collect_diagnostics(
        container
    )

    analysis = analyze_incident(
        diagnostics
    )

    return build_report(

        container,

        diagnostics,

        analysis,
    )