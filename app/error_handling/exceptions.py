
class ApiException(Exception):
    def __init__(self, status: int, *errors: dict[str, str]) -> None:
        super().__init__()
        self._status = status
        self._errors = errors

    @property
    def errors(self):
        return self._errors

    @property
    def status(self):
        return self._status
