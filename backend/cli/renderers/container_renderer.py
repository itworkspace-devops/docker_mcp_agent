from rich.table import Table


def render_containers(data):

    table = Table(
        title="Docker Containers"
    )

    table.add_column(
        "ID",
        style="cyan"
    )

    table.add_column(
        "Name",
        style="green"
    )

    table.add_column(
        "Status",
        style="yellow"
    )

    table.add_column(
        "Image",
        style="magenta"
    )

    for item in data:

        table.add_row(
            str(item.get("id", "")),
            str(item.get("name", "")),
            str(item.get("status", "")),
            ",".join(
                item.get("image", [])
            ),
        )

    return table