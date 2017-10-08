from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import SGDClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import confusion_matrix
from sklearn.neural_network import MLPClassifier
import itertools
import numpy as np
import matplotlib.pyplot as plt
from sklearn.pipeline import Pipeline
from pprint import pprint
from time import time
from sklearn.model_selection import train_test_split
from sklearn import metrics


def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)
    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    '''
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")
                 '''
    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')


text_clf = Pipeline([('vect', CountVectorizer()),
                    ('tfidf', TfidfTransformer(norm='l2', sublinear_tf=True)),
                    ('clf', MLPClassifier())
                     ])
'''
parameters = {
    'vect__max_features': (None, 100, 300, 500, 1000),
    #'vect__ngram_range': ((1, 1), (1, 2)),  # unigrams or bigrams
    #'tfidf__use_idf': (True, False),
    #'tfidf__norm': ('l1', 'l2'),
    'clf__alpha': (0.00001, 0.000001),
    'clf__penalty': ('l2', 'elasticnet'),
    'clf__n_iter': (10, 50, 80),
grid_search = GridSearchCV(text_clf, parameters, n_jobs=-1, verbose=1)
print("Performing grid search...")
print("pipeline:", [name for name, _ in text_clf.steps])
print("parameters:")
pprint(parameters)
t0 = time()
grid_search.fit(X_train, y_train)
print("done in %0.3fs" % (time() - t0))
print()

print("Best score: %0.3f" % grid_search.best_score_)
print("Best parameters set:")
best_parameters = grid_search.best_estimator_.get_params()
for param_name in sorted(parameters.keys()):
    print("\t%s: %r" % (param_name, best_parameters[param_name]))
'''

X = open('./300K/tweets.text', 'r', encoding='utf-8').readlines()
y = open('./300K/tweets.labels', 'r', encoding='utf-8').readlines()

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)

true = open('true_keys.txt', 'w', encoding='utf-8')
for i in y_test:
    true.write(i)
true.close()

for clf in [SGDClassifier, LogisticRegression]:
    print(str(clf))
    text_clf = Pipeline([('vect', CountVectorizer()),
                        ('tfidf', TfidfTransformer(norm='l2', sublinear_tf=True)),
                        ('clf', clf())])
    text_clf.fit(X_train, y_train)
    predicted = text_clf.predict(X_test)
    pred = open('predicted_keys_' + str(clf) + '.txt', 'w', encoding='utf-8')
    for i in predicted:
        pred.write(i)
    pred.close()
    print(metrics.classification_report(y_test, predicted, target_names=y_test))
    print('\n\n\n')
    class_names = list(set(y_test))
    cnf_matrix = confusion_matrix(predicted, y_test)
    plt.figure()
    plot_confusion_matrix(cnf_matrix, classes=class_names, normalize=True,
                          title='Normalized confusion matrix')
    plt.show()
    plt.savefig(str(clf) + '_cnf_matrix.png')
    print('\n\n\n')
