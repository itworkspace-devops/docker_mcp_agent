from backend.mcp.docker_client import get_docker
from backend.mcp.tools.base import success, failure


def docker_volume_ls(arguments):
    try:
        client = get_docker(arguments.get("host_name"))
        return success([{"name": v.name, "driver": v.attrs.get("Driver")} for v in client.volumes.list()], message="Listed volumes.")
    except Exception as ex:
        return failure(str(ex))


def docker_volume_inspect(arguments):
    try:
        client = get_docker(arguments.get("host_name"))
        return success(client.volumes.get(arguments["volume"]).attrs, message="Inspected volume.")
    except Exception as ex:
        return failure(str(ex))


def docker_volume_create(arguments):
    try:
        client = get_docker(arguments.get("host_name"))
        vol = client.volumes.create(name=arguments["name"], driver=arguments.get("driver", "local"))
        return success({"name": vol.name}, message="Created volume.")
    except Exception as ex:
        return failure(str(ex))


def docker_volume_rm(arguments):
    try:
        client = get_docker(arguments.get("host_name"))
        client.volumes.get(arguments["volume"]).remove(force=arguments.get("force", False))
        return success({"volume": arguments["volume"], "action": "removed"}, message="Removed volume.")
    except Exception as ex:
        return failure(str(ex))


def docker_volume_orphans(arguments):
    try:
        client = get_docker(arguments.get("host_name"))
        volumes = client.volumes.list()
        orphans = [v.name for v in volumes if not (v.attrs.get("UsageData") or {}).get("RefCount")]
        return success(orphans, message="Detected orphaned volumes.")
    except Exception as ex:
        return failure(str(ex))
