# To run in venv : spacy-ner
import spacy
nlp = spacy.load("it_core_news_md")

piano_class_text = None

with open("compiled-data/transcription-val.txt") as file:
    piano_class_text = file.read() 


piano_class_doc = nlp(piano_class_text)

for ent in piano_class_doc.ents:
    print(f"{ent.text = } {ent.start_char = } {ent.end_char = } {ent.label_ = } spacy.explain('{ent.label_}') = {spacy.explain(ent.label_)}")
