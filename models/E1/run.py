from numpy import source
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
output_file = 'models/E1/results/benchie_en_seperation_2_commas.json'
input_file_train = 'visualiser/datasets/reoie2016_test.json'
input_file_test = 'datasets/benchie/annotations/benchie_en.json'
train_data = pd.DataFrame(load_dataset(input_file_train))
test_data = pd.DataFrame(load_dataset(input_file_test))

# Pre-processing for training
# the library expects dataframe to have 2 columns: "source_text" and "target_text"
train_data['source_text'] = [source_pre_processing(text) for text in train_data['text']]
train_data['target_text'] = [label_pre_processing(text, separation_token=SEPARATION_TOKEN) for text in train_data['labels']]

test_data['source_text'] = [source_pre_processing(text) for text in test_data['text']]
test_data['target_text'] = [label_pre_processing(text, separation_token=SEPARATION_TOKEN) for text in test_data['labels']]

#Training 
model = SimpleT5()
model.from_pretrained(model_type="t5", model_name="t5-base")
model.train(train_df=train_data,
            eval_df=test_data, 
            source_max_token_len=512, 
            target_max_token_len=512, 
            batch_size=8, max_epochs=10, use_gpu=True)

# Create Predictions
#model.load_model("t5","/content/outputs/simplet5-epoch-2-train-loss-0.9862-val-loss-1.2533", use_gpu=True

forward = model.predict
prompt_strings, predicted_labels = [], []

prompt_string_train = ''

try:
  for i in tqdm(range(len(test_data['text']))):
    source_text = test_data['text'][i]
    prompt_string = prompt_string_train + source_pre_processing(source_text)
    response = forward(prompt_string)

    # Updating the results dictionary
    prompt_strings += [source_text]
    predicted_labels += [response]
    
except Exception as e:
    print("Exception caught:" + str(e))


# Exporting results to JSON for further processing and visualisation
results = {'hyperparameters': 'model=t5-base, separator=,,', 
        'predicted_labels': predicted_labels,
        'prompt_text': prompt_strings,
        'prompt_train_text': prompt_string_train, 
        'text': test_data['text']}

export_dict(output_file, results)