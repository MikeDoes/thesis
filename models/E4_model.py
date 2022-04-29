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

missing_indices = []
maximum_length = 0
for i, predicted_label in enumerate(evaluations_1['predicted_labels']):
  if predicted_label["choices"][0]["text"] == "":
    missing_indices += [i]
  else:
    maximum_length = max(len(test_data["text"][i]), maximum_length)


prompt_string_train = ""  
for i in range(8):
    prompt_string_train += 'Q:' + train_data['text'][i] +'\n'
    prompt_string_train += 'A:' + str(train_data['labels'][i]) +'\n\n'


# Iterating over the test_data
maximum_length = 0

predicted_labels = []
try:
  for i in tqdm(missing_indices):
    sentence = test_data['text'][i]
    
    prompt_string = prompt_string_train + 'Q:' + sentence +'\n'+'A:'
    response = forward(prompt_string)
    predicted_labels += [response]
    
  
except:
  print('breaking out the loop')

dump = {'hyperparameters': 'engine="text-davinci-002", prompt=prompt_string, temperature=0, max_tokens=359, top_p=1, frequency_penalty=0.0, presence_penalty=0.0, stop=["\n"]', 
        'predicted_labels': predicted_labels,
        'missed_labels': missing_indices}

with open(f'models/results/E4_2.json', 'w') as f:
    json.dump(dump, f)