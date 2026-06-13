import json
import shlex
import subprocess
from pathlib import Path

from langchain_ollama import ChatOllama

from backend.config.settings import settings
from backend.mcp.docker_client import get_docker
from backend.mcp.tools.base import success, failure

llm = ChatOllama(
    model=settings.ollama_model,
    base_url=settings.ollama_url,
    temperature=0,
)


def _build_spec_prompt(request: str, spec_type: str) -> str:
    if spec_type == "dockerfile":
        description = (
            "Generate a Dockerfile for a single service application based on the user request. "
            "Do not produce docker-compose content."
        )
    else:
        description = (
            "Generate a docker-compose.yml for a requested multi-service or orchestrated stack. "
            "Use compose only when the request is explicitly about docker-compose or multiple services."
        )

    return f"""
You are a Docker spec generator.

{description}

Return ONLY valid JSON with the following keys:
  - file_name: string
  - file_contents: string
  - explanation: string

Do not return markdown, code fences, or any text outside the JSON object.
Do not perform any Docker actions; only generate the requested spec.

User request:
{request}
"""


def _parse_llm_json(content: str) -> dict:
    try:
        return json.loads(content)
    except Exception as ex:
        raise ValueError(
            "Failed to parse LLM response as JSON. "
            f"Response was: {content!r}. Error: {ex}"
        )


def _write_file(output_dir: str, file_name: str, contents: str) -> Path:
    output_path = Path(output_dir or ".").resolve() / file_name
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(contents, encoding="utf-8")
    return output_path


def generate_dockerfile(arguments):
    try:
        request = arguments["request"]
        output_dir = arguments.get("output_dir", ".")
        file_name = arguments.get("file_name", "Dockerfile")

        prompt = _build_spec_prompt(request, "dockerfile")
        response = llm.invoke(prompt).content.strip()
        spec = _parse_llm_json(response)

        file_contents = spec.get("file_contents")
        if not file_contents:
            return failure("LLM returned an empty Dockerfile content.")

        path = _write_file(output_dir, file_name, file_contents)

        return success(
            {
                "file_name": str(path.name),
                "path": str(path),
                "content": file_contents,
                "explanation": spec.get("explanation", "Generated Dockerfile."),
            }
        )

    except Exception as ex:
        return failure(str(ex))


def generate_compose(arguments):
    try:
        request = arguments["request"]
        output_dir = arguments.get("output_dir", ".")
        file_name = arguments.get("file_name", "docker-compose.yml")

        prompt = _build_spec_prompt(request, "compose")
        response = llm.invoke(prompt).content.strip()
        spec = _parse_llm_json(response)

        file_contents = spec.get("file_contents")
        if not file_contents:
            return failure("LLM returned an empty docker-compose content.")

        path = _write_file(output_dir, file_name, file_contents)

        return success(
            {
                "file_name": str(path.name),
                "path": str(path),
                "content": file_contents,
                "explanation": spec.get("explanation", "Generated docker-compose.yml."),
            }
        )

    except Exception as ex:
        return failure(str(ex))


def execute_dockerfile(arguments):
    try:
        request = arguments.get("request")
        output_dir = arguments.get("output_dir", ".")
        dockerfile_name = arguments.get("dockerfile_name", "Dockerfile")
        dockerfile_path = Path(output_dir).resolve() / dockerfile_name
        build_context = Path(arguments.get("context", output_dir)).resolve()
        tag = arguments.get("tag", "generated_docker_image")
        run_container = arguments.get("run", True)
        name = arguments.get("name")
        run_args = arguments.get("run_args", {}) or {}

        if not dockerfile_path.exists():
            if not request:
                return failure("Dockerfile does not exist and no request was provided to generate one.")

            generate_result = generate_dockerfile(
                {
                    "request": request,
                    "output_dir": output_dir,
                    "file_name": dockerfile_name,
                }
            )
            if not generate_result["success"]:
                return failure(generate_result["error"])

        docker_client = get_docker()
        build_result = docker_client.images.build(
            path=str(build_context),
            tag=tag,
            dockerfile=str(dockerfile_path.name),
            rm=True,
            pull=True,
        )

        image_info = {
            "tag": tag,
            "build_result": str(build_result[0].id if build_result else "unknown"),
        }

        if not run_container:
            return success(
                {
                    "action": "built",
                    "image": image_info,
                    "dockerfile_path": str(dockerfile_path),
                }
            )

        run_kwargs = {
            "image": tag,
            "detach": True,
        }
        if name:
            run_kwargs["name"] = name

        if "ports" in run_args:
            run_kwargs["ports"] = run_args["ports"]
        if "environment" in run_args:
            run_kwargs["environment"] = run_args["environment"]
        if "volumes" in run_args:
            run_kwargs["volumes"] = run_args["volumes"]

        container = docker_client.containers.run(**run_kwargs)

        return success(
            {
                "action": "built_and_run",
                "image": image_info,
                "container": {
                    "id": container.short_id,
                    "name": container.name,
                },
                "dockerfile_path": str(dockerfile_path),
            }
        )

    except Exception as ex:
        return failure(str(ex))


def execute_compose(arguments):
    try:
        request = arguments.get("request")
        output_dir = arguments.get("output_dir", ".")
        compose_name = arguments.get("compose_name", "docker-compose.yml")
        compose_path = Path(output_dir).resolve() / compose_name
        action = arguments.get("action", "up")
        service = arguments.get("service")
        build_flag = arguments.get("build", False)

        if not compose_path.exists():
            if not request:
                return failure("docker-compose.yml does not exist and no request was provided to generate one.")

            generate_result = generate_compose(
                {
                    "request": request,
                    "output_dir": output_dir,
                    "file_name": compose_name,
                }
            )
            if not generate_result["success"]:
                return failure(generate_result["error"])

        command = ["docker", "compose", "-f", str(compose_path)]
        if action == "up":
            command += ["up", "-d"]
            if build_flag:
                command.append("--build")
            if service:
                command.append(service)
        elif action == "down":
            command += ["down"]
        elif action == "build":
            command += ["build"]
            if service:
                command.append(service)
        else:
            return failure(f"Unsupported compose action: {action}")

        process = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False,
        )

        if process.returncode != 0:
            return failure(
                {
                    "command": " ".join(shlex.quote(part) for part in command),
                    "stdout": process.stdout,
                    "stderr": process.stderr,
                }
            )

        return success(
            {
                "action": action,
                "compose_path": str(compose_path),
                "stdout": process.stdout,
                "stderr": process.stderr,
            }
        )

    except Exception as ex:
        return failure(str(ex))
