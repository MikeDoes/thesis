import json

def load_dataset(path):
  with open(path) as f:
    data = json.load(f)
  return data

data = load_dataset('models/results/reoie2016_e4.json')
data['extraction'] = []
for i, sentence in enumerate(data['text']):
    
    triple_list = data['labels'][i]
    
    combinations = []
    for triple in triple_list:
        tails = []
        if len(triple)<2:
            break
        combination = (triple[0], triple[1])
        if combination in combinations:
            break
        combinations += [combination]

        for triple_ in triple_list:
            if len(triple_)<2:
                break
            if triple_[0] == combination[0] and triple_[1] == combination[1]:
                
                if len(triple_)<3:
                    tail = ''
                else:  
                    tail = triple_[2]
                if tail not in tails:
                    tails += [tail]

        data['extraction'] += [{
            'head': combination[0],
            'relation': combination[1],
            'tails': tails
        }]

file_name = 'metrics_e4re'
with open(f'models/results/{file_name}.json', 'w') as f:
    json.dump(data, f)