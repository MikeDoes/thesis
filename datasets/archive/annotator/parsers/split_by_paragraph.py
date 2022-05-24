import json

with open('earning_transcripts.json') as json_file:
    data = json.load(json_file)

paragraph_array = []

for key in data.keys():
    paragraph_count = 0
    for paragraph in data[key].split('\n'):
        if paragraph == '': continue
        paragraph_count += 1
        #paragraph_array += [paragraph]
        with open(f'{key}/{paragraph_count}.json', 'w') as json_file:
            json.dump(paragraph, json_file)
