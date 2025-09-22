from app.dto.dto_base_model import DtoBaseModel


class ErrorDetailDto(DtoBaseModel):
    code: str
    message: str
