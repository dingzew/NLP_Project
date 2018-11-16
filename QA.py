import nltk
from sys import stdin
from nltk.tag.stanford import StanfordNERTagger
from nltk.tag import StanfordNERTagger
#from nltk.tag.stanford import NERTagger
from stanford_utils import *


def tokenizeDoc(cur_doc):
    return re.findall('\\w+', cur_doc)

def tokenizeSent(text):
    return nltk.sent_tokenize(text)

def tokenizeWord(sentence):
    return nltk.word_tokenize(sentence)

def tagSent(sentence):
    tokens = tokenizeWord(sentence)
    path_to_model = "stanford-ner/classifiers/english.conll.4class.distsim.crf.ser.gz"
    path_to_jar = "stanford-ner/stanford-ner.jar"
    st = StanfordNERTagger(path_to_model, path_to_jar)
    return st.tag(tokens)

def who(question, sentence):
    tags = tagSent(sentence)
    for tag in tags:
        if tag[1] == "PERSON":
            return tag[0]
    return sentence

def when(question, sentence):
    tags = tagSent(sentence)
    return sentence

def where(question, sentence):
    tags = tagSent(sentence)
    answer = ""
    for tag in tags:
        if tag[1] == "LOCATION":
            answer += tag[0]+" "
    if answer != "":
        return answer
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
    return sentence

def yesno(question, sentence):
    tags = tagSent(sentence)
    return sentence

def getSent(words):
    return "Alice knows last year about New York at 10:00a.m."

for line in stdin:
    sentence = getSent(line)
    words = line.lower().split()
    if len(words) < 2:
        print("Could you be more specific?")
        continue
    if words[0] == "who" or (words[0] == "to" and words == "whom"):
        print(who(line, sentence))
    elif words[0] == "when":
        print(when(line, sentence))
    elif words[0] == "where":
        print(where(line, sentence))
    elif words[0] == "what":
        print(what(line, sentence))
    elif words[0] == "which":
        print(which(line, sentence))
    elif words[0] == "how" and words[1] == "many":
        print(howmany(line, sentence))
    elif words[0] == "how" and words[1] == "much":
        print(howmuch(line, sentence))
    elif words[0] == "how":
        print(how(line, sentence))
    else:
        print(yesno(line, sentence))

