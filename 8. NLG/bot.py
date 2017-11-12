import xml.etree.ElementTree as ET
import re
import random

tree = ET.parse('Astronauts.xml')
root = tree.getroot()

triples = list()
answers = dict()

for entry in root.iter('entry'):
    originaltripleset = entry.find('originaltripleset')
    otriple = originaltripleset.find('otriple')
    triples.append((otriple.text, re.sub('_', ' ', otriple.text).split(' | ')))
    triple_answers = entry.findall('lex')
    triple_answers = [ans.text for ans in triple_answers]
    answers[otriple.text] = triple_answers

rel_phrase = {'almaMater': ['Alma Mater', 'alma mater', 'graduate', 'degree', 'studied', 'university', 'study'],
              'birthDate': ['was born', 'birthday', 'born'],
              'birthPlace': ['was born'],
              'birthName': ['birth name'],
              'dateOfRet': ['retire'],
              'occupation': ['work', 'job', 'occupation'], # what does/did he do
              'status': ['status', 'job'], # what does he do
              'timeInSpace': ['space'],
              'mission': ['mission'],
              'selection': ['select', 'hire'],
              'deathDate': ['died', 'die', 'death'],
              'nationality': ['nationality'],
              'ribbon': ['award', 'won'],
              'awards': ['award', 'won'],
              'operator': ['operator', 'operate'],
              'alternativeNames': ['known', 'real name'],
              'crew1Up': ['command'],
              'crewMembers': ['member', 'crew', 'crewman'],
              'crew2Up': ['pilot', 'backup pilot'],
              }

objects = ['Alan Bean', "Alan Bean's", 'Alan Shepard', "Alan Shepard's",
           'Apollo 11', 'Apollo 12', 'Apollo 8', 'Buzz Aldrin', "Buzz Aldrin's",
           'Elliot See', "Elliot See's", 'William Anders', "'William Anders'"]

class GetOutOfLoop(Exception):
    def __init__(self, q):
        self.sorry = "Sorry, I don't know anything about it.."
        q = re.sub('\?', '', q)
        q = re.sub(' ', '+', q)
        self.google = "You can try googling it: https://www.google.com/search?q=" + q + '\n\n'

question = 'start'
while question.lower() != 'stop':
    question = input('Please enter your question. If you want to quit the chat-bot, please type "stop"...\n')
    if question.lower() == 'stop':
        break
    try:
        obj_found = False
        rel_found = False
        triple_found = False
        for obj in objects:
            if obj in question:
                object = re.sub(' ', '_', obj)
                obj_found = True
        if not obj_found:
            raise GetOutOfLoop(question)
        for rel0 in rel_phrase:
            for rel in rel_phrase[rel0]:
                if rel in question:
                    relation = rel0
                    rel_found = True
        if not rel_found:
            if 'does' in question or 'did' in question and 'do' in question:
                relation = 'occupation'
            if 'where' in question and 'from' in question:
                relation = 'nationality'
            else:
                raise GetOutOfLoop(question)
        for triple in triples:
            triple_0 = triple[0]
            triple_1 = triple[1]
            if object in triple_0 and relation in triple_0:
                triple_found = True
                print(random.choice(answers[triple_0]), '\n\n')
        if not triple_found:
            raise GetOutOfLoop(question)
    except GetOutOfLoop as e:
        print(e.sorry, e.google)