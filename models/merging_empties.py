# This model is a zero-shot GPT-3 using the OpenAI application point interface

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

train_data = load_dataset('datasets/supervised_oie/parsed/train_sequence_sequences.json')
test_data = load_dataset('datasets/supervised_oie/parsed/test_sequence_sequences.json')
# missing_indices = list(range(len(test_data['text'])))

evaluations_1 = load_dataset('models/results/E4_1.json')
evaluations_2 = load_dataset('models/results/E4_2.json')

missing_indices = []
maximum_length = 0
for i, index in enumerate(evaluations_2["missed_labels"]):
    evaluations_1['predicted_labels'][index] = evaluations_2['predicted_labels'][i]


with open(f'models/results/E4_merged.json', 'w') as f:
    json.dump(evaluations_1, f)