ROLES = {

    "viewer": [

        "docker_ps",

        "docker_logs",

        "docker_images",

        "docker_info",

        "docker_version",
    ],

    "operator": [

        "docker_ps",

        "docker_logs",

        "docker_images",

        "docker_info",

        "docker_version",

        "docker_start",

        "docker_stop",

        "docker_restart",
    ],

    "admin": [

        "*",
    ],
}