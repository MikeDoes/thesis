import pandas as pd
import sys
import os
from simplet5 import SimpleT5
from tqdm import tqdm

cwd=os.getcwd()
sys.path.append(r"{}".format(cwd))

from models.utils import load_dataset, source_pre_processing, label_pre_processing, export_dict

# CONSTANTS
SEPARATION_TOKEN = ",,"

# Loading the data
output_file = 'models/E1/results/benchie_en_separation_2_commas.json'
input_file_train = 'visualiser/datasets/benchie_en.json'
input_file_test = 'visualiser/datasets/benchie_en.json'
train_data = pd.DataFrame(load_dataset(input_file_train))
test_data = pd.DataFrame(load_dataset(input_file_test))

# Pre-processing for training
# the library expects dataframe to have 2 columns: "source_text" and "target_text"
train_data['source_text'] = [source_pre_processing(text) for text in train_data['text']]
train_data['target_text'] = [label_pre_processing(text, separation_token=SEPARATION_TOKEN) for text in train_data['labels']]

test_data['source_text'] = [source_pre_processing(text) for text in test_data['text']]
test_data['target_text'] = [label_pre_processing(text, separation_token=SEPARATION_TOKEN) for text in test_data['labels']]

test_data = train_data.iloc[-40:]
train_data = train_data.iloc[:260]

print("Train Data Length", len(train_data))
print(train_data.head())
print("Test Data Length", len(test_data))
print(test_data.head())

#Training 
model = SimpleT5()
model.from_pretrained(model_type="t5", model_name="t5-base")
model.train(train_df=train_data,
            eval_df=test_data, 
            source_max_token_len=200, 
            target_max_token_len=350, 
            batch_size=4, max_epochs=40, use_gpu=True)

# Create Predictions
def epoch_number(elem):
    return int(elem.split('-')[2])
    
for epoch in sorted(os.listdir('outputs'), key=epoch_number):
  
  model = SimpleT5()
  model.load_model("t5",f"/content/thesis/outputs/{epoch}", use_gpu=True)

  epoch = epoch.split('-')[2]
  output_file = f'models/E1/results/benchie_en_separation_2_commas_{epoch}.json'
  forward = model.predict
  prompt_strings, predicted_labels = [], []
  prompt_string_train = ''
  test_data = pd.DataFrame(load_dataset(input_file_test))


  for i in tqdm(range(len(test_data['text']))):
    predicted_labels += [{'choices':[]}]
    source_text = test_data['text'][i]
    prompt_string = prompt_string_train + source_pre_processing(source_text)


    responses = forward(prompt_string, num_return_sequences=3, num_beams=4, top_p=1, top_k=50, repetition_penalty = 1.5,)
    # Updating the results dictionary
    for response in responses:
      predicted_labels[i]['choices'] += [ {'text':response} ]

    prompt_strings += [source_text]


  # Exporting results to JSON for further processing and visualisation
  results = {'hyperparameters': 'model=t5-base, separator=,,', 
          'predicted_labels': predicted_labels,
          'prompt_text': prompt_strings,
          'prompt_train_text': prompt_string_train, 
          'text': list(test_data['text'])}

  export_dict(output_file, results)