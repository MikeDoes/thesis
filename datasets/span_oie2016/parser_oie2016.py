import json

def clean_string(string):
    return string.replace(' - ', ' ').replace(' .', '.').replace(' ,', ',').replace(' n\'t', 'n\'t').replace(' \'s', '\'s').replace(' )', ')').replace('( ', '(').replace('$ ', '$')


with open('all.json') as f:
    data = json.load(f)

dataset = {
    'text': [clean_string(i) for i in list(data.keys())], #string of sentence ''
    'labels': [] #triplets (h, r, t)
}
for sentence_key in data:
    dataset['labels'] += [[]]
    index = len(dataset['labels'])

    for triple in data[sentence_key]:
        head = clean_string(triple["arg0"])
        relation = clean_string(triple["pred"])

        for j in range(1,6):
            if f"arg{j}" not in triple.keys():
                break

            tail = clean_string(triple[f"arg{j}"])
            if '' in [head, tail, relation]: break

            dataset['labels'][index-1] += [[head, relation, tail]]

with open('all_sequence_sequences.json', 'w') as f:
    json.dump(dataset, f)