
class ApiException(Exception):
    def __init__(self, status: int, errors: dict[str, str]) -> None:
        super().__init__()
        self.status = status
        self.errors = errors

    def to_dict(self):
        return self.errors


class ApiRequestException(ApiException):
    pass


class InvalidRequestFormException(ApiRequestException):
    def __init__(self) -> None:
        super().__init__(400, {"INVALID_REQUEST_BODY": "The request body is in an invalid form"})


class InvalidRequestFieldsException(ApiRequestException):
    def __init__(self, error_names: set[str]) -> None:
        errors: dict[str, str] = {}
        for error_name in error_names:
            error_code = f"INVALID_{error_name.upper()}"
            error_msg = f"{error_name.capitalize()} is missing from request body or in is a wrong format"
            errors[error_code] = error_msg
        super().__init__(400, errors)
