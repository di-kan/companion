from enum import Enum
import re

class NounType(Enum):
    MALE = "der "
    FEMALE = "die "
    NEUTRAL = "das "
    PLURAL = "die "


class Noun():
    def __init__(self, the_entry):
        self.entry = the_entry
        self.singular = ''
        self.plural = ''
        self.sub_type = None
        self.plural_separator = ","
        self.try_decode()

    def _get_article(self):
        match self.sub_type:
            case NounType.MALE:
                return "der"
            case NounType.FEMALE:
                return "die"
            case NounType.NEUTRAL:
                return "das"

    def try_decode(self):
        the_string = self.entry.line.text_from
        if 'der ' in the_string.lower():
            self.sub_type = NounType.MALE
        if 'das ' in the_string.lower():
            self.sub_type = NounType.NEUTRAL
        if 'die ' in the_string.lower():
            self.sub_type = NounType.FEMALE
        if self.plural_separator in the_string:
            self.singular = the_string.split(self.plural_separator)[0].replace(self._get_article(), "")
            self.plural = re.sub(r".*-", self.singular, the_string.split(self.plural_separator)[1])
        else:
            self.singular = the_string.replace(self._get_article(), "")
            self.plural = self.singular

    def __str__(self):
        return f"{self.sub_type}\t{self._get_article()}{self.singular}|die {self.plural} <-- {self.entry.line.text_from}"
