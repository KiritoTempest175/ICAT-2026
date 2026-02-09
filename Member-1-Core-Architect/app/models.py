from pydantic import BaseModel

class ProcessResponse(BaseModel):
    filename: str
    content: str
    message: str
