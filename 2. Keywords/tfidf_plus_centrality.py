from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
import nltk.data
import networkx as nx
import matplotlib.pyplot as plt
import operator
import copy
import os


def get_text_and_sentences(filename, lower, sw):
    text = open(filename + '.txt', 'r', encoding='utf-8')
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    sentences0 = tokenizer.tokenize(text.read())
    sentences = list()
    if sw:
        from sklearn.feature_extraction import stop_words
        stop_words = stop_words.ENGLISH_STOP_WORDS
        for sent in sentences0:
            sentences.append(' '.join([w for w in sent.split() if w not in stop_words]))
    text.close()
    text = open(filename + '.txt', 'r', encoding='utf-8')
    return text, sentences


def create_tfidf_matrix(filename, lower, sw):
    text = get_text_and_sentences(filename, lower, sw)[0]
    if sw:
        tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 4),
                             min_df = 0, stop_words='english', sublinear_tf=True, lowercase=lower)
    else:
        tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 4),
                             min_df = 0, sublinear_tf=True, lowercase=lower)
    tfidf_matrix = tf.fit_transform(text)
    feature_names = tf.get_feature_names()
    feature_index = tfidf_matrix[0, :].nonzero()[1]
    tfidf_scores = zip(feature_index, [tfidf_matrix[0, x] for x in feature_index])
    matrix = [(feature_names[i], s) for (i, s) in tfidf_scores]
    return matrix


def create_coocurence_matrix(filename, lower, sw):
    sentences = get_text_and_sentences(filename, lower, sw)[1]
    matrix = create_tfidf_matrix(filename, lower, sw)
    candidates = [w[0] for w in matrix]
    cooucurence = list()
    for cand in candidates:
        word_coocurence = list([0]*(len(candidates)-1))
        candidates.pop(candidates.index(cand))
        word_cand = candidates
        for sent in sentences:
            for i in range(len(word_cand)):
                if cand in sent and word_cand[i] in sent:
                    word_coocurence[i] += 1
        cooucurence.append(word_coocurence)
    candidates = [w[0] for w in matrix]
    return candidates, cooucurence


def create_graph(filename, lower, sw):
    candidates = create_coocurence_matrix(filename, lower, sw)[0]
    cooucurence = create_coocurence_matrix(filename, lower, sw)[1]
    G = nx.Graph()
    for word in range(len(cooucurence)):
        for el in range(len(cooucurence[word])):
            G.add_weighted_edges_from([(candidates[word], candidates[el], cooucurence[word][el])])
    return G


def get_betweenness_centrality(filename, lower, sw):
    G = create_graph(filename, lower, sw)
    bc = nx.betweenness_centrality(G)
    return bc


def draw_graph(filename, graphname, lower, sw):
    G = create_graph(filename, lower, sw)
    bc = get_betweenness_centrality(filename, lower, sw)
    pos = nx.fruchterman_reingold_layout(G)
    nx.draw_networkx_nodes(G, pos, node_size=[v * 1000 for v in bc.values()], node_color='pink')
    nx.draw_networkx_edges(G, pos, width=1, edge_color='grey')
    nx.draw_networkx_labels(G, pos, font_size=8, font_family='sans-serif', font_weight='bold')
    plt.axis('off')
    plt.savefig('./graphs/' + graphname + "_graph.png", dpi=100)


def get_top_betweenness_centrality(filename, lower, sw):
    bc = get_betweenness_centrality(filename, lower, sw)
    candidates = create_coocurence_matrix(filename, lower, sw)[0]
    nodes_by_betweenness_centrality = sorted(bc.items(), key=operator.itemgetter(1), reverse=True)
    top_betweenness_centrality = [candidates[candidates.index(t[0])] for t in nodes_by_betweenness_centrality[:15]]
    return top_betweenness_centrality


def generate_metrics(filename, lower, sw):
    top_betweenness_centrality = get_top_betweenness_centrality(filename, lower, sw)
    true = open(filename + '.key', 'r', encoding='utf-8').readlines()
    true = [line.split('\n')[0] for line in true]
    print(get_top_betweenness_centrality(filename, lower, sw), '\n')
    print(true, '\n')
    true0 = copy.copy(true)
    precision = 0
    for top in top_betweenness_centrality:
        for term in true0:
            if top.lower() == term:
                precision += 1
                del true0[true0.index(term)]
            else:
                if top.lower() in term or term in top.lower():
                    precision += 0.5
                    del true0[true0.index(term)]
    precision = round(precision/len(true), 2)
    recall = round((len(true)-len(true0))/len(true), 2)
    try:
        F1 = round(2 * (precision * recall) / (precision + recall), 2)
    except ZeroDivisionError:
        F1 = float(0)
    '''
    print('For the text "' + filename + '" ' + 'precision is ' + str(round(precision, 2)),
          ', recall is ' + str(round(recall, 2)),
          ', F1 is ' + str(round(F1, 2)))
    '''
    return precision, recall, F1

results = open('tfidf_plus_centrality_without_sw_metrics.csv', 'w', encoding='utf-8')
results.write('Filename;Precision;Recall;F1\n')

for file in os.listdir('./dataset'):
    print(file)
    if file.endswith('.txt'):
        file = file.split('.txt')[0]
        draw_graph('./dataset/' + file, file, True, True)
        metrics = generate_metrics('./dataset/' + file, True, True)
        results.write(file + ';' + str(metrics[0]) + ';' + str(metrics[1]) + ';' + str(metrics[2]) + '\n')
        # generate_metrics('./dataset/' + file)

results.close()