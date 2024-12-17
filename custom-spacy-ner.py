import spacy

trained_nlp = spacy.load("models/output/model-best")
text = None
with open("compiled-data/transcription-val.txt") as file:
    text = file.read()
doc = trained_nlp(text)

for ent in doc.ents:
    print(f"{ent.text = } {ent.start_char = } {ent.end_char = } {ent.label_ = } ")
