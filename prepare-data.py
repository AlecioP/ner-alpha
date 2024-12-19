# v1 -> Store paths as variables
#ANNOTATIONS_FILE = "./escriptorium_annotations.json"
#TRANSCRIPTION_FILE = "./escriptorium_transcriptions.json"
#ONTOLOGY_FILE = "./ontology_export.json"
#OUTPUT_FILE = "SPACY_DATA"

# v2 -> Argparse
from argparse import ArgumentParser

parser = ArgumentParser(description="Generate a dataset to train Spacy's NER component from escriptorium data")
parser.add_argument("--annotations",type=str,help="Path to Annotations JSON",nargs=1,required=True)
parser.add_argument("--transcriptions",type=str,help="Path to Transcriptions JSON",nargs=1,required=True)
parser.add_argument("--ontology",type=str,help="Path to Ontology JSON",nargs=1,required=True)
parser.add_argument("--outfile",type=str,help="Path to Output file",nargs=1,required=True)
ARGS = parser.parse_args()
ANNOTATIONS_FILE = ARGS.annotations[0]
TRANSCRIPTION_FILE = ARGS.transcriptions[0]
ONTOLOGY_FILE = ARGS.ontology[0]
OUTPUT_FILE = ARGS.outfile[0]

# v3 -> Requests from Escriptorium API at urls
# http://localhost:8080/api/documents/1/parts/1/annotations/text/?format=json
# http://localhost:8080/api/documents/1/parts/1/transcriptions/?format=json
# http://localhost:8080/document/1/ontology/export/

import json

ann_file = open(ANNOTATIONS_FILE, 'r')
onto_file = open(ONTOLOGY_FILE, 'r')

tran_file = open(TRANSCRIPTION_FILE, 'r')


ann_data : dict = json.load(ann_file)
onto_data : dict = json.load(onto_file)
tran_data : dict = json.load(tran_file)

TRAIN_DATA = []

for ann in ann_data.get("results",[]):

    tag_key = ann.get("taxonomy",-1)
    tag_name = None

    for index, term in enumerate(onto_data.get("taxonomy",[])):
        if ( index + 1 ) == tag_key :
            tag_name : str = term.get("name","NO_ANN_TYPE").capitalize()
            # NOTE : Capitalize function is just a style choice
        #endIF
    #endFOR

    line_num = ann.get("start_line",-1) 

    
    char_0 = ann.get("start_offset",-1)
    char_n = ann.get("end_offset",-1)

    # TODO : Here we are making simple assumptions like:
    #           - The annotated token is all contained in a single line
    #           - Each line contains exactly one sentence (very unlikely 
    #                                   in an auto-transcribed manuscript)
    #       Less dumb implementation is required here. Take a look:
    #       https://ner.pythonhumanities.com/03_02_train_spacy_ner_model.html#preparing-the-data
    # ------------------------------------------------------------------------------------------

    line = None
    for match_index in tran_data.get("results",[]):
        if match_index["line"] == line_num :
            line = match_index["content"]

    sample = (line, {'entities' : [(char_0, char_n, tag_name)]})

    TRAIN_DATA.append(sample)
#endFOR

with open(OUTPUT_FILE,"w") as spacy_data:
    print(f"TRAIN_DATA = {TRAIN_DATA}",file=spacy_data)

ann_file.close()
onto_file.close()
tran_file.close()