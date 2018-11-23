import nltk
from sys import stdin
from nltk.tag.stanford import StanfordNERTagger
from nltk.tag import StanfordNERTagger
from stanford_utils import *


def tokenizeDoc(cur_doc):
    return re.findall('\\w+', cur_doc)

def tokenizeSent(text):
    return nltk.sent_tokenize(text)

def tokenizeWord(sentence):
    return nltk.word_tokenize(sentence)

def tagSent(sentence):
    tokens = tokenizeWord(sentence)
    path_to_model = "stanford-ner/classifiers/english.muc.7class.distsim.crf.ser.gz"
    path_to_jar = "stanford-ner/stanford-ner.jar"
    st = StanfordNERTagger(path_to_model, path_to_jar)
    return st.tag(tokens)

def who(question, sentence):
    tags = tagSent(sentence)
    answer = [tag[0] for tag in tags if tag[1] == 'PERSON']
    if len(answer):
        return ' '.join(answer)
    else:
        return sentence

def when(question, sentence):
    tags = tagSent(sentence)
    answer = [tag[0] for tag in tags if tag[1] == 'DATE' or tag[1] == 'TIME']
    if len(answer):
        return ' '.join(answer)
    else:
        return sentence

def where(question, sentence):
    tags = tagSent(sentence)
    answer = [tag[0] for tag in tags if tag[1] == 'LOCATION']
    if len(answer):
        return ' '.join(answer)
    else:
        return sentence

def what(question, sentence):
    tags = tagSent(sentence)
    return sentence

def which(question, sentence):
    tags = tagSent(sentence)
    return sentence

def how(question, sentence):
    tags = tagSent(sentence)
    return sentence

def howmany(question, sentence):
    tags = tagSent(sentence)
    return sentence

def howmuch(question, sentence):
    tags = tagSent(sentence)
    answer = [tag[0] for tag in tags if tag[1] == 'MONEY']
    if len(answer):
        return ' '.join(answer)
    else:
        return sentence

def yesno(question, sentence):
    tags = tagSent(sentence)
    return sentence


def getTag(line):
    words = line.lower().split()
    # if len(words) < 2:
        # print("Could you be more specific?")
        # continue
    if words[0] == "who":# or (words[0] == "to" and words[1] == "whom"):
        return "WHO"
    elif words[0] == "when":
        return "WHEN"
    elif words[0] == "where":
        return "WHERE"
    elif words[0] == "what":
        return "WHAT"
    elif words[0] == "which":
        return "WHICH"
    elif words[0] == "how" and words[1] == "many":
        return "HOWMANY"
    elif words[0] == "how" and words[1] == "much":
        return "HOWMUCH"
    elif words[0] == "how":
        return "HOW"
    elif words[0] == "why":
        return "WHY"
    else:
        return "YESNO"

