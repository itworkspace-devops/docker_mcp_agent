import docker
from .config import settings
from backend.database.repository import get_host_by_name

_clients = {}

def get_docker(host_name=None):
    global _clients
    
    base_url = None
    
    # Use "local" if host_name is None or "local"
    if not host_name or host_name == "local":
        base_url = settings.docker_host if settings.docker_host != "none" else None
    else:
        host_record = get_host_by_name(host_name)
        if host_record:
            # Construct base_url from host and port
            h = host_record.host
            p = host_record.port
            
            # If h is literally "none" or empty, treat as invalid for a remote host
            if not h or h.lower() == "none":
                base_url = None
            elif h.startswith("/") or h.startswith("unix://"):
                base_url = h
            elif h.startswith("//./pipe"):
                base_url = f"npipe://{h}"
            elif h.startswith("npipe://"):
                base_url = h
            elif "://" in h:
                base_url = h
                if p and ":" not in h.split("://")[1]:
                    base_url = f"{h}:{p}"
            else:
                base_url = f"tcp://{h}:{p}" if p else f"tcp://{h}:2375"
    
    # Final default if nothing resolved
    if not base_url:
        import os
        if os.name == 'nt':
            base_url = "npipe:////./pipe/docker_engine"
        else:
            base_url = "unix:///var/run/docker.sock"

    print(f"DEBUG: get_docker(host_name={host_name}) -> base_url={base_url}")

    if base_url not in _clients:
        try:
            _clients[base_url] = docker.DockerClient(base_url=base_url, timeout=10)
        except Exception as e:
            print(f"Failed to initialize docker client for {base_url}: {e}")
            # Don't cache failed clients, or maybe cache failure?
            return docker.DockerClient(base_url=base_url, timeout=10) # Let it raise if it fails again

    return _clients[base_url]