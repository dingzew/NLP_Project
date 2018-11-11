import nltk
from nltk.tree import Tree
from nltk import word_tokenize
from nltk.corpus import stopwords
import string
import os
import re
import sys

class Answer(object):
    def __init__(self, sentences, question):
        self.sentences = sentences
        self.question = question
        self.length = 0
        for s in self.sentences:
            for word in self.question:
                self.length += s.count(word)

        self.sentences = self.preprocessSentence(self.sentences)
        self.questionDict = self.compQues(self.question)
        self.sentDict = self.calculToken(self.sentences)
        self.vectorList = self.similarity(self.sentDict, self.question)

    def preprocessSentence(self, sentList):
        for words in sentList:
            words = [w for w in words if w not in stopwords and not w.isdigit()]
        return sentList

    # take in a sentence of words
    def calculToken(self, sentList, questionDict):
        questionSet = questionDict.keys()
        vocabulary = set()
        sentDictList = []

        for words in sentList:
            d = dict()
            for word in questionSet:
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
        return sentDict[word]

    def inverseFreq(self, word, sentDict):
        count = 0
        if word in sentDict:
            count += 1
        return math.log(len(self.sentences) / (count + 1))

    def similarity(self, question):
        vectorList = []
        for sent in self.sentDictList:
            vector = []
            for word in question:
                tfidf = self.termFreq(sent, word) * self.inverseFreq(word, sent)
                vector.append(tfidf)
            vectorList.append(vector)
        return vectorList

with open ("data/set1/a1/txt", "r") as doc:
    text = doc.read()
    sent_text = nltk.sent_tokenize(text)
    for sentence in sent_text:
        tokenized_text = nltk.word_tokenize(sentence)
        tagged = nltk.pos_tag(tokenized_text) 