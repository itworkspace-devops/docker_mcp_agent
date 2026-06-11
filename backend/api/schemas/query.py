from pydantic import BaseModel


class QueryRequest(BaseModel):

    query: str


class QueryResponse(BaseModel):

    success: bool

    response: dict | list | str