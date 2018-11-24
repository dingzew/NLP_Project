#!/usr/bin/env python3

import nltk
from nltk.tree import Tree
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.corpus import wordnet
import string
import os
import re
import sys
import math

from nltk.stem.wordnet import WordNetLemmatizer
import answer_yesno
from process import *
from tree_file import *
# nltk.download('punkt')
# nltk.download('stopwords')
lemma = WordNetLemmatizer()
VERB = ["VB","VBZ","VBP","VBD","VBN","VBG"]

class Answer(object):
    def __init__(self, orig, sentences):
        self.original = orig
        self.length = 0
        self.sentences = self.preprocessSentence(sentences) # tokenized
    
    def setQuestion(self, question):
        self.raw_question = question
        self.tag = getTag(question)
        self.question = re.compile('\w+').findall(question.lower())
        self.questionSynset = self.preprocessQuestion()
        self.questionDict = self.compQues(self.question)
        self.sentDict = self.calculToken(self.sentences, self.questionDict)
        self.vectorList = self.similarity(self.question)

    def preprocessSentence(self, sentList):
        for index,words in enumerate(sentList):
            sentList[index] = [lemma.lemmatize(w) for w in words if w not in stopwords.words()]
        return sentList

    def preprocessQuestion(self):
        questionSynset = []
        for word in self.question:
            questionSynset.append(wordnet.synsets(word))
        return questionSynset

    # take in a sentence of words
    def calculToken(self, sentList, questionDict):
        questionSet = questionDict.keys()
        vocabulary = set()
        sentDictList = []

        for words in sentList:
            d = dict()
            for word in words:
                if word in questionDict:
                    d[word] = d.get(word, 0) + 1
            for word in d:
                d[word] = d[word] / len(words)
            sentDictList.append(d)
        return sentDictList

    def compQues(self, questionList):
        d = dict()
        for word in questionList:
            d[word] = d.get(word, 0) + 1
        return d

    def termFreq(self, sentDict, word):
        return sentDict.get(word, 0)

    def inverseFreq(self, word):
        count = 0
        for sent in self.sentDict:
            if word in sent:
                count += 1
        return math.log(len(self.sentences) / (count + 1))

    def similarity(self, question):
        tokens = nltk.word_tokenize(self.raw_question)
        path_to_model = "stanford-ner/classifiers/english.muc.7class.distsim.crf.ser.gz"
        path_to_jar = "stanford-ner/stanford-ner.jar"
        st = StanfordNERTagger(path_to_model, path_to_jar)
        question = st.tag(tokens)
#       
        vectorList = []
        for sent in self.sentDict:
            vector = []
            for word,tag in question:
                word = word.lower()
                tfidf = self.termFreq(sent, word) * self.inverseFreq(word)
                if tag != 'O':
                    tfidf *= 2
                vector.append(tfidf)
            vectorList.append(vector)
        return vectorList

    def getSentence(self):
        score = []
        for j in range(len(self.vectorList)):
            vector = self.vectorList[j]
            curr_sum = sum([i for i in vector])
            score.append((curr_sum, j))
            score.sort(key = lambda x : x[0], reverse=True)
        j = 0
        while True:
            res = []
            parsed_ques = generateTree(self.original[score[j][1]])
            for tag in VERB:
                res += get_phrases(parsed_ques, tag)
            if len(res) > 0:
                break
            j += 1
        return score[j][1]
        # get the highest ranked sentences

    def answer_yesno(self):
        target_index = self.getSentence()
        target = self.original[target_index]
        answer = answer_yesno.get_ans_wrapper(self.raw_question, target)
        if answer:
            return "Yes."
        else:
            return "No."

    def answer_wh(self):
        target_index = self.getSentence()
        target = self.original[target_index]
        return target

    def get_answer(self):
        if self.tag == "YESNO":
            return self.answer_yesno()
        else:
            sent = self.answer_wh()
            if self.tag == "WHO":
                return who(self.question, sent)
            elif self.tag == "WHERE":
                return where(self.question, sent)
            elif self.tag == "WHEN":
                return when(self.question, sent)
            elif self.tag == "WHAT":
                return what(self.question, sent)
            elif self.tag == "WHICH":
                return which(self.question, sent)
            elif self.tag == "HOW":
                return how(self.question, sent)
            elif self.tag == "HOWMANY":
                return howmany(self.question, sent)
            elif self.tag == "HOWMUCH":
                return howmuch(self.question, sent)
            elif self.tag == "WHY":
                return why(self.question, sent)
            else:
                return sent

''' test script
text = "Early life and education\nDonovan was born on March 4, 1982, in Ontario, California, to Donna Kenney-Cash, a special education teacher, and Tim Donovan, a semi-professional ice hockey player originally from Canada, which makes Donovan a Canadian citizen by descent. His mother raised him and his siblings in Redlands, California.\nWhen Donovan was six, his mother allowed him to join an organized league, and he scored seven goals in his first game. Donovan was a member of Cal Heat – a club based in nearby Rancho Cucamonga under coach Clint Greenwood. In 1997, he was accepted into U.S. Youth Soccer's Olympic Development Program. He attended Redlands East Valley High School when not engaged in soccer activities elsewhere. In 1999, Donovan attended the IMG Academy in Bradenton, Florida, part of U.S. Soccer's training program."
sent_text = nltk.sent_tokenize(text)
token = []
for sentence in sent_text:
    tokenized_text = nltk.word_tokenize(sentence)
    token.append(tokenized_text)
question = "Who was born in California".split()
A = Answer(token, question)
'''

def main(argv):
    articleLoc = argv[1]
    questionLoc = argv[2]
    with open (articleLoc, "r", encoding="utf-8") as art_doc:
        article = art_doc.read()
        # article = art_doc.decode('utf-8')
        article = article.split('\n')[1:]
        article = " ".join(article)
        article = article.encode('ascii', errors='ignore') 
        article = article.decode("ascii")

    sent_text = nltk.sent_tokenize(article)
    sent_text = [s for s in sent_text]
    token_list = []
    for sentence in sent_text:
        tokenized_text = nltk.word_tokenize(sentence)
        res = [w.lower() for w in tokenized_text]

        token_list.append(res)

    with open (questionLoc, "r", encoding="utf-8") as ques_doc:
        question = ques_doc.read()
        question = question.encode('ascii', errors='ignore')
        question = question.decode("ascii")

    question_list = question.split("\n")
    A = Answer(sent_text, token_list)
    for ques in question_list:
        A.setQuestion(ques)
        print (A.get_answer())

    art_doc.close()
    ques_doc.close()

if __name__ == "__main__":
    main(sys.argv)
