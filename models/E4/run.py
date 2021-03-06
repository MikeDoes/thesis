# This model is a zero-shot GPT-3 using the OpenAI application point interface
from cgi import test
import openai
from tqdm import tqdm
import sys, os
cwd=os.getcwd()
sys.path.append(r"{}".format(cwd))
from models.utils import generate_train_prompt, assert_maximum_prompt_length, pre_process, load_dataset, export_dict


MAX_PROMPT_LENGTH = 4096
MAX_TOKEN_PREDICTION = 358
SEPERATION_TOKEN = ",,"
STOP_SEQUENCE = ["\n\n"]

output_file = 'models/E4/results/benchie_en_test_set.json'
input_file_train = 'datasets/benchie/annotations/benchie_en.json'
input_file_test = 'datasets/benchie/annotations/benchie_en.json'

train_data = load_dataset(input_file_train)
test_data = load_dataset(input_file_test)

test_data = {
  'text': test_data['text'][-40:],
  'labels': test_data['labels'][-40:]
}

prompt_string_train = generate_train_prompt(train_data, 6, SEPERATION_TOKEN)

assert_maximum_prompt_length(test_data, prompt_string_train, MAX_PROMPT_LENGTH)

# Defining the forward function of GPT-3
def forward(prompt_string):
  openai.api_key = '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'
  response = openai.Completion.create(
    engine="text-davinci-002",
    prompt=prompt_string,
    n=3,
    max_tokens=MAX_TOKEN_PREDICTION,
    frequency_penalty=0,
    presence_penalty=0,
    temperature=0.95,
    stop=STOP_SEQUENCE
  )
  return response

prompt_strings, predicted_labels = [], []

try:
  for i in tqdm(range(len(test_data['text']))):
    sentence = test_data['text'][i]
    prompt_string = prompt_string_train + 'In the sentence: ' + pre_process(sentence) +'\n'
    response = forward(prompt_string)

    # Updating the results dictionary
    prompt_strings += [sentence]
    predicted_labels += [response]
    
except Exception as e:
    print("Exception caught:" + str(e))


# Exporting results to JSON for further processing and visualisation
results = {'hyperparameters': 'engine="text-davinci-002", prompt=prompt_string, temperature=0, max_tokens=359, top_p=1, frequency_penalty=0.0, presence_penalty=0.0, stop=["\n"]', 
        'predicted_labels': predicted_labels,
        'prompt_text': prompt_strings,
        'prompt_train_text': prompt_string_train, 
        'text': test_data['text']}

export_dict(output_file, results)