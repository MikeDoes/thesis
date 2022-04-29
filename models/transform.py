# Transforms GPT-3 Zero-shot output to text for visualiser

import os
import openai
import json
from tqdm import tqdm

def load_dataset(path):
  with open(path) as f:
    data = json.load(f)
  return data


def forward(prompt_string):
  openai.api_key = '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'
  response = openai.Completion.create(
    engine="text-davinci-002",
    prompt=prompt_string,
    temperature=0,
    max_tokens=200,
    top_p=1,
    frequency_penalty=0.0,
    presence_penalty=0.0,
    stop=["\n"]
  )
  return response

data = load_dataset('datasets/supervised_oie/parsed/test_sequence_sequences.json')
# missing_indices = list(range(len(test_data['text'])))

evaluations_1 = load_dataset('models/results/E4_partial.json')

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