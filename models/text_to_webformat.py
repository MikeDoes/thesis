import json

def load_dataset(path):
  with open(path) as f:
    data = json.load(f)
  return data


test_data = load_dataset('datasets/supervised_oie/parsed/test_sequence_sequences.json')
result_data = load_dataset('models/results/E4_3.json')

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

file_name = 'oie2016_e4'
with open(f'visualiser/datasets/{file_name}.json', 'w') as f:
    json.dump(test_data, f)