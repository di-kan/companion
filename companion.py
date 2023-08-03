from entries.entry import Entry


class Companion:
    def __init__(self):
        self.entries = []
        self.filtered = []

    def import_file(self, filename):
        with open(filename) as f:
            self.entries = [Entry(line.strip()) for line in f if len(line)>5]

    def print(self):
        for entry in self.entries:
            print(str(entry))

    def empty_filter(self):
        self.filtered = []
        
    def filter_contains(self, text):
        self.empty_filter()
        for index, entry in enumerate(self.entries):
            if text.lower() in entry.line.text.lower():
                self.filtered.append(index)

    def filter_length(self, length, type="min"):
        self.empty_filter()
        if type == "min":
            for index, entry in enumerate(self.entries):
                if len(entry.line.text_from) <= length:
                    self.filtered.append(index)
        else:
            for index, entry in enumerate(self.entries):
                if len(entry.line.text_from) > length:
                    self.filtered.append(index)

    def filter_starts_ends(self, start_text="", end_text=""):
        self.empty_filter()
        for index, entry in enumerate(self.entries):
            if entry.line.text_from.startswith(start_text) and entry.line.text_from.endswith(end_text):
                self.filtered.append(index)

    def get_filtered(self):
        results = []
        for index in self.filtered:
            results.append(self.entries[index])
        return results