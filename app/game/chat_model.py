

class Chat:
    def __init__(self, participant_names: set[str]):
        self._participant_names = participant_names
        self._messages: list[tuple[str, str]] = []

    @property
    def messages(self):
        return self._messages

    @property
    def participant_names(self):
        return self._participant_names

    def add_message(self, message: tuple[str, str]):
        if message[0] in self._participant_names:
            self._messages.append(message)

    def add_participant(self, participant_name: str):
        self._participant_names.add(participant_name)

    def remove_participant(self, participant_name: str):
        self.participant_names.discard(participant_name)
