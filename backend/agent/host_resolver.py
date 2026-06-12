from backend.hosts.selector import (
    extract_host
)


def host_resolver(
    state
):

    host = extract_host(
        state["query"]
    )

    return {
        "host": host
    }