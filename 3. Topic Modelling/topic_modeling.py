from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation
import numpy as np
from en_stopwords import stopwords # stop-words list from MySQL
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
import re


class LemmaTokenizer(object):
    def __init__(self):
        self.wnl = WordNetLemmatizer()
    def __call__(self, doc):
        return [self.wnl.lemmatize(t) for t in word_tokenize(doc)]


def display_topics(model, feature_names, no_top_words):
    for topic_idx, topic in enumerate(model.components_):
        print("Topic {}:".format(topic_idx))
        print(", ".join([feature_names[i]
                        for i in topic.argsort()[:-no_top_words - 1:-1]]))
        # print(", ".join([feature_names[i]
        #                  for i in topic.argsort()[::-1][:no_top_words]]))


n_topics = 9

documents = open('1_en.txt', 'r', encoding='utf-8').read()
documents = re.sub('[\.,\?!-\'`:%\$\)\(-;]', '', documents)
documents = documents.split('\n\n')
print('Text collection size and median length in symbols:')
print(len(documents), np.median([len(d) for d in documents]))


tfidf_vectorizer = TfidfVectorizer(ngram_range=(1, 2),
                                   max_df=0.8,
                                   min_df=5,
                                   stop_words=stopwords,
                                   tokenizer=LemmaTokenizer())
tfidf = tfidf_vectorizer.fit_transform(documents)
tfidf_feature_names = tfidf_vectorizer.get_feature_names()

print()

nmf = NMF(n_components=n_topics)
nmf_doc_topic = nmf.fit_transform(tfidf)
print('NMF doc-topic shape:', nmf_doc_topic.shape)


# LDA on raw words counts
tf_vectorizer = CountVectorizer(max_df=0.8,
                                min_df=5,
                                stop_words='english')
tf = tf_vectorizer.fit_transform(documents)
tf_feature_names = tf_vectorizer.get_feature_names()

lda = LatentDirichletAllocation(n_topics=n_topics)
lda_doc_topic = lda.fit_transform(tf)
print('LDA doc-topic shape:', lda_doc_topic.shape)

no_top_words = 15
print('\nNMF top terms:')
display_topics(nmf, tfidf_feature_names, no_top_words)
print('\nLDA top terms:')
display_topics(lda, tf_feature_names, no_top_words)