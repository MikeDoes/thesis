
# Imports
import pandas as pd
import numpy as np
from tqdm import tqdm
import json

# Reading the file:
file_name = 'all' #all, train, test

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
    'labels': [] #triplets ()
}


# Extracting all the rows with the right sentence id

sent_id = '3'
sent_subset = df[df['sent_id']==sent_id]

dataset['labels'] += [[]]
index = len(dataset['labels'])


# Extract triplets
for i, run_id in enumerate(sent_subset['run_id'].unique()):
    pred_subset = sent_subset[df['run_id']==run_id]
    
    head = pred_subset[(pred_subset['label']=='A0-B') | (pred_subset['label']=='A0-I')]['word']

    head = ' '.join(list(head))
    head = head.replace(' - ', '').replace(' .', '').replace(' ,', ',').replace(' n\'t', 'n\'t').replace(' \'s', '\'s').replace(' )', ')').replace('( ', '(').replace(' $', '$')
    
    
    relation = pred_subset[(pred_subset['label']=='P-B') | (pred_subset['label']=='P-I')]['word']
    relation = ' '.join(list(relation))
    

    relation = relation.replace(' - ', '').replace(' .', '').replace(' ,', ',').replace(' n\'t', 'n\'t').replace(' \'s', '\'s').replace(' )', ')').replace('( ', '(').replace(' $', '$')
    
    # tails
    # argument 1

    for j in range(1,6):
        if len(pred_subset[pred_subset['label']==f'A{j}-B']) == 0:
            break

        tail = pred_subset[(pred_subset['label']==f'A{j}-B') | (pred_subset['label']==f'A{j}-I')]['word'] 

        tail = ' '.join(list(tail))
        tail = tail.replace(' - ', '').replace(' .', '').replace(' ,', ',').replace(' n\'t', 'n\'t').replace(' \'s', '\'s').replace(' )', ')').replace('( ', '(').replace(' $', '$')
        
        dataset['labels'][index-1] += [(head, relation, tail)]


# Extract the sentences
word_list = sent_subset[df['run_id']==run_id]['word']
sentence = ' '.join(word_list)

dataset['text'] += [sentence.replace(' - ', '').replace(' .', '').replace(' ,', ',').replace(' n\'t', 'n\'t').replace(' \'s', '\'s').replace(' )', ')').replace('( ', '(').replace(' $', '$')]
print(dataset)