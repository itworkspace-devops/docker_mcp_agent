from backend.cli.renderers.container_renderer import (
    render_containers
)

from backend.cli.renderers.image_renderer import (
    render_images
)

from backend.cli.renderers.system_renderer import (
    render_system
)


def format_result(result):

    if not result:

        return result

    if not result.get(
        "success",
        False
    ):
        return result

    data = result.get(
        "data"
    )

    if isinstance(data, list):

        if len(data):

            first = data[0]

            if "status" in first:

                return render_containers(
                    data
                )

            if "tags" in first:

                return render_images(
                    data
                )

    if isinstance(data, dict):

        return render_system(
            data
        )

    return data