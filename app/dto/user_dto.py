from dataclasses import dataclass


@dataclass
class JwtResponseDto:
    jwt: str
    name: str


@dataclass
class UserDto:
    id: int
    name: str
