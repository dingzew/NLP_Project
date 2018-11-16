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
# nltk.download('punkt')
# nltk.download('stopwords')
lemma = WordNetLemmatizer()

class Answer(object):
    def __init__(self, orig, sentences, question):
        self.original = orig
        self.question = question
        self.tag = getTag(question)

        self.length = 0

        self.sentences = self.preprocessSentence(sentences) # tokenized
        for s in self.sentences:
            for word in self.question:
                self.length += s.count(word)
        self.questionSynset = self.preprocessQuestion()
        self.questionDict = self.compQues(self.question)
        self.sentDict = self.calculToken(self.sentences, self.questionDict)
        self.vectorList = self.similarity(self.question)

    def preprocessSentence(self, sentList):
        for words in sentList:
            words = [w for w in words if w not in stopwords.words()]
            words = [lemma.lemmatize(w) for w in words]
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
                d[word] = d[word] / self.length
            sentDictList.append(d)
        return sentDictList

    def compQues(self, questionList):
        d = dict()
        for word in questionList:
            d[word] = d.get(word, 0) + 1
        return d

    def termFreq(self, sentDict, word):
        return sentDict.get(word, 0)

    def inverseFreq(self, word, sentDict):
        count = 0
        if word in sentDict:
            count += 1
        return math.log(len(self.sentences) / (count + 1))

    def similarity(self, question):
        vectorList = []
        for sent in self.sentDict:
            vector = []
            for word in question:
                tfidf = self.termFreq(sent, word) * self.inverseFreq(word, sent)
                vector.append(tfidf)
            vectorList.append(vector)
        return vectorList

    def getSentence(self):
        max_sum = 0
        max_index = 0
        for j in range(len(self.vectorList)):
            vector = self.vectorList[j]
            curr_sum = sum([i**2 for i in vector])
            if curr_sum > max_sum:
                max_sum = curr_sum
                max_index = j
        return max_index
        # get the highest ranked sentences

    def answer_yesno(self):
        target_index = self.getSentence()
        target = self.original[target_index]
        answer = answer_yesno.get_ans_wrapper(self.question, target)
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
            if self.tag == "WHERE":
                return where(self.question, sent)
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
        article = article.encode('ascii', errors='ignore') 
        article = article.decode("ascii")

    sent_text = nltk.sent_tokenize(article)
    sent_text = [s for s in sent_text]
    token_list = [] 
    for sentence in sent_text:
        tokenized_text = nltk.word_tokenize(sentence)
        res = []
        for w in tokenized_text:
            
            # w = re.findall(r'[\w.].*[\w.]', s)[0]
            res.append(w.lower())

        token_list.append(res)

    with open (questionLoc, "r", encoding="utf-8") as ques_doc:
        question = ques_doc.read()
        question = question.encode('ascii', errors='ignore')
        question = question.decode("ascii")

    question_list = question.split("\n")
    for ques in question_list:
        #try:
        ques = re.findall(r'[\w.].*[\w.]', ques)[0]
        A = Answer(sent_text, token_list, ques.lower())
        print (A.get_answer())
        # except:
            # print ("NULL")

    art_doc.close()
    ques_doc.close()

if __name__ == "__main__":
    main(sys.argv)
