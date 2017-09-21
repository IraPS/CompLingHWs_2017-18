from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
import nltk.data
from nltk import bigrams
import networkx as nx
import matplotlib.pyplot as plt
import operator
import copy
import os
from rake_nltk import Rake



def get_text_and_sentences(filename, all_texts, sw):
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
    collection = [os.path.join(all_texts, f) for f in os.listdir(all_texts)]
    collection = [file for file in collection if file.endswith('.txt')]
    return text, sentences, collection


def create_tfidf_matrix(filename, all_texts, lower, sw):
    text = get_text_and_sentences(filename, all_texts, sw)[0]
    collection = get_text_and_sentences(filename, all_texts, sw)[2]
    if sw:
        tf = TfidfVectorizer(input='filename', analyzer='word', ngram_range=(1, 4),
                             min_df = 0, stop_words='english', sublinear_tf=True, lowercase=lower)
    else:
        tf = TfidfVectorizer(input='filename', analyzer='word', ngram_range=(1, 4),
                             min_df = 0, sublinear_tf=True, lowercase=lower)
    tf = tf.fit(collection)
    tfidf_matrix = tf.transform([filename + '.txt'])
    feature_names = tf.get_feature_names()
    feature_index = tfidf_matrix[0, :].nonzero()[1]
    tfidf_scores = zip(feature_index, [tfidf_matrix[0, x] for x in feature_index])
    matrix = [(feature_names[i], s) for (i, s) in tfidf_scores]
    reversed_matrix = sorted(matrix, key=lambda x: x[1], reverse=False)
    matrix = sorted(matrix, key=lambda x: x[1], reverse=True)
    return feature_names, matrix, reversed_matrix


def create_coocurence_matrix(filename, all_texts, lower, sw):
    sentences = get_text_and_sentences(filename, all_texts, sw)[1]
    tfidf_ngrams = create_tfidf_matrix(filename, all_texts, lower, sw)[1][:250] \
                   + create_tfidf_matrix(filename, all_texts, lower, sw)[2][:250]
    top_tfidf_ngrams = [x[0] for x in tfidf_ngrams]
    cooucurence = list()
    for ngram in top_tfidf_ngrams:
        word_coocurence = list([0]*(len(top_tfidf_ngrams)-1))
        top_tfidf_ngrams.pop(top_tfidf_ngrams.index(ngram))
        word_cand = top_tfidf_ngrams
        for sent in sentences:
            for i in range(len(word_cand)):
                if ngram in sent and word_cand[i] in sent:
                    word_coocurence[i] += 1
        cooucurence.append(word_coocurence)
    candidates = [x[0] for x in tfidf_ngrams]
    return candidates, cooucurence


def create_graph(filename, all_texts, lower, sw):
    candidates = create_coocurence_matrix(filename, all_texts, lower, sw)[0]
    cooucurence = create_coocurence_matrix(filename, all_texts, lower, sw)[1]
    G = nx.Graph()
    for word in range(len(cooucurence)):
        for el in range(len(cooucurence[word])):
            G.add_weighted_edges_from([(candidates[word], candidates[el], cooucurence[word][el])])
    return G


def get_centrality(filename, all_texts, lower, sw):
    G = create_graph(filename, all_texts, lower, sw)
    bc = nx.betweenness_centrality(G)
    gc = nx.degree_centrality(G)
    return bc, gc


def get_top_centrality(filename, all_texts, lower, sw):
    bc = get_centrality(filename, all_texts, lower, sw)[0]
    gc = get_centrality(filename, all_texts, lower, sw)[1]
    nodes_by_betweenness_centrality = sorted(bc.items(), key=operator.itemgetter(1), reverse=True)
    top_betweenness_centrality = [t[0] for t in nodes_by_betweenness_centrality[:15]]
    nodes_by_degree_centrality = sorted(gc.items(), key=operator.itemgetter(1), reverse=True)
    top_degree_centrality = [t[0] for t in nodes_by_degree_centrality[:15]]
    return top_betweenness_centrality, top_degree_centrality


def generate_metrics_tfidf(filename, all_texts, lower, sw):
    true = open(filename + '.key', 'r', encoding='utf-8').readlines()
    true = [line.split('\n')[0] for line in true]
    top_tfidf = create_tfidf_matrix(filename, all_texts, lower, sw)[1][:15]
    predicted = [x[0] for x in top_tfidf]
    true0 = copy.copy(true)
    precision = 0
    print('tfidf:', predicted)
    for res in predicted:
        for term in true0:
            if res.lower() == term:
                precision += 1
                del true0[true0.index(term)]
            else:
                if res.lower() in term or term in res.lower():
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


def generate_metrics_betw_centrality(filename, all_texts, lower, sw):
    top_betweenness_centrality = get_top_centrality(filename, all_texts, lower, sw)[0]
    true = open(filename + '.key', 'r', encoding='utf-8').readlines()
    true = [line.split('\n')[0] for line in true]
    true0 = copy.copy(true)
    precision = 0
    print('betw:', top_betweenness_centrality)
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


def generate_metrics_deg_centrality(filename, all_texts, lower, sw):
    top_deg_centrality = get_top_centrality(filename, all_texts, lower, sw)[1]
    true = open(filename + '.key', 'r', encoding='utf-8').readlines()
    true = [line.split('\n')[0] for line in true]
    true0 = copy.copy(true)
    precision = 0
    print('deg:', top_deg_centrality)
    for top in top_deg_centrality:
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


def generate_metrics_rake(filename):
    r = Rake()
    text = open(filename + '.txt', 'r', encoding='utf-8').read()
    r.extract_keywords_from_text(text)
    predicted = r.get_ranked_phrases()[:15]
    true = open(filename + '.key', 'r', encoding='utf-8').readlines()
    true = [line.split('\n')[0] for line in true]
    true0 = copy.copy(true)
    precision = 0
    print('Rake:', predicted)
    for top in predicted:
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

results = open('comparing_tfidf_and_centrality(topdowntfidf)_metrics.csv', 'w', encoding='utf-8')
results.write('Filename;tfidf_Precision;tfidf_Recall;tfidf_F;betw_Precision;betw_Recall;betw_F1;'
              'deg_Precision;deg_Recall;deg_F1;rake_Precision;rake_Recall;rake_F1\n')

for file in os.listdir('./dataset'):
    print(file)
    if file.endswith('.txt'):
        file = file.split('.txt')[0]
        metrics_tfidf = generate_metrics_tfidf('./dataset/' + file, './dataset', True, True)
        metrics_betw = generate_metrics_betw_centrality('./dataset/' + file, './dataset', True, True)
        metrics_deg = generate_metrics_deg_centrality('./dataset/' + file, './dataset', True, True)
        metrics_rake = generate_metrics_rake('./dataset/' + file)
        results.write(file + ';' + str(metrics_tfidf[0]) + ';' + str(metrics_tfidf[1]) + ';' + str(metrics_tfidf[2])
                      + ';' + str(metrics_betw[0]) + ';' + str(metrics_betw[1]) + ';' + str(metrics_betw[2])
                      + ';' + str(metrics_deg[0]) + ';' + str(metrics_deg[1]) + ';' + str(metrics_deg[2])
                      + ';' + str(metrics_rake[0]) + ';' + str(metrics_rake[1]) + ';' + str(metrics_rake[2]) + '\n')

results.close()