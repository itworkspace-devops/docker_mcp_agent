from backend.hosts.service import (
    list_hosts,
)


def load_hosts():

    hosts = {}

    for host in list_hosts():

        if not host.enabled:
            continue

        hosts[
            host.name
        ] = {

            "host":
                host.host,

            "port":
                host.port,

            "docker_host":
                f"tcp://{host.host}:{host.port}",
        }
        print(f"Loaded host: {host.name} at {host.host}:{host.port}")
    return hosts


HOSTS = load_hosts()