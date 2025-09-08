from pydantic import BaseModel


class ExceptionDto(BaseModel):
    code: str
    message: str
