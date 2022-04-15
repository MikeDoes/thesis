
def load_openie_dataset():
    import json
    import torch    
    # Loading the Open IE dataset into the PyTorch DataLoader
    with open('datasets/oie2016/earnings_20161_openie5.json') as json_file:
        data = json.load(json_file)

    return data