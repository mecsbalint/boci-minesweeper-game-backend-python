from typing import Any, Type, TypeVar
from dataclasses import asdict, is_dataclass
from app.error_handling.exceptions import InvalidRequestFieldsException, InvalidRequestFormException

T = TypeVar("T")


def validate_request_body(payload: dict[Any, Any], payload_cls: Type[T], *items: tuple[str, type]) -> T:

    if not is_dataclass(payload_cls):
        raise TypeError("payload_cls has to be a dataclass type")

    try:
        data = payload_cls(*payload)  # pyright: ignore[reportUnknownArgumentType]
    except TypeError:
        raise InvalidRequestFormException()

    error_names: set[str] = set()
    data_dict = asdict(data)
    for key, type in items:
        data_member = data_dict[key]
        if not data_member or not isinstance(data_member, type):
            error_names.add(key)
    if error_names:
        raise InvalidRequestFieldsException(error_names)

    return data
