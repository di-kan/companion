from entries.adjective import Adjective
from entries.adverb import Adverb
from entries.article import Article
from entries.noun import Noun
from entries.numeral import Numeral
from entries.other import Other
from entries.preposition import Preposition
from entries.verb import Verb


class Line:
    def __init__(self, text, language_from="german", language_to="greek", separator=":"):
        self.text = text
        self.text_from = ""
        self.text_to = ""
        self.separator = separator
        self.page = 0
        self.language_from = language_from
        self.language_to = language_to
        self._decode()

    def _decode(self):
        try:
            self.page = int(self.text.split(self.separator)[0])
            self.text_from = self.text.split(self.separator)[1]
            self.text_to = self.text.split(self.separator)[2]
        except Exception as e:
            print(f"ERROR _decode, {e}")

    def __str__(self):
        return f"{self.page}|{self.text_from}|{self.text_to}"


class Entry:
    part_of_speech_map = {'adjective': Adjective,
                          'adverb': Adverb,
                          'article': Article,
                          'noun': Noun,
                          'numeral': Numeral,
                          'other': Other,
                          'preposition': Preposition,
                          'verb': Verb}

    def __init__(self, original_text):
        self.line = Line(original_text)
        self.type = None

    def __str__(self):
        message = str(self.line)
        if self.type:
            message += f"|{str(self.type)}"
        else:
            message += "|Unknown"
        return message

    def set_type(self, part_of_speech):
        self.type = Entry.part_of_speech_map[part_of_speech](self)
