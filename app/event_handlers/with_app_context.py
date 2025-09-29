from typing import Callable, ParamSpec, TypeVar
from flask import current_app


R = TypeVar("R")
P = ParamSpec("P")


def with_app_context(func: Callable[P, R]) -> Callable[P, R]:
    def with_app_context_wrapper(*args: P.args, **kwargs: P.kwargs):
        with current_app.app_context():
            return func(*args, **kwargs)
    return with_app_context_wrapper
