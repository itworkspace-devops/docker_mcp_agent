from backend.mcp.docker_client import get_docker
from backend.mcp.tools.base import success, failure


def list_images(arguments):

    try:

        client = get_docker()

        images = client.images.list()

        result = []

        for image in images:

            result.append(
                {
                    "id": image.short_id,
                    "tags": image.tags,
                }
            )

        return success(result)

    except Exception as ex:

        return failure(str(ex))


def pull_image(arguments):

    try:

        image_name = arguments["image"]

        image = get_docker().images.pull(
            image_name
        )

        return success(
            {
                "image": image_name,
                "id": image.short_id,
                "tags": image.tags,
            }
        )

    except Exception as ex:

        return failure(str(ex))


def remove_image(arguments):

    try:

        image_name = arguments["image"]

        force = arguments.get(
            "force",
            False
        )

        get_docker().images.remove(
            image=image_name,
            force=force
        )

        return success(
            {
                "image": image_name,
                "action": "removed"
            }
        )

    except Exception as ex:

        return failure(str(ex))