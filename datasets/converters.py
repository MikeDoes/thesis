import json

def load_json(path):
    with open(path) as f:
        data = json.load(f)
    return data

def reoie2016_to_visualisation(in_path='datasets/span_oie2016/test_sequence_sequences.json', out_path='visualiser/datasets/reoie2016_e4.json', result_data_path='models/results/E4_ReOIE2016.json')
    test_data = load_json(in_path)
    result_data = load_json(result_data_path)

    predicted_labels = []
    for i, text in enumerate(result_data['predicted_labels']):
    
    print(text)
    print(result_data['prompt_text'][i])
    print('#####')

    predicted_triple_list = []

    for triple_list in text['choices']:
        for triple in triple_list['text'].split('(')[1:]:
            predicted_triple_list += [triple.split(')')[0].split(', ')]

    predicted_labels += [predicted_triple_list]

    test_data['labels'] = predicted_labels

    with open(out_path, 'w') as f:
        json.dump(test_data, f)


def visualisation_to_reoie2016(in_path='visualiser/datasets/oie2016_spanoie_dataset.json', out_path='models/results/reoie2016.json'):
    data = load_json(in_path)
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

    with open(out_path, 'w') as f:
        json.dump(data, f)

def prediction_text_to_visualiser():
    # Transforms output from language models to visualiser
    data = load_json('datasets/supervised_oie/parsed/test_sequence_sequences.json')
    # missing_indices = list(range(len(test_data['text'])))

    evaluations_1 = load_json('models/results/E4_partial.json')

    data['labels'] = []

    for i, predicted_label in enumerate(evaluations_1['predicted_labels']):
        triple_list = predicted_label["choices"][0]["text"]

        try:
            #remove the extra parenthesis
            triple_list = triple_list[1:-1]
            new_triple_list = []
            for triple in triple_list.split(', ['):
                new_triple = []
                for argument in triple.split(', \''):
                    new_triple += [str(argument).replace('\'', '').replace('\'', '').replace('[', '').replace(']','')]
                new_triple_list += [new_triple]
        except:
            new_triple_list = [[["", "", ""]]]

        data['labels'] += [new_triple_list]

    print(data['labels'])
    with open(f'visualiser/datasets/oie2016_e4.json', 'w') as f:
        json.dump(data, f)