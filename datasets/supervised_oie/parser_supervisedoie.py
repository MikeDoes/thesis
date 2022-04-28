
# Imports
import pandas as pd
import numpy as np
from tqdm import tqdm
import json

# Reading the file:
file_name = 'train' #all, train, test

with open(f'{file_name}.oie.conll') as f:
    headers = f.readline().replace('\n', '')
    entries = f.read().split('\n\n')
    
# Pre-processing steps:
entry_array = []
for entry in entries:
    rows = entry.split('\n')

    for row in rows:
        row = row.split('\t')
        entry_array += [row]

    
df = pd.DataFrame(columns=headers.split('\t'), data=entry_array).dropna()

dataset = {
    'text': [], #string of sentence ''
    'labels': [] #triplets (h, r, t)
}

for sent_id in tqdm(df['sent_id'].unique()):
    
    # Extracting all the rows with the right sentence id
    
    sent_subset = df[df['sent_id']==sent_id]
    
    dataset['labels'] += [[]]

    index = len(dataset['labels'])

    # Extract triplets
    for i, run_id in enumerate(sent_subset['run_id'].unique()):
        run_subset = sent_subset[df['run_id']==run_id]
        
        head = run_subset[(run_subset['label']=='A0-B') | (run_subset['label']=='A0-I')]['word']
    
        head = ' '.join(list(head))
        head = head.replace(' - ', ' ').replace(' .', '').replace(' ,', ',').replace(' n\'t', 'n\'t').replace(' \'s', '\'s').replace(' )', ')').replace('( ', '(').replace('$ ', '$')
        
        
        relation = run_subset[(run_subset['label']=='P-B') | (run_subset['label']=='P-I')]['word']
        relation = ' '.join(list(relation))
        

        relation = relation.replace(' - ', ' ').replace(' .', '').replace(' ,', ',').replace(' n\'t', 'n\'t').replace(' \'s', '\'s').replace(' )', ')').replace('( ', '(').replace('$ ', '$')
        
        # tails
        # argument 1

        for j in range(1,6):
            if len(run_subset[run_subset['label']==f'A{j}-B']) == 0:
                break

            tail = run_subset[(run_subset['label']==f'A{j}-B') | (run_subset['label']==f'A{j}-I')]['word'] 

            tail = ' '.join(list(tail))
            tail = tail.replace(' - ', ' ').replace(' .', '').replace(' ,', ',').replace(' n\'t', 'n\'t').replace(' \'s', '\'s').replace(' )', ')').replace('( ', '(').replace('$ ', '$')
            
            dataset['labels'][index-1] += [(head, relation, tail)]

        

    # Extract the sentences on sentence for loop
    word_list = run_subset['word']
    sentence = ' '.join(word_list)

    dataset['text'] += [sentence.replace(' - ', ' ').replace(' .', '').replace(' ,', ',').replace(' n\'t', 'n\'t').replace(' \'s', '\'s').replace(' )', ')').replace('( ', '(').replace('$ ', '$')]

with open(f'{file_name}_sequence_sequences.json', 'w') as f:
    json.dump(dataset, f)