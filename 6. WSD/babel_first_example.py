from urllib.request import urlopen
from pprint import pprint
import json
# from urllib import request

key = "31e6e5aa-404c-4cc1-87b5-31d90af3fb8b"

# http://babelnet.org/guide


def get_babel_version(key):
    url = "https://babelnet.io/v4/getVersion?key={key}".format(key=key)

    response = urlopen(url).read().decode('utf-8')
    ver = json.loads(response)

    print(ver)

# get_babel_version(key)


def synsets_for_word(key, word, lang):

    url = "https://babelnet.io/v4/getSynsetIds?word={word}&langs={lang}&key={key}".format(word=word, lang=lang, key=key)

    response = urlopen(url).read().decode('utf-8')
    ans = json.loads(response)

    pprint(ans)

# synsets_for_word(key, word='bank', lang='EN')


def synset_info(key, synsetId):

    url = "https://babelnet.io/v4/getSynset?id={synsetId}&key={key}".format(synsetId=synsetId, key=key)

    response = urlopen(url).read().decode('utf-8')
    ans = json.loads(response)

    pprint(ans)


# synset_info(key, 'bn:01885340n')


def senses_for_word(word, lang, key):

    url = 'https://babelnet.io/v4/getSenses?word={word}&lang={lang}&key={key}'.format(word=word, lang=lang, key=key)

    response = urlopen(url).read().decode('utf-8')
    ans = json.loads(response)

    print(len(ans))
    pprint(ans)


senses_for_word(key=key, word='plant', lang='EN')


def get_edges(synsetId, key):
    url = 'https://babelnet.io/v4/getEdges?id={synsetId}&key={key}'.format(synsetId=synsetId, key=key)

    response = urlopen(url).read().decode('utf-8')
    ans = json.loads(response)

    pprint(ans)

# get_edges(key=key, synsetId='bn:01885340n')







