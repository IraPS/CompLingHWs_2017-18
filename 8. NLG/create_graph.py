import xml.etree.ElementTree as ET
import re
import networkx as nx
import matplotlib.pyplot as plt

tree = ET.parse('Astronauts.xml')
root = tree.getroot()

triples = list()
answers = dict()

for entry in root.iter('entry'):
    originaltripleset = entry.find('originaltripleset')
    otriple = originaltripleset.find('otriple')
    triples.append((otriple.text, re.sub('_', ' ', otriple.text).split(' | ')))
    triple_answers = entry.findall('lex')
    triple_answers = [ans.text for ans in triple_answers]
    answers[otriple.text] = triple_answers

parsed_triples = [tr[1] for tr in triples]

graph_nodes = [tr[0] for tr in parsed_triples]
graph_nodes.append(tr[2] for tr in parsed_triples)
graph_nodes = list(set(graph_nodes))

G = nx.Graph()

G.add_nodes_from(graph_nodes)

graph_edges = list()
for triple in parsed_triples:
    graph_edges.append([triple[0], triple[2], {'label': triple[1]}])

G.add_edges_from(graph_edges)

plt.figure(figsize=(20, 25))
nx.draw(G, pos=nx.spring_layout(G), node_color='lightpink', edge_color='black', width=1.5,
        font_weight='bold', font_family='Helvetica', font_size='16', node_size=250,
        with_labels=True)
plt.axis('off')
plt.savefig('astronauts_graph.png')