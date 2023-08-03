from companion import Companion


filename = "voc.csv"
comp = Companion()
comp.import_file(filename)

comp.filter_starts_ends(end_text="?")
for entry in comp.get_filtered():
    print(entry.line.text_from)
