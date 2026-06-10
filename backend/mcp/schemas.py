from pydantic import BaseModel

class ToolRequest(BaseModel):

    name: str

    arguments: dict = {}


class ToolResponse(BaseModel):

    success: bool

    data: dict | list | str | None = None

    error: str | None = None