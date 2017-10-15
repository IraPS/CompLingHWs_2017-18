from natasha import NamesExtractor
import os
import re

extractor = NamesExtractor()

tp = 0
fp = 0
fn = 0

for file in os.listdir('./testset'):
    if file.endswith('.txt'):
        # tp = 0
        # fp = 0
        # fn = 0
        textnum = file.split('.txt')[0]
        text = open('./testset/' + file, 'r', encoding='utf-8').read()
        matches = extractor(text)
        true = open('./testset/' + textnum + '.objects', 'r', encoding='utf-8').readlines()
        true = [re.sub('\n', '', line.split('# ')[-1]) for line in true]
        predicted = list()
        for match in matches:
            start, stop = match.span
            predicted.append(text[start:stop])
        for i in predicted:
            if i in true:
                tp += 1
            else:
                fp += 1
        for i in true:
            if i not in predicted:
                fn += 1
        '''
        precision = 0
        recall = 0
        fscore = 0
        if fp != 0 or tp != 0: precision = tp / (fp + tp)
        if fn != 0 or tp != 0: recall = tp / (fn + tp)
        if precision != 0 or recall != 0: fscore = 2*((precision*recall)/(precision+recall))
        print(textnum)
        if precision == 0 or recall == 0:
            print("CHECK")
            print(tp)
            print(fp)
            print(true)
            print(predicted)
        print('Precision', round(precision, 2))
        print('Recall', round(recall, 2))
        print('F1 score', round(fscore, 2))
        print('\n\n')
        '''

precision = tp / (fp + tp)
recall = tp / (fn + tp)
fscore = 2*((precision*recall)/(precision+recall))
print('Precision', round(precision, 2))
print('Recall', round(recall, 2))
print('F1 score', round(fscore, 2))

