import json

with open('data/earnings_20161_openie5.json') as json_file:
    data = json.load(json_file)


#Nodes
sentence_count = 0
previous_sentence = ''
text = ''
nodes = []
node_lines = []
node_confidence = []

for i, _ in enumerate(data):
    if previous_sentence!= data[i]['sentence']: 
        sentence_count += 1
        text += data[i]['sentence']
        previous_sentence = data[i]['sentence']

    confidence = data[i]['confidence']

    nodes += [data[i]['extraction']['arg1']['text']]
    node_lines += [sentence_count]
    node_confidence += [confidence]

    for j, _ in enumerate(data[i]['extraction']['arg2s']):
        nodes += [data[i]['extraction']['arg2s'][j]['text']]
        node_lines += [sentence_count]
        node_confidence += [confidence]


nodes_formated = [nodes, node_lines, node_confidence]

with open('earning_openie5_nodes.json', 'w') as f:
    json.dump(nodes_formated, f)

#Edges

edges = []
sentence_count = 0
for i, _ in enumerate(data):
    if previous_sentence!= data[i]['sentence']: 
        sentence_count += 1
        previous_sentence = data[i]['sentence']
    
    confidence = data[i]['confidence']

    h = nodes.index(data[i]['extraction']['arg1']['text'])
    label = data[i]['extraction']['rel']['text']

    for j, _ in enumerate(data[i]['extraction']['arg2s']):
        t = nodes.index(data[i]['extraction']['arg2s'][j]['text'])

        found = False
        for k, edge in enumerate(edges):
            if edge[0]== h:
                if edge[1] == t:
                    if edge[2] == label:
                        found = k

        if found:
            edges[found][5] += 1

        else:
            edges += [[h, t, label, confidence, sentence_count, 1]]

##edges_formated += [[h, t, label, confidence, line, frequency]]

with open('earning_openie5_edges.json', 'w') as f:
    json.dump(edges, f)