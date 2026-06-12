def calculate_cpu_percent(
    stats
):

    cpu_delta = (

        stats["cpu_stats"][
            "cpu_usage"
        ]["total_usage"]

        -

        stats["precpu_stats"][
            "cpu_usage"
        ]["total_usage"]
    )

    system_delta = (

        stats["cpu_stats"][
            "system_cpu_usage"
        ]

        -

        stats["precpu_stats"][
            "system_cpu_usage"
        ]
    )

    if system_delta <= 0:

        return 0

    return round(

        (
            cpu_delta
            /
            system_delta
        )
        * 100,

        2,
    )