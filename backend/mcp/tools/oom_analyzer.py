from backend.mcp.docker_client import get_docker
from backend.mcp.tools.base import success, failure


def detect_oom_containers(arguments):
    try:
        client = get_docker(arguments.get("host_name"))
        rows = []
        for c in client.containers.list(all=True):
            attrs = c.attrs or {}
            if attrs.get("State", {}).get("OOMKilled"):
                rows.append({"container": c.name, "id": c.short_id, "status": c.status})
        return success(rows, message="Detected OOM-killed containers.")
    except Exception as ex:
        return failure(str(ex))


def get_memory_usage(arguments):
    try:
        client = get_docker(arguments.get("host_name"))
        c = client.containers.get(arguments["container"])
        stats = c.stats(stream=False)
        mem_usage = stats.get("memory_stats", {}).get("usage", 0)
        mem_limit = stats.get("memory_stats", {}).get("limit", 0) or 1
        percent = round((mem_usage / mem_limit) * 100, 2)
        risk = "HIGH" if percent >= 80 else "MEDIUM" if percent >= 50 else "LOW"
        return success({"container": c.name, "memory_percent": percent, "risk": risk}, message="Measured memory usage.")
    except Exception as ex:
        return failure(str(ex))
