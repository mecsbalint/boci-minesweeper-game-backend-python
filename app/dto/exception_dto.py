from pydantic import BaseModel


class ErrorDetailDto(BaseModel):
    code: str
    message: str
