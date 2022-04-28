import json

data = []
with open('data.json') as f:
    data = json.load(f)

dataset = {
    'text': [], #string of sentence ''
    'labels': [] #triplets (h, r, t)
}
