import json

def load_json(path):
    with open(path) as f:
        data = json.load(f)
    return data

def reoie2016_to_visualisation(in_path='datasets/span_oie2016/test_sequence_sequences.json', out_path='visualiser/datasets/reoie2016_e4.json', result_data_path='models/results/E4_ReOIE2016.json'):
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

def prediction_text_to_visualiser(
        test_dataset_path = 'models/E4/results/benchie_en.json',
        results_path = 'models/E4/results/benchie_en.json',
        output_path = 'visualiser/datasets/benchie_e4.json'):
    # Transforms output from language models to visualiser
    data = load_json(test_dataset_path)
    # missing_indices = list(range(len(test_data['text'])))

    evaluations_1 = load_json(results_path)

    data['labels'] = []

    for i, predicted_label in enumerate(evaluations_1['predicted_labels']):
        for j, _ in enumerate(predicted_label["choices"]):
            new_triple_list = []
            try:
                triple_list = predicted_label["choices"][j]["text"]
                triple_list = triple_list.split('are: ')[1]
                triple_list = triple_list.split('), (')
                triple_list[0] = triple_list[0][1:]
                triple_list[-1] = triple_list[-1][:-1]
                triple_list = [arg.split(', ') for arg in triple_list if len(arg.split(', ')) == 3]

            except:
                #triple_list = [[["", "", ""]]]
                pass

            new_triple_list += [triple_list]
            
        data['labels'] += [triple_list]


    print(data['labels'])
    with open(output_path, 'w') as f:
        json.dump(data, f)


def benchie_to_visualiser(in_path='evaluators/benchie/data/gold/2_annotators/benchie_gold_annotations_en.txt', out_path='visualiser/datasets/benchie_en.json'):
    with open(in_path) as f:
        data = f.read()
    
    output = {
        'text' : [],
        'labels' : []
    }

    for sentence_batch in data.split('\n\n'):
        sentence_id = sentence_batch.split('\t')[0].split(':')[1]
        sentence_text = sentence_batch.split('\t')[1].split('\n')[0]
        output['text'] += [sentence_text]
        triple_list = []
        
        for i, cluster in enumerate(sentence_batch.split(f"{sentence_id}-->")):
            if i == 0: continue
            try:
                triple = cluster.split('\n')[1]
                triple = triple.split(' --> ')
                triple_list += [triple]
            except:
                pass

        output['labels'] += [triple_list]
    
    print(len(output['text']))
    print(len(output['labels']))
    with open(out_path, 'w') as f:
        json.dump(output, f)
    

def visualisation_to_benchie(
        in_path='visualiser/datasets/benchie_e4.json', 
        out_path='evaluators/benchie/data/oie_systems_explicit_extractions/e4_explicit.txt'):
    data = load_json(in_path)
    output_string = ''

    for i, triple_list in enumerate(data['labels']):
       for triple in triple_list:
            try:
               output_string += f'{i+1}  {triple[0]}  {triple[1]}  {triple[2]}\n'
            except:
                pass

    with open(out_path, 'w') as f:
        f.write(output_string)

visualisation_to_benchie()