def remediation_plan(finding):

    message = finding["message"]

    # Stopped container
    if "is stopped" in message:

        container = (
            message
            .replace("Container ", "")
            .replace(" is stopped", "")
        )

        return {
            "tool_name": "docker_restart",
            "tool_args": {
                "container": container
            }
        }

    return None