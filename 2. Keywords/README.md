The goal was to try using betweenness centrality of terms candidates' graphs' nodes as a factor of terms extraction.

The initial plan was to calculate tf-idf for documents, choose candidates from the top of tf-idf matrices for each text, create graphs basing on these candidates and filter the terms by their betweenness centrality. But my laptop was dying from calculating tf-idf :(

So I put this version in "correct_tf_idf.py" but I didn't succeed running it even on test material.

The current script ("main.py") calculates tf-idf for each document for ngrams from 1 to 4 assuming that one document is the whole collection. Looking into results it seems like it helps extracting some kind of keywords for the document even though it's a fake tf-idf. The algorighm was tested on 23 documents.

The script has a parameter that can be modified: removing or keeping stopwrods. The stopwords' list is taken from Sklearn library. The graphs are created and betweenness centrality is calculated with Networkx library. The graphs are creating basing on the coocurence matrix for each candidate in each document, the edges' weights' are the number of sentences where candidates appear together in a text.

The (rough) evalutation metrics are calcaulated the following way:

if "predicted" term fully mathces with "true" term, precision and recall get +1;

if "predicted" term partially mathces (either "predicted" or "true" term is a substring of another) with "true" term, precision gets +0.5 and recall gets +1;

else both get 0.

There are two results:
- no stopwords deletion -- the highest F1 is 0.12
- without sotopwords -- the highest F1 is 0.13.

Both of them are on the same text. The overall result is quite low as some texts had 0 for all metrics. 

Removing the stopwords seems to be essential but looking at the dataset it's questionable:

"C-22.key": 'performance and scalability', ..., 'propagation and delivery'

This task gives the understanding that the algorithm of terms extraction should be multifactor (so tf-idf, graphs metrics are not enough). It should be aimed on a particular genre of texts, so the preliminary study of the material is initial. And also, evaluation metrics should be thoroughly developed (not taking into account stopwrods in both "predicted" and "true",  soften or stiffen evaluation depending on which POS is missing when it's a partial match, and etc.).
