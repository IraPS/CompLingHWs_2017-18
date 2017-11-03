from conllu.parser import parse
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB


def collect_features(data):
    X = list()
    y = list()
    POS = {'VERB': 1, 'ADP': 2, 'CONJ': 3, 'SCONJ': 4, 'NUM': 5, 'PUNCT': 6,
           'ADJ': 7, 'AUX': 8, 'SYM': 9, 'INTJ': 10, 'NOUN': 11, 'PROPN': 12,
           'PRON': 13, 'X': 14, 'ADV': 15}
    voice = {'Pass': 1, 'Act': 2}
    case = {'Gen': 1, 'Ins': 2, 'Com': 3, 'Nom': 4, 'Ess': 5,
            'Ela': 6, 'Par': 7, 'All': 8, 'Ill': 9, 'Abl': 10,
            'Tra': 11, 'Ade': 12, 'Abe': 13, 'Acc': 14, 'Ine': 15}
    verbform = {'Inf': 1, 'Part': 2, 'Fin': 3}
    deprel = {'amod': 1, 'punct': 2, 'nmod': 3, 'case': 4, 'csubj': 5, 'xcomp:ds': 6,
              'advmod': 7, 'ccomp': 8, 'root': 9, 'appos': 10, 'nmod:own': 11, 'neg': 12,
              'conj': 13, 'compound:nn': 14, 'acl': 15, 'cop': 16, 'dobj': 17, 'nmod:gsubj': 18,
              'name': 19, 'acl:relcl': 20, 'foreign': 21, 'nsubj': 22, 'advcl': 23,
              'compound:prt': 24, 'aux': 25, 'remnant': 26, 'nummod': 27, 'vocative': 28,
              'nmod:gobj': 29, 'auxpass': 30, 'goeswith': 31, 'nsubj:cop': 32,
              'parataxis': 33, 'csubj:cop': 34, 'discourse': 35, 'mark': 36, 'mwe': 37,
              'det': 38, 'cc:preconj': 39, 'nmod:poss': 40, 'compound': 41, 'xcomp': 42, 'cc': 43,
              'dep': 44}
    for sent in data:
        for w in sent:
            w_res = list()
            w_feats = (dict(w)['feats'])
            w_res.append(POS[dict(w)['upostag']])
            w_res.append(dict(w)['id'])
            if w_feats:
                w_feats = dict(w_feats)
                try: w_res.append(case[w_feats['Case']])
                except: w_res.append(0)
                try: w_res.append(voice[w_feats['Voice']])
                except: w_res.append(0)
                try: w_res.append(verbform[w_feats['VerbForm']])
                except: w_res.append(0)
            else:
                w_res.append(0)
                w_res.append(0)
                w_res.append(0)
            y.append(deprel[dict(w)['deprel']])
            X.append(w_res)
    return X, y

train_data = open('fipb-ud-train.conllu', 'r').read()
test_data = open('fipb-ud-test.conllu', 'r').read()

parsed_train = parse(train_data)
parsed_test = parse(test_data)

X_train = collect_features(parsed_train)[0]
y_train = collect_features(parsed_train)[1]
X_test = collect_features(parsed_test)[0]
y_test = collect_features(parsed_test)[1]

classifiers = [
    KNeighborsClassifier(3),
    DecisionTreeClassifier(max_depth=5),
    RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1),
    MLPClassifier(alpha=1),
    GaussianNB(),
    LogisticRegression()]

names = ["Nearest Neighbors",
         "Decision Tree", "Random Forest", "Neural Net",
         "Naive Bayes", "Logistic Regression"]


for name, clf in zip(names, classifiers):
    print(name, 'is learning on the train dataset...')
    clf.fit(X_train, y_train)
    print('Predicting...')
    prediction = clf.predict(X_test)
    print(name, round(metrics.accuracy_score(y_test, prediction), 2), '\n')
    if name == "Logistic Regression":
        print(clf.coef_)