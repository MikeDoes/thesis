import json

def generate_train_prompt(train_data, number_example_sentences=8, separation_token=',,'):
  prompt_string_train = ""  
  number_example_sentences = min(len(train_data['labels'], number_example_sentences))
  for i in range(number_example_sentences):
      prompt_string_train += source_pre_processing(train_data['text'][i])
      prompt_string_train += label_pre_processing(train_data['labels'][i], separation_token)
  return prompt_string_train

def source_pre_processing(text):
  return 'In the sentence: ' + pre_process(text) +'\n'

def label_pre_processing(labels, separation_token):
  return 'The facts are: ' + ', '.join(['(' + pre_process(j[0]) + separation_token + pre_process(j[1]) + separation_token + pre_process(j[2]) + ')' for j in labels]) + '\n\n'



def assert_maximum_prompt_length(test_data, prompt_string_train, maximum_prompt_length):
  '''
  This function iterates through the test data and checks wether the maximum length of prompt/ context input is not exceed. If it does exceed, then it creates an error
  '''
  # Iterating over the test_data
  prompt_strings = []
  predicted_labels = []

  # Assert that the prompt tokens are smaller than 4096
  for i in range(len(test_data['text'])):
    prompt_string = prompt_string_train + 'In the sentence: ' + pre_process(test_data['text'][i]) +'\n'
    assert 0 < len(prompt_string) < maximum_prompt_length

def pre_process(text):
  text = str(text)
  text = text.replace('[', '').replace(']', '').replace('``','\'\'')
  return text

def load_dataset(path):
  with open(path) as f:
    data = json.load(f)
  return data

def export_dict(output_file, dictionary):
    with open(output_file, 'w') as f:
        json.dump(dictionary, f)