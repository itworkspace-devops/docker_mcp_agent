from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class MCPSettings(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

    docker_host: str = "npipe:////./pipe/docker_engine"

    mcp_host: str = "0.0.0.0"

    mcp_port: int = 8001


settings = MCPSettings()