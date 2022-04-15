
def load_openie_dataset():
    import json
    import torch    
    # Loading the Open IE dataset into the PyTorch DataLoader
    with open('datasets/oie2016/data.json') as json_file:
        data = json.load(json_file)

    return data