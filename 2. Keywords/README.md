I was really trying to do someting unteresting though I didn't succeed because my laptop wasn't able to perfom as needed I guess.

The idea was to compare tf-idf term extraction results to graphs metrics results where nodes are text's ngrams (https://github.com/IraPS/CompLingHWs_2017-18/blob/master/2.%20Keywords/comparing_tfidf_and_centrality.py).

But I couldn't run the cooccurrence matrix creation (for graph construction) on all ngrams (even lowering the ngrams range to (1, 2)).

So what I had to do is chosing some amount of ngrams (range (1, 4)) and it shouldn't have been random (as I understand) and create graphs on them. When I was creating graph on top-500 tf-idf for the text, the results of this was completely identical for both centralities I used (betweenness and degree) and top of tf-idf ngrams: https://github.com/IraPS/CompLingHWs_2017-18/blob/master/2.%20Keywords/comparing_tfidf_and_centrality(toptfidf)_metrics.csv.

So I tried using 250-top and 250-bottom tf-idf ngrams for coocurence calculation which didn't change the situation: https://github.com/IraPS/CompLingHWs_2017-18/blob/master/2.%20Keywords/comparing_tfidf_and_centrality(topdowntfidf)_metrics.csv.

I'd appreciate advice on how to complete this idea - built-in cooccurrence matrix calculation or other tricks? or just a better algorithm for cooccurrence calculation?

After all I decided to compare these results (basically tf-idf) to Rake (https://pypi.python.org/pypi/rake-nltk), and Rake preformed really bad. It didn't introduce any prepoccessing as it seemed and results included symbols or the ngrams were very long and could include just whole unique clauses from the texts.

The (rough) evalutation metrics were calcaulated the following way:

if "predicted" term fully mathced with "true" term, precision and recall got +1;

if "predicted" term partially mathced (either "predicted" or "true" term was a substring of another) with "true" term, precision got +0.5 and recall got +1;

else both got 0.

I also tried to not compare the tfidf and centrality results but use them together and apply centrality as a filter for already chosen candidates. As I couldn't calculate cooccurrence for all ngrams and tfidf and centrality gave me similar results when running centrality algorithm on top of tfidf, I did the following (https://github.com/IraPS/CompLingHWs_2017-18/blob/master/2.%20Keywords/tfidf_plus_centrality.py):

I was calculating tfidf for each document with assumption that this document was the whole collection itself. Then I was chosing nonzero elements from this matrix and it was giving me a list of kind of "important" ngrams (range (1, 4)) for this document which I was filtering with betweenness centrality - chosing top-15 of these. The results are here: https://github.com/IraPS/CompLingHWs_2017-18/blob/master/2.%20Keywords/tfidf_plus_centrality_without_sw_metrics.csv .

The conclusion is that simple tf-idf method seems to be enough for a very basic task, if we're not using ML. The first variant got much better results than the second one. The metrics are so high due to very-verty rough evaluation.

The are some thoughts that term extraction task provokes:

Removing the stopwords seems to be essential but looking at the dataset it's questionable:

"C-22.key": 'performance and scalability', ..., 'propagation and delivery'

The method should be aimed on a particular genre of texts, so the preliminary study of the material is initial. And also, evaluation metrics should be thoroughly developed (not taking into account stopwrods in both "predicted" and "true",  soften or stiffen evaluation depending on which POS is missing when it's a partial match, setting the requested proportion of partical match, and etc.).

Also the golden standard itself is questionable. It's clear how people write the keywords for articles but seems that sometimes these aren't neccessary based on lexical scope of a document and, for example, keywords often have both terms like "roses" and "red roses". If we're aiming on good metrics it's not clear how we draw the line and decide what to take or ditch out of these two.

And some ngram graphs of those "fake" nonzero tf-idf terms from the second variant:
https://github.com/IraPS/CompLingHWs_2017-18/tree/master/2.%20Keywords/graphs
