from typing import Any, Type, TypeVar
from dataclasses import asdict, is_dataclass
from app.error_handling.exceptions import InvalidRequestFieldsException, InvalidRequestFormException

T = TypeVar("T")


def validate_request_body(payload: dict[str, Any], payload_cls: Type[T], *items: tuple[str, list[Any]]) -> T:

    if not is_dataclass(payload_cls):
        raise TypeError("payload_cls has to be a dataclass type")

    try:
        data = payload_cls(**payload)  # pyright: ignore[reportUnknownArgumentType]
    except TypeError:
        raise InvalidRequestFormException()

    data_dict = asdict(data)
    error_names: set[str] = set()
    for key, union in items:
        data_member = data_dict.get(key)
        if not __validate_item(data_member, union):
            error_names.add(key)
    if error_names:
        raise InvalidRequestFieldsException(error_names)

    return data


def __validate_item(value: Any, union: list[Any]) -> bool:
    if value is None and None not in union:
        return False
    for constituent in union:
        if isinstance(constituent, type) and isinstance(value, constituent):
            return True
        elif value == constituent:
            return True
    return False
