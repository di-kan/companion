from enum import Enum


class ArticleType(Enum):
    DEFINITE = 1
    INDEFINITE = 2


class Article():
    def __init__(self, original_text):
        super().__init__(original_text)
        self.type = None
        self.singular = ''
        self.plural = ''
        self.decode()

    def decode(self):
        pass
