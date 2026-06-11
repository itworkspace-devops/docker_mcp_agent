import uuid

DANGEROUS_TOOLS = {

    "docker_restart",

    "docker_stop",

    "docker_rm",

    "docker_rmi",
}


def requires_approval(
    tool_name,
):

    return (
        tool_name
        in
        DANGEROUS_TOOLS
    )


def create_execution_id():

    return str(
        uuid.uuid4()
    )