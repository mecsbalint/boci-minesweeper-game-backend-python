from uuid import UUID
from pydantic import BaseModel


def to_camel_case(var_name: str) -> str:
    name_parts = var_name.split("_")
    return name_parts[0] + "".join([part.capitalize() for part in name_parts[1:]])


class DtoBaseModel(BaseModel):

    class Config:
        alias_generator = to_camel_case
        validate_by_name = True
