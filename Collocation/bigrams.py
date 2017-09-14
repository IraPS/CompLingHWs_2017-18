from pymystem3 import Mystem
from math import log
import re

m = Mystem()


def preprocess(file):
    corpus = open(file, 'r', encoding='utf-8').read()
    corpus = re.sub('[\\n\(\)\[\]—\-,!\?:;$«»„“\.]', ' ', corpus)
    corpus = corpus.split()
    return corpus


def get_bigrams(corpus_path, term):
    corpus = preprocess(corpus_path)
    corpus_lemmas = list()
    bigrams = list()
    for i in range(1, len(corpus)-1):
        corpus_lemmas.append(m.lemmatize(corpus[i])[0])
        prev_words = list()
        next_words = list()
        if corpus[i] == term:
            prev_words.append(m.lemmatize(corpus[i-1])[0])
            prev_words.append(m.lemmatize(corpus[i])[0])
            next_words.append(m.lemmatize(corpus[i])[0])
            next_words.append(m.lemmatize(corpus[i+1])[0])
            bigrams.append(prev_words)
            bigrams.append(next_words)
    return corpus_lemmas, bigrams


def get_numbers(corpus_path, threshold, term):
    num_words = len(get_bigrams(corpus_path, term)[0])
    corpus_lemmas = get_bigrams(corpus_path, term)[0]
    bigrams = get_bigrams(corpus_path, term)[1]
    doubles = list()
    results = list()
    for bigram in bigrams:
        if bigram not in doubles:
            doubles.append(bigram)
            res = list()
            for word in bigram:
                res.append(word)
                res.append(corpus_lemmas.count(word))
            res.append(bigrams.count(bigram))
            if res[4] >= threshold:
                p_word1 = log(int(res[1])/num_words)
                p_word2 = log(int(res[3])/num_words)
                p_bigram = log(int(res[4])/(num_words-1))
                pmi = round(p_bigram/(p_word1*p_word2), 2)
                res.append(pmi)
                results.append(res)
    return results


def write_to_table(corpus_path, threshold, term):
    results = get_numbers(corpus_path, threshold, term)
    sorting = ['count', 'PMI']
    for sorting_type in sorting:
        table = open(term + '_bigrams_by_' + sorting_type + '.csv', 'w', encoding='utf-8')
        table.write('word1;word2;count(word1);count(word2);count(bigram);' + sorting_type + '\n')
        if sorting_type is 'PMI':
            sorted_results = sorted(results, key=lambda x: float(x[5]), reverse=True)
            for res in sorted_results:
                table.write(res[0] + ';' + res[2] + ';' + str(res[1]) + ';' + str(res[3])
                            + ';' + str(res[4]) + ';' + str(res[5]) + '\n')
        if sorting_type is 'count':
            sorted_results = sorted(results, key=lambda x: int(x[4]), reverse=True)
            for res in sorted_results:
                table.write(res[0] + ';' + res[2] + ';' + str(res[1]) + ';' + str(res[3])
                            + ';' + str(res[4]) + ';' + str(res[5]) + '\n')
        print('Bigrams for', term, 'sorted by', sorting_type, 'are ready.')
        table.close()

corpus_file = 'corpus.txt'
companies = ['Google', 'Amazon', 'Facebook', 'Apple']
for company in companies:
    write_to_table(corpus_file, 10, company)
