from rich.table import Table


def render_system(data):

    table = Table(
        title="Docker System"
    )

    table.add_column("Property")
    table.add_column("Value")

    for key, value in data.items():

        table.add_row(
            str(key),
            str(value)
        )

    return table