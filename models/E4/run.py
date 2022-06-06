# This model is a zero-shot GPT-3 using the OpenAI application point interface
import openai
import json
from tqdm import tqdm

MAX_PROMPT_LENGTH = 4096
output_file = 'models/E4/results/benchie_en_seperation_2_commas.json'
input_file_train = 'visualiser/datasets/oie2016_spanoie_dataset.json'
input_file_test = 'datasets/benchie/annotations/benchie_en.json'

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

train_data = load_dataset(input_file_train)
test_data = load_dataset(input_file_test)

prompt_string_train = ""  

#To seperate within the sentence
seperation_token = ",,"

for i in range(8):
    prompt_string_train += 'In the sentence: ' + pre_process(train_data['text'][i]) +'\n'
    prompt_string_train += 'The facts are: ' + ', '.join(['(' + pre_process(j[0]) + seperation_token + pre_process(j[1]) + seperation_token + pre_process(j[2]) + ')' for j in train_data['labels'][i]]) + '\n\n'

# Iterating over the test_data
prompt_strings = []
predicted_labels = []

# Assert that the prompt tokens are smaller than 4096
for i in range(len(test_data['text'])):
  prompt_string = prompt_string_train + 'In the sentence: ' + pre_process(test_data['text'][i]) +'\n'
  assert 0 < len(prompt_string) < MAX_PROMPT_LENGTH


try:
  for i in tqdm(range(len(test_data['text']))):
    
    sentence = test_data['text'][i]
    
    prompt_string = prompt_string_train + 'In the sentence: ' + pre_process(sentence) +'\n'
    
    response = forward(prompt_string)


    # Updating the result dump
    prompt_strings += [sentence]
    predicted_labels += [response]
    
except Exception as e:
    print("Exception caught:" + str(e))

dump = {'hyperparameters': 'engine="text-davinci-002", prompt=prompt_string, temperature=0, max_tokens=359, top_p=1, frequency_penalty=0.0, presence_penalty=0.0, stop=["\n"]', 
        'predicted_labels': predicted_labels,
        'prompt_text': prompt_strings,
        'prompt_train_text': prompt_string_train, 
        'text': test_data['text']}

with open(output_file, 'w') as f:
    json.dump(dump, f)