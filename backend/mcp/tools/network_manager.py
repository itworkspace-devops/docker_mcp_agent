from backend.mcp.docker_client import get_docker
from backend.mcp.tools.base import success, failure


def docker_network_ls(arguments):
    try:
        client = get_docker(arguments.get("host_name"))
        return success([{"id": n.id, "name": n.name, "driver": n.attrs.get("Driver")} for n in client.networks.list()], message="Listed networks.")
    except Exception as ex:
        return failure(str(ex))


def docker_network_inspect(arguments):
    try:
        client = get_docker(arguments.get("host_name"))
        return success(client.networks.get(arguments["network"]).attrs, message="Inspected network.")
    except Exception as ex:
        return failure(str(ex))


def docker_network_create(arguments):
    try:
        client = get_docker(arguments.get("host_name"))
        network = client.networks.create(arguments["name"], driver=arguments.get("driver", "bridge"))
        return success({"id": network.id, "name": network.name}, message="Created network.")
    except Exception as ex:
        return failure(str(ex))


def docker_network_rm(arguments):
    try:
        client = get_docker(arguments.get("host_name"))
        client.networks.get(arguments["network"]).remove()
        return success({"network": arguments["network"], "action": "removed"}, message="Removed network.")
    except Exception as ex:
        return failure(str(ex))


def docker_network_connect(arguments):
    try:
        client = get_docker(arguments.get("host_name"))
        client.networks.get(arguments["network"]).connect(arguments["container"])
        return success({"network": arguments["network"], "container": arguments["container"]}, message="Connected container to network.")
    except Exception as ex:
        return failure(str(ex))


def docker_network_disconnect(arguments):
    try:
        client = get_docker(arguments.get("host_name"))
        client.networks.get(arguments["network"]).disconnect(arguments["container"])
        return success({"network": arguments["network"], "container": arguments["container"]}, message="Disconnected container from network.")
    except Exception as ex:
        return failure(str(ex))


def docker_network_prune(arguments):
    try:
        client = get_docker(arguments.get("host_name"))
        return success(client.networks.prune(), message="Pruned unused networks.")
    except Exception as ex:
        return failure(str(ex))
