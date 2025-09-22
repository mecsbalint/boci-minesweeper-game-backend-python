from app.dto.dto_base_model import DtoBaseModel


class JwtResponseDto(DtoBaseModel):
    jwt: str
    name: str


class UserDto(DtoBaseModel):
    id: int
    name: str


class UserRegistrationDto(DtoBaseModel):
    name: str
    email: str
    password: str


class UserLoginDto(DtoBaseModel):
    email: str
    password: str
