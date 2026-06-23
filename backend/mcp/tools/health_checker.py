from backend.mcp.docker_client import get_docker
from backend.mcp.tools.base import success, failure


def check_container_health(arguments):
    try:
        client = get_docker(arguments.get("host_name"))
        c = client.containers.get(arguments["container"])
        health = (c.attrs.get("State", {}) or {}).get("Health", {})
        return success({"container": c.name, "status": c.status, "health": health}, message="Checked container health.")
    except Exception as ex:
        return failure(str(ex))


def list_all_health_statuses(arguments):
    try:
        client = get_docker(arguments.get("host_name"))
        rows = []
        for c in client.containers.list(all=True):
            health = (c.attrs.get("State", {}) or {}).get("Health", {})
            rows.append({"container": c.name, "status": c.status, "health": health.get("Status", "unknown")})
        return success(rows, message="Listed health statuses.")
    except Exception as ex:
        return failure(str(ex))
