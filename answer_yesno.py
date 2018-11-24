import nltk
from nltk.tree import Tree
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem.porter import *
import string
import os
import re
import sys
import math
from stanford_utils import *
from tree_file import *

stemmer = PorterStemmer()
lemma = WordNetLemmatizer()
yesno_list = ['be','have','do','will','can','would','could','']

def positive_exist(word, patt_tree):
    morphy = lemma.lemmatize(word)
    synset = wordnet.synsets(word)
    for sub in patt_tree:
        for cand in sub.leaves():
            if word == cand:
                return True
            for syn in synset: 
                for lem in syn.lemmas(): 
                    if cand == lem.name() or lemma.lemmatize(cand) == lem.name():
                        return True
                    for ant in lem.antonyms():
                        if cand == ant.name():
                            return False
    return False


def get_yesno_answer(question_list, question, target):
    if (len(question_list) == 0):
        return question
    feature = lemma.lemmatize(question_list[0].lower(),'v')

    if (feature.lower() not in yesno_list):
        return question
    # output yes/no instance
    parsed_ques = generateTree(question)
    parsed_ans = generateTree(target)

    labels = [["NN","NNS","NNP","NNPS"]]
              #["VB","VBZ","VBP","VBD","VBN","VBG"],
              #["JJ","JJR","JJS"],
              #["RB","RBS","RBR"]]

    for label_set in labels:
        ques_label = []
        ans_label = []
        for label in label_set:
            ques_label += get_phrases(parsed_ques, label)
            ans_label += get_phrases(parsed_ans, label)

        for tree in ques_label:
            word = tree.leaves()[0]
            if not positive_exist(word, ans_label):
                return False

    return True

def get_ans_wrapper(original, question, target):
    print(target)
    ans = get_yesno_answer(original, question, target)
    if "not" in target:
        return not ans
    return ans




