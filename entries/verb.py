from enum import Enum


class VerbType(Enum):
    REGULAR = 1
    IRREGULAR = 2
    MODAL = 3
    SEPARABLE = 4


class Verb():
    def __init__(self, the_entry):
        self.entry = the_entry
        self.sub_type = None
        self.infinitive = ''
        self.perfekt = ''
        self.partizip_I = ''
        self.partizip_II = ''
