from backend.mcp.docker_client import get_docker
from backend.mcp.tools.base import success, failure
import shutil
import subprocess


def scan_image_vulnerabilities(arguments):
    try:
        image = arguments["image"]
        if not shutil.which("trivy"):
            return success({"image": image, "scanner": "trivy", "note": "Trivy not installed on this host."}, message="Vulnerability scan skipped.")
        result = subprocess.run(["trivy", "image", "--quiet", image], capture_output=True, text=True, timeout=300)
        return success({"image": image, "output": result.stdout or result.stderr}, message="Vulnerability scan completed.")
    except Exception as ex:
        return failure(str(ex))


def list_image_labels(arguments):
    try:
        client = get_docker(arguments.get("host_name"))
        image = client.images.get(arguments["image"])
        attrs = image.attrs
        config = attrs.get("Config", {})
        return success(
            {
                "image": arguments["image"],
                "user": config.get("User"),
                "labels": config.get("Labels") or {},
                "exposed_ports": list((config.get("ExposedPorts") or {}).keys()),
            },
            message="Collected image metadata."
        )
    except Exception as ex:
        return failure(str(ex))
