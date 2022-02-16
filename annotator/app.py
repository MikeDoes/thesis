from flask import Flask, render_template,request
import json 
import os

app = Flask(__name__, static_url_path='/static/')

def choose_paragraph():
    reviewed = os.listdir('crowd_source_input/')

    for dataset in os.listdir('unlabeled_data/'):
        for identifier in os.listdir('unlabeled_data/' + dataset+ '/'):
            # Checks for available datasets
            identifier = identifier.split('.json')[0]
            print(dataset, identifier)
            found = False

            for user_input in reviewed:
                if f'{dataset}_{identifier}' in user_input:
                    found = True

            if found: continue
            
            return dataset, identifier

@app.route("/")
def index():
    dataset, id = choose_paragraph()
    with open(f'unlabeled_data/{dataset}/{id}.json') as json_file:
        data = json.load(json_file)
    return render_template('index.html', data= data, dataset=dataset, id=id)


@app.route("/add_triplets/", methods = ['GET', 'POST'])
def add_triplets():
    if request.method == 'POST':
        triplets = request.form['triplet_list']
        dataset = request.form['dataset']
        id = request.form['identifier']

        count = 0
        for f in os.listdir('crowd_source_input/'):
            if f'{dataset}_{id}' in f:
                count+=1
        
        with open(f'crowd_source_input/{dataset}_{id}_{count}.json', 'w') as json_file:
            data = json.dump(triplets, json_file)

    return 'success'


@app.route("/dataset/<dataset>/<id>")
def dataset(dataset, id):
    with open(f'unlabeled_data/{dataset}/{id}.json') as json_file:
        data = json.load(json_file)
    return data


