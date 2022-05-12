# This model is a zero-shot GPT-3 using the OpenAI application point interface
\
import openai
import json
from tqdm import tqdm

def load_dataset(path):
  with open(path) as f:
    data = json.load(f)
  return data

def pre_process(text):
  text = str(text)
  text = text.replace('[', '(').replace(']', ')').replace('``','\'\'')
  return text

def forward(prompt_string):
  openai.api_key = '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'
  response = openai.Completion.create(
    engine="text-davinci-002",
    prompt=prompt_string,
    n=3,
    max_tokens=358,
    frequency_penalty=0,
    presence_penalty=0,
    temperature=0.95,
    stop=["\n\n"]
  )
  return response

train_data = load_dataset('datasets/supervised_oie/parsed/train_sequence_sequences.json')
test_data = load_dataset('datasets/span_oie2016/test_sequence_sequences.json')

prompt_string_train = ""  
for i in range(8):
    prompt_string_train += 'In the sentence: ' + pre_process(test_data['text'][i]) +'\n'
    prompt_string_train += 'The facts are: ' + ', '.join(['(' + pre_process(j[0]) + ', ' + pre_process(j[1]) + ', ' + pre_process(j[2]) + ')' for j in train_data['labels'][i]]) + '\n\n'

# Iterating over the test_data
prompt_strings = []
predicted_labels = []

try:
  for i in tqdm(range(len(test_data['text']))):
    sentence = test_data['text'][i]
    
    prompt_string = prompt_string_train + 'In the sentence: ' + pre_process(sentence) +'\n'
    
    response = forward(prompt_string)


    # Updating the result dump
    prompt_strings += ['In the sentence: ' + pre_process(sentence) +'\n']
    predicted_labels += [response]
    
  
except:
  print('breaking out the loop')

dump = {'hyperparameters': 'engine="text-davinci-002", prompt=prompt_string, temperature=0, max_tokens=359, top_p=1, frequency_penalty=0.0, presence_penalty=0.0, stop=["\n"]', 
        'predicted_labels': predicted_labels,
        'prompt_text': prompt_strings,
        'prompt_train_text': prompt_string_train}

with open(f'models/results/E4_.json', 'w') as f:
    json.dump(dump, f)