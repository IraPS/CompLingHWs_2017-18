The goal was to try using betweenness centrality of terms candidates' graphs' nodes as a factor of term extracting.

The initial plan was to calculate tf-idf for documents, choose candidates from the top of tf-idf matrices for each text, create graphs basing on these candidates and filter the terms by their betweenness centrality. But my laptop was dying from calculating tf-idf :(

So I put this version in "correct_tf_idf.py" but I didn't succeed running it even on test material.

The current script ("main.py") calculates tf-idf for each document for ngrams from 1 to 4 assuming that one document is the whole collection. Looking into results it seems like it helps extracting some kind of keywords for the document even though it's a fake tf-idf.

The script has two parameters that can be modified: turning on and off lowercase and removing or keeping stopwrods. The stopwords' list is taken from Sklearn library. The graphs are created and betweenness centrality is calculated with Networkx library. 

The evalutation metrics are calcaulated the following way:

if "predicted" term fully mathces with "true" term, precision and recall get +1;

if "predicted" term partially mathces (either "predicted" or "true" term is a substring of another) with "true" term, precision gets +0.5 and recall gets +1;

else both get 0.


