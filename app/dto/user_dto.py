from dataclasses import dataclass


@dataclass
class JwtResponseDto:
    jwt: str
    name: str


@dataclass
class UserDto:
    id: int
    name: str


@dataclass
class UserRegistrationDto:
    name: str
    email: str
    password: str


@dataclass
class UserLoginDto:
    email: str
    password: str
