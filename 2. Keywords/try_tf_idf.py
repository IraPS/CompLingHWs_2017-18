from sklearn.feature_extraction.text import TfidfVectorizer
import os

collection = os.listdir('./dataset')
collection = [file for file in collection if file.endswith('.txt')]
tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 4),
                     min_df = 0, stop_words='english', sublinear_tf=True, lowercase=True)
tfidf_matrix = tf.fit_transform(collection)
feature_names = tf.get_feature_names()
dense = tfidf_matrix.todense()
text = dense[0].tolist()[0]
phrase_scores = [pair for pair in zip(range(0, len(text)), text) if pair[1] > 0]
sorted_phrase_scores = sorted(phrase_scores, key=lambda t: t[1] * -1)
for phrase, score in [(feature_names[word_id], score) for (word_id, score) in sorted_phrase_scores][:20]:
   print('{0: <20} {1}'.format(phrase, score))
