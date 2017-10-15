from nltk.corpus import wordnet
from nltk.wsd import lesk


# http://www.nltk.org/howto/wordnet.html
# http://compprag.christopherpotts.net/wordnet.html

car_synsets = wordnet.synsets('car', 'n')
for synset in car_synsets:
    print(synset, synset.lemmas())

print('\nPlant_VERB:')
for synset in wordnet.synsets('plant', pos=wordnet.VERB):
    print()
    print(synset)
    print(synset.definition())

print('')


print('\nPlant_N_01')
synset = wordnet.synset('look.n.03')
print('lemmas:', synset.lemmas())
print(synset.examples())

print('hypernyms:', synset.hypernyms())
print('hyponyms:', synset.hyponyms())


print('lowest_common_hypernym, rice&soup:',
      wordnet.synset('rice.n.01').lowest_common_hypernyms(wordnet.synset('soup.n.01')))


# similarity/distance
# http://atlas.ahc.umn.edu/umls_similarity/similarity_measures.html
dog = wordnet.synset('dog.n.01')
cat = wordnet.synset('man.n.01')

sim = dog.path_similarity(cat)    # shortest path similarity
dist = dog.shortest_path_distance(cat)
print('Distance', sim, dist)


# http://www.nltk.org/howto/wsd.html

# sent = 'I went to the bank to deposit money'.split()

# print(lesk(sent, 'bank', 'n'))












