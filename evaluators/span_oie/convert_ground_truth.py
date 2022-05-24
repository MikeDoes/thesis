
import json

with open('Re-OIE2016.json') as f:
    data = json.load(f)

export_data = {}

export_data['text'] = []

for _, key in enumerate(data):
    export_data['text'] += [key]
    

    for extraction_origin in data['key']:
        extraction = {}
        extraction['head'] = extraction_origin

