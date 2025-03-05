class Player:
    def __init__(self, name: str):
        self._name: str = name[:25]

    @property
    def name(self) -> str:
        return self._name
