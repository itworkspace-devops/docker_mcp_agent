from backend.database.repository import (
    create_host,
    get_hosts,
    get_host_by_name,
    update_host_record,
    delete_host_record,
)

import requests


import docker
import requests

def get_docker_host(
    host_name,
):
    host = get_host_by_name(
        host_name
    )

    if not host:
        raise Exception(
            f"Host '{host_name}' not found"
        )

    h = host.host
    p = host.port
    
    if h.startswith("/") or h.startswith("unix://"):
        return h
    elif h.startswith("//./pipe"):
        return f"npipe://{h}"
    elif h.startswith("npipe://"):
        return h
    elif "://" in h:
        url = h
        if p and ":" not in h.split("://")[1]:
            url = f"{h}:{p}"
        return url
    else:
        return f"tcp://{h}:{p}" if p else f"tcp://{h}:2375"

def test_host_connectivity(
    host,
    port,
):
    try:
        # Construct base_url
        if host.startswith("/") or host.startswith("unix://"):
            base_url = host
        elif host.startswith("//./pipe"):
            base_url = f"npipe://{host}"
        elif host.startswith("npipe://"):
            base_url = host
        elif "://" in host:
            base_url = host
            if port and ":" not in host.split("://")[1]:
                base_url = f"{host}:{port}"
        else:
            base_url = f"tcp://{host}:{port}" if port else f"tcp://{host}:2375"

        client = docker.DockerClient(base_url=base_url, timeout=5)
        client.ping()

        return {
            "success": True,
            "message": "Connectivity test passed!"
        }

    except Exception as e:

        return {
            "success": False,
            "message": str(e)
        }


def register_host(
    name,
    host,
    port,
):
    return create_host(
        name,
        host,
        port,
    )


def list_hosts():
    return get_hosts()


def update_host(
    host_id,
    name,
    host,
    port,
    enabled=True,
):
    return update_host_record(
        host_id,
        name,
        host,
        port,
        enabled,
    )


def remove_host(
    host_id,
):
    return delete_host_record(
        host_id
    )