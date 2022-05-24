import json

data = []
with open('bert-large-cased-bob_dylan.jsonl') as f:
    for line in f:
        data.append(json.loads(line))

#Generating the nodes
nodes = []
node_lines = []
node_confidence = []

for i, line in enumerate(data):
    for triplet in data[i]['tri']:
        if triplet["h"] not in nodes:
            nodes += [triplet["h"]]
            node_lines += [i]
            node_confidence += [triplet["c"]]

        else:
            index = nodes.index(triplet["h"])
            node_confidence[index] = max([node_confidence[index], triplet["c"]])

        if triplet["t"] not in nodes:
            nodes += [triplet["t"]]
            node_lines += [i]
            node_confidence += [triplet["c"]]
        
        else:
            index = nodes.index(triplet["t"])
            node_confidence[index] = max([node_confidence[index], triplet["c"]])
            

        

#Have to write down their first appearance for the slider

nodes_formated = [nodes, node_lines, node_confidence]


with open('bob_dylan_nodes.json', 'w') as f:
    json.dump(nodes_formated, f)


#Generating the edges

edges_formated = []


for i, line in enumerate(data):
    for triplet in data[i]['tri']:
        h = nodes.index(triplet["h"])
        t = nodes.index(triplet["t"])
        label = triplet["r"]
        c = round(triplet["c"], 3)
        line = i

        #Check if it's not already in there:
        found = None
        for j, edge in enumerate(edges_formated):
            if edge[0] == h: 
                if edge[1] == t:
                    if edge[2] == label:
                        found = j

        if not found:
            frequency = 1
            edges_formated += [[h, t, label, c, line, frequency]]
        
        else:
            edges_formated[found][5] += 1 
        

with open('bob_dylan_edges.json', 'w') as f:
    json.dump(edges_formated, f)




