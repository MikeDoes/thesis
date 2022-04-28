# This model is a zero-shot GPT-3 using the OpenAI application point interface

import os
import openai
import json

def load_dataset(path):
  with open(path) as f:
    data = json.load(f)
  return data

train_data = load_dataset('datasets/supervised_oie/parsed/train_sequence_sequences.json')
test_data = load_dataset('datasets/supervised_oie/parsed/test_sequence_sequences.json')

prompt_string = ""  
for i in range(12):
  prompt_string += 'Text:' + train_data['text'][i] +'\n'
  prompt_string += 'Facts:' + train_data['text'][i] +'\n\n'

prompt_string += 'Text:' + test_data['text'][0] +'\n'+'Facts:'

openai.api_key = ''

response = openai.Completion.create(
  engine="text-davinci-002",
  prompt="I am a highly intelligent question answering bot. If you ask me a question that is rooted in truth, I will give you the answer. If you ask me a question that is nonsense, trickery, or has no clear answer, I will respond with \"Unknown\".\n\nQ: What is human life expectancy in the United States?\nA: Human life expectancy in the United States is 78 years.\n\nQ: Who was president of the United States in 1955?\nA: Dwight D. Eisenhower was president of the United States in 1955.\n\nQ: Which party did he belong to?\nA: He belonged to the Republican Party.\n\nQ: What is the square root of banana?\nA: Unknown\n\nQ: How does a telescope work?\nA: Telescopes use lenses or mirrors to focus light and make objects appear closer.\n\nQ: Where were the 1992 Olympics held?\nA: The 1992 Olympics were held in Barcelona, Spain.\n\nQ: How many squigs are in a bonk?\nA: Unknown\n\nQ: Where is the Valley of Kings?\nA:",
  temperature=0,
  max_tokens=200,
  top_p=1,
  frequency_penalty=0.0,
  presence_penalty=0.0,
  stop=["\n"]
)

print('Response Dict: \n', response.__dict__)
print('GPT-3 response: \n', response)
print('Labeled response: \n', test_data['text'][0])