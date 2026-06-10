from backend.cli.renderers.container_renderer import (
    render_containers
)


def format_result(result):

    if not result:

        return "No data"

    data = result.get(
        "data",
        []
    )

    if isinstance(data, list):

        if len(data):

            if "status" in data[0]:

                return render_containers(
                    data
                )

    return result