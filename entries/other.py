from enum import Enum


class OtherType(Enum):
    UNKNOWN = 1
    INTERJECTION = 2
    CONJUNCTION = 3
    PARTICLE = 4
    PHRASE = 5


class Other:
    def __init__(self, text):
        self.type = None
        self.string = text
        self.decode()

    def decode(self):
        print("Decoding Other entry type")
        self.type = OtherType.UNKNOWN

    def get_print(self):
        return f"{self.type}{self.string}  <--  {self.string}"

