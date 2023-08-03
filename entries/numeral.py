from enum import Enum


class NumeralType(Enum):
    CARDINAL = 1
    ORDINAL = 2
    MULTIPLICATIVE = 3
    ITERATIVE = 4
    FRACTION = 5
    SAME_KIND = 6
    COLLECTIVE = 7
    INDEFINITE = 8


class Numeral():
    def __init__(self, original_text):
        super().__init__(original_text)
        self.type = None
        self.decode()

    def decode(self):
        pass
