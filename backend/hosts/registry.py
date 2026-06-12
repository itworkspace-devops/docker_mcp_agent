HOSTS = {

    "local": {
        "docker_host":
            "npipe:////./pipe/docker_engine"
    },

    "dev": {
        "docker_host":
            "tcp://10.0.0.10:2375"
    },

    "qa": {
        "docker_host":
            "tcp://10.0.0.11:2375"
    },

    "prod": {
        "docker_host":
            "tcp://10.0.0.12:2375"
    },
}