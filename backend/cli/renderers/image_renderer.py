from rich.table import Table


def render_images(data):

    table = Table(
        title="Docker Images"
    )

    table.add_column(
        "ID",
        style="cyan"
    )

    table.add_column(
        "Tags",
        style="green"
    )

    for image in data:

        table.add_row(
            str(
                image.get(
                    "id",
                    ""
                )
            ),
            ",".join(
                image.get(
                    "tags",
                    []
                )
            ),
        )

    return table