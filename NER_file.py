from stanford_utils import *

import nltk
from nltk.tokenize import word_tokenize

NER_PARSER = new_NERtagger()

""" 
The section of code below is copied from alvas' answer at https://stackoverflow.com/questions/30664677/extract-list-of-persons-and-organizations-using-stanford-ner-tagger-in-nltk 
"""

def get_continuous_chunks(tagged_sent):
    continuous_chunk = []
    current_chunk = []

    for token, tag in tagged_sent:
        if tag != "O":
            current_chunk.append((token, tag))
        else:
            if current_chunk: # if the current chunk is not empty
                continuous_chunk.append(current_chunk)
                current_chunk = []
    # Flush the final current_chunk into the continuous_chunk, if any.
    if current_chunk:
        continuous_chunk.append(current_chunk)
    named_entities_str_tag = [(" ".join([token for token, tag in ne]), ne[0][1]) for ne in continuous_chunk]
    return named_entities_str_tag

""" 
The section of code above is copied from alvas' answer at https://stackoverflow.com/questions/30664677/extract-list-of-persons-and-organizations-using-stanford-ner-tagger-in-nltk 
"""



"""
def detect_NER_Phrase(phrase):
    tagged_sent = NER_PARSER.tag(phrase.split())
    named_entities = get_continuous_chunks(tagged_sent)
    named_entities_str_tag = [(" ".join([token for token, tag in ne]), ne[0][1]) for ne in named_entities]

    return named_entities_str_tag
"""


def detect_NER_word(sentence):
    tokenized_text = word_tokenize(sentence)
    classified_text = NER_PARSER.tag(tokenized_text)
    return classified_text

def contains_person(sentence):
    list = detect_NER_word(sentence)
    people = set()
    peoplelist = ["he", "she", "it", "they", "we", "i"]

    list = detect_NER_Phrase(sentence)
    for t in list:
        if (t[1] == "PERSON"):
            return True


    for person in peoplelist:
        people.add(person)
    for t in list:
        if (t[1] == "PERSON"):
            return True

    for t in sentence.split(" "):
        if t.lower() in people:
            return True

    return False



def contains_loc(sentence):
    list = detect_NER_word(sentence)
    for t in list:
        if (t[1] == "ORGANIZATION"):
            return True
        if (t[1] == "LOCATION"):
            return True
    list = detect_NER_Phrase(sentence)
    for t in list:
        if (t[1] == "ORGANIZATION"):
            return True
        if (t[1] == "LOCATION"):
            return True
    return False

def get_tokens(sentence):
    tokenized_text = nltk.word_tokenize(sentence)
    tagged = nltk.pos_tag(tokenized_text)
    return tagged

def contains_num(sentence):
    tokens = get_tokens(sentence)
    for i in range(len(tokens)):
        if (i < len(tokens) - 1 and tokens[i][1] == 'CD' and (tokens[i + 1][1] == 'NNS' or tokens[i + 1][1] == 'NN')):
            return tokens[i + 1]
        if (i < len(tokens) - 1 and tokens[i][1] == 'DT' and (tokens[i + 1][1] == 'NNS' or tokens[i + 1][1] == 'NN')):
            return tokens[i + 1]


if __name__ == "__main__":
    # print(detect_NER_Phrase("Carnegie Mellon University"))
    # print(detect_NER_Phrase('While in France, Christine Lagarde discussed short-term stimulus efforts in a recent interview with the Wall Street Journal.'))
    # print(detect_NER_word("Carnegie Mellon University"))
    # print(detect_NER_word('While in France, Christine Lagarde discussed short-term stimulus efforts in a recent interview with the Wall Street Journal.'))
    print(contains_person("Dingze Wang ate an apple in Carnegie Mellon University"))
    print(contains_person("While in France, Christine Lagarde discussed short-term stimulus efforts in a recent interview with the Wall Street Journal."))
    print(contains_person("I ate an apple yesterday"))
    # print(contains_person("While in France, Christine Lagarde discussed short-term stimulus efforts in a recent interview with the Wall Street Journal."))
