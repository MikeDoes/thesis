# This model is a zero-shot GPT-3 using the OpenAI application point interface

import os
from matplotlib.pyplot import text
import openai
import json
from tqdm import tqdm

def load_dataset(path):
  with open(path) as f:
    data = json.load(f)
  return data


train_data = load_dataset('datasets/supervised_oie/parsed/train_sequence_sequences.json')
test_data = load_dataset('datasets/supervised_oie/parsed/test_sequence_sequences.json')
# missing_indices = list(range(len(test_data['text'])))

text = ""
for i, label in enumerate(train_data['labels']):
    text += "Q: " + train_data["text"][i] + "\n"
    text += "A: " + str(label) + "\n\n"


with open(f'training.txt', 'w') as f:
    f.write(text)