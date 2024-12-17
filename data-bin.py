from SPACY_DATA import TRAIN_DATA

import warnings
from pathlib import Path

import spacy
from spacy.tokens import DocBin

def convert(lang: str, TRAIN_DATA, output_path: Path):
    nlp = spacy.blank(lang)
    db = DocBin()
    for text, annot in TRAIN_DATA:
        doc = nlp.make_doc(text)
        ents = []
        for start, end, label in annot["entities"]:
            span = doc.char_span(start, end, label=label)
            if span is None:
                msg = f"Skipping entity [{start}, {end}, {label}] in the following text because the character span '{doc.text[start:end]}' does not align with token boundaries:\n\n{repr(text)}\n"
                warnings.warn(msg)
            else:
                ents.append(span)
        doc.ents = ents
        db.add(doc)
    db.to_disk(output_path)

# Same data for train and validation just to test the pipeline

convert("it", TRAIN_DATA[:int(len(TRAIN_DATA)/2)], "compiled-data/train.spacy")
convert("it", TRAIN_DATA[int(len(TRAIN_DATA)/2):], "compiled-data/valid.spacy")