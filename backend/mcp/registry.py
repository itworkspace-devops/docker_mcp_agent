from backend.mcp.tools.compliance import compliance_scan

from .tools.containers import (
    list_containers,
    inspect_container,
    start_container,
    stop_container,
    restart_container,
    remove_container,
    container_logs,
    container_stats,
    run_container,
)

from .tools.images import (
    list_images,
    pull_image,
    remove_image,
)

from .tools.system import (
    docker_info,
    docker_ping,
    docker_version,
)

from .tools.monitoring import (
    docker_metrics,
    docker_top,
    docker_unhealthy,
)

from .tools.incidents import (
    incident_investigate
)

from .tools.drift import (
    drift_scan
)

TOOL_REGISTRY = {

    # ==================================================
    # Containers
    # ==================================================

    "docker_ps": list_containers,

    "docker_inspect": inspect_container,

    "docker_start": start_container,

    "docker_stop": stop_container,

    "docker_restart": restart_container,

    "docker_rm": remove_container,

    "docker_logs": container_logs,

    "docker_stats": container_stats,
    
    "docker_run": run_container,

    "incident_investigate":
        incident_investigate,

    # ==================================================
    # Images
    # ==================================================

    "docker_images": list_images,

    "docker_pull": pull_image,

    "docker_rmi": remove_image,
    
    # =================================================
    # Docker System
    # =================================================
    
    # Monitoring

    "docker_metrics":
        docker_metrics,

    "docker_top":
        docker_top,

    "docker_unhealthy":
        docker_unhealthy,
        
    "drift_scan":
        drift_scan,
        
    "compliance_scan":
         compliance_scan,

    # ==================================================
    # System
    # ==================================================

    "docker_info": docker_info,

    "docker_ping": docker_ping,

    "docker_version": docker_version,
}


def get_registered_tools():
    """
    Return all registered MCP tool names.
    Used by:
    - API /tools endpoint
    - Future UI
    - Teams integrations
    """

    return sorted(
        TOOL_REGISTRY.keys()
    )


def get_tool(tool_name: str):
    """
    Return tool callable by name.
    """

    return TOOL_REGISTRY.get(
        tool_name
    )