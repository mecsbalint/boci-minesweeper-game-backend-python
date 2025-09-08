from pydantic import BaseModel


class JwtResponseDto(BaseModel):
    jwt: str
    name: str


class UserDto(BaseModel):
    id: int
    name: str


class UserRegistrationDto(BaseModel):
    name: str
    email: str
    password: str


class UserLoginDto(BaseModel):
    email: str
    password: str
