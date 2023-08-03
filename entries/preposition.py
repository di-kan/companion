from enum import Enum


class PrepositionType(Enum):
    LOCAL = 1
    TEMPORAL = 2
    MODAL = 3
    CASUAL = 4


class Preposition():
    def __init__(self, original_text):
        super().__init__(original_text)
        self.type = None
        self.decode()

    def decode(self):
        pass