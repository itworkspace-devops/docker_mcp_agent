from backend.mcp.docker_client import get_docker
from backend.mcp.tools.base import success, failure


def list_dangling_images(arguments):
    try:
        client = get_docker(arguments.get("host_name"))
        images = client.images.list(filters={"dangling": True})
        return success([{"id": img.short_id, "tags": img.tags} for img in images], message="Listed dangling images.")
    except Exception as ex:
        return failure(str(ex))


def prune_images(arguments):
    try:
        client = get_docker(arguments.get("host_name"))
        result = client.images.prune()
        return success(result, message="Pruned unused images.")
    except Exception as ex:
        return failure(str(ex))


def prune_containers(arguments):
    try:
        client = get_docker(arguments.get("host_name"))
        result = client.containers.prune()
        return success(result, message="Pruned stopped containers.")
    except Exception as ex:
        return failure(str(ex))


def prune_volumes(arguments):
    try:
        client = get_docker(arguments.get("host_name"))
        result = client.volumes.prune()
        return success(result, message="Pruned unused volumes.")
    except Exception as ex:
        return failure(str(ex))


def system_prune(arguments):
    try:
        client = get_docker(arguments.get("host_name"))
        result = client.api.prune_system()
        return success(result, message="System prune completed.")
    except Exception as ex:
        return failure(str(ex))
