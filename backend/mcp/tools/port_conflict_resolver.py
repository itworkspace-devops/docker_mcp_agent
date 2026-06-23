from __future__ import annotations

from backend.mcp.docker_client import get_docker
from backend.mcp.tools.base import success, failure


def list_port_mappings(arguments):
    try:
        host_name = arguments.get("host_name")
        client = get_docker(host_name)
        rows = []
        for c in client.containers.list(all=True):
            ports = (c.attrs or {}).get("NetworkSettings", {}).get("Ports", {}) or {}
            for container_port, bindings in ports.items():
                for binding in bindings or []:
                    rows.append(
                        {
                            "container": c.name,
                            "host_ip": binding.get("HostIp"),
                            "host_port": binding.get("HostPort"),
                            "container_port": container_port,
                        }
                    )
        return success(rows, message="Collected all port mappings.")
    except Exception as ex:
        return failure(str(ex))


def detect_port_conflicts(arguments):
    try:
        mappings = list_port_mappings(arguments)
        if not mappings["success"]:
            return mappings
        seen = {}
        conflicts = []
        for row in mappings["data"]:
            key = f"{row['host_ip']}:{row['host_port']}"
            if key in seen:
                conflicts.append({"binding": key, "containers": [seen[key], row["container"]]})
            else:
                seen[key] = row["container"]
        return success(conflicts, message="Port conflict scan completed.")
    except Exception as ex:
        return failure(str(ex))


def find_free_port(arguments):
    try:
        start = int(arguments.get("start_port", 3000))
        end = int(arguments.get("end_port", start + 100))
        used = set()
        mappings = list_port_mappings(arguments)
        if mappings["success"]:
            used = {int(row["host_port"]) for row in mappings["data"] if str(row.get("host_port", "")).isdigit()}
        for port in range(start, end + 1):
            if port not in used:
                return success({"free_port": port}, message=f"Suggested free port: {port}")
        return failure("No free port found in the requested range.")
    except Exception as ex:
        return failure(str(ex))
