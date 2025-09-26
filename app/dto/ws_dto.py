from pydantic import BaseModel


class WSAuthDto(BaseModel):
    jwt: str
