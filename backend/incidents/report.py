def build_report(
    container,
    diagnostics,
    analysis,
):

    return {

        "container":
            container,

        "analysis":
            analysis,

        "logs_preview":

            str(
                diagnostics.get(
                    "logs",
                    ""
                )
            )[:500],

        "generated":
            True,
    }