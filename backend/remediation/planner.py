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
        
    
def create_plan(finding):

    message = finding["message"]

    if finding["category"] == "container":

        container = message.split()[0]

        return {

            "tool_name":
                "docker_restart",

            "tool_args": {

                "container":
                    container
            }
        }

    return None