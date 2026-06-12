from backend.database.repository import (
    create_host,
    get_hosts,
)


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