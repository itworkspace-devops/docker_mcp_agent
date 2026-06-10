from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"  # Ignore unknown env vars
    )

    # Ollama
    ollama_url: str = "http://localhost:11434"
    ollama_model: str = "llama3.1:latest"

    # MCP
    mcp_host: str = "192.168.29.225"
    mcp_port: int = 8001

    # Docker
    # docker_host: str = "unix:///var/run/docker.sock"
    docker_host: str = "npipe:////./pipe/docker_engine"


settings = Settings()