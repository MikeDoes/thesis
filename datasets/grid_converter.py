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
            if len(triple) < 2:
                break
            combination = (triple[0], triple[1])
            if combination in combinations:
                break
            combinations += [combination]

            for triple_ in triple_list:
                if len(triple_) < 2:
                    break
                if triple_[0] == combination[0] and triple_[1] == combination[1]:
                    
                    if len(triple_) <3 :
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

def model_output_to_visualiser(
        test_dataset_path = 'models/E4/results/benchie_en.json',
        results_path = 'models/E4/results/benchie_en_seperation_2_commas.json',
        output_path = 'visualiser/datasets/benchie_e4.json',
        max_number_runs = 999):
    # Transforms output from language models to visualiser
    data = load_json(test_dataset_path)
    # missing_indices = list(range(len(test_data['text'])))

    evaluations_1 = load_json(results_path)

    data['labels'] = []
    data["hyperparameters"] = evaluations_1["hyperparameters"]

    not_in_sentence_prediction = 0
    successful_parsing = 0
    invalid_syntax_count, valid_syntax_count = 0, 0

    accuracies_by_epoch = {}

    for i, predicted_label in enumerate(evaluations_1['predicted_labels']):
        sentence_level_triple_list = []
        sentence = data['text'][i]

        for j, choice in enumerate(predicted_label["choices"]):
            try:
                # We have to check if the words are in the text, if there are commas. Treat them as words?
                choice_level_triple_list = choice["text"]
                choice_level_triple_list = choice_level_triple_list.split('are: ')[1]
                choice_level_triple_list = choice_level_triple_list.split('), (')
                choice_level_triple_list[0] = choice_level_triple_list[0][1:]
                choice_level_triple_list[-1] = choice_level_triple_list[-1][:-1]
                

                for triple in choice_level_triple_list:
                    if len(triple.split(',,')) > 3:
                        pass
                        #Figure out how to recover with more than 
                    
                    if len(triple.split(',,')) == 3:
                        args = triple.split(',,')
                        
                        #Checks if words are in the sentence
                        in_sentence = True
                        for i, arg in enumerate(args):
                            if arg[0]==' ':
                                args[i] = args[i][1:]
                            
                            if arg[-1]==' ':
                                args[i] = args[i][:-1]

                            for word in arg:
                                if word not in sentence or arg == '' or arg is None:
                                    in_sentence = False


                        if not in_sentence:
                            not_in_sentence_prediction += 1
                            continue
                        
                        successful_parsing += 1
                        
                        triple = [args[0], args[1], args[2]]
                        sentence_level_triple_list += [triple]
                
                valid_syntax_count += 1

            except:
                invalid_syntax_count += 1
            
            if j >= (max_number_runs-1): break

        sentence_level_triple_list = list(set(tuple(i) for i in sentence_level_triple_list))
        data['labels'] += [sentence_level_triple_list]

    in_sentence_accuracy = float(successful_parsing)/(successful_parsing+not_in_sentence_prediction)
    syntax_accuracy = float(valid_syntax_count)/(valid_syntax_count + invalid_syntax_count)
    
    accuracies_by_epoch = {
        'model':results_path.split('_')[-1].split('.')[0],
        'in_sentence_accuracy':in_sentence_accuracy,
        'syntax_accuracy':syntax_accuracy,
    }

    with open(output_path, 'w') as f:
        json.dump(data, f)
    
    return accuracies_by_epoch


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
            if len(triple) != 3 or triple[0]=='' or triple[1]=='' or triple[2]=='': continue

            try:
                output_string += f'{i+1}\t{triple[0]}\t{triple[1]}\t{triple[2]}\n'
            except:
                pass

    with open(out_path, 'w') as f:
        f.write(output_string)


# By Epoch


accuracies = {}
number_choices = 4
number_epoch = 5


for i in range(number_choices):
    for j in range(number_epoch):
        out_path = f"evaluators/benchie/data/oie_systems_explicit_extractions/e1_grid/e1_explicit_{i}_{j}.txt"

        accuracies_by_runs = model_output_to_visualiser(test_dataset_path = 'models/E4/results/benchie_en.json',
                results_path = f'models/E1/results/4runs/benchie_en_separation_2_commas_{j}.json',
                output_path = f'visualiser/model_results/e1_grid/e1_explicit_{i}_{j}.json',
                max_number_runs= i+1)

        accuracies[str(i)] = accuracies_by_runs
        

        visualisation_to_benchie(in_path=f'visualiser/model_results/e1_grid/e1_explicit_{i}_{j}.json', 
                out_path=out_path)

with open('visualiser/model_results/t5_epochs.json', 'w') as f:
    json.dump(accuracies, f)

