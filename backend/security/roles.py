ROLES = {

    "viewer": [

        "docker_ps",

        "docker_logs",

        "docker_images",

        "docker_info",

        "docker_version",
        "docker_metrics",
        "docker_top",
        "docker_unhealthy",
        "check_container_health",
        "list_all_health_statuses",
        "list_port_mappings",
        "detect_port_conflicts",
        "find_free_port",
        "detect_crash_loop",
        "detect_oom_containers",
        "get_memory_usage",
        "list_dangling_images",
        "list_image_labels",
        "docker_volume_ls",
        "docker_volume_inspect",
        "docker_volume_orphans",
        "docker_network_ls",
        "docker_network_inspect",
        "scan_image_vulnerabilities",
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
        "docker_network_connect",
        "docker_network_disconnect",
    ],

    "admin": [

        "*",
    ],
}
