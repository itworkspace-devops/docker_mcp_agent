from pydantic import BaseModel


class QueryRequest(BaseModel):

    query: str
    
    session_id: str | None = None
    host_name: str | None = None


class QueryResponse(BaseModel):

    success: bool

    response: dict | list | str
