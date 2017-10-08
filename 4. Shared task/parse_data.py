import xml.etree.ElementTree as ET
import re
import random

tree = ET.parse('train-data.xml')
root = tree.getroot()
data = list()
instances = root.findall("./instance")
for i in range(3):
    text_data = list()
    text = instances[i].findtext('./text')
    text_data.append(text.lower())
    questions = instances[i].findall('./questions/question')
    for question in questions:
        question_data = list()
        question_data.append(question.attrib['text'].lower())
        answers = dict()
        for answer in question.findall('./answer'):
            answers[re.sub('\.', '', answer.attrib['text'].lower())] = answer.attrib['correct']
        question_data.append(answers)
        text_data.append(question_data)
    data.append(text_data)

# text = 0, questions = [1:]

test = data[0]
text = test[0]
questions = test[1:]
for q in questions:
    print(q[0])
    print(q[1])
    predicted = dict()
    answers = q[1]
    if 'yes' not in answers.keys():
        for el in answers.keys():
            if el in text:
                predicted[el] = 'True'
            else:
                predicted[el] = 'False'
    else:
        true_answer = random.choice(['yes', 'no'])
        predicted[true_answer] = 'True'
        predicted[['yes', 'no'].remove(true_answer)[0]] = 'False'
    print(predicted)







#print(root.findall("./instance/questions")[0])