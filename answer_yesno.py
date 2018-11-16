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


def get_yesno_answer(question, target):
    question_list = question.split()
    if (len(question_list) == 0):
        return question
    feature = lemma.lemmatize(question_list[0].lower(),'v')
    if (feature.lower() not in yesno_list):
        return question
    # output yes/no instance
    parsed_ques = generateTree(question)
    parsed_ans = generateTree(target)

    nouns_label = get_phrases(parsed_ques, "NN") + get_phrases(parsed_ques, "NNS")
    ans_label = get_phrases(parsed_ans, "NN") + get_phrases(parsed_ans, "NNS")
    for tree in nouns_label:
        noun_word = tree.leaves()[0]
        if not positive_exist(noun_word, ans_label):
            return False

    np_label = get_phrases(parsed_ques, "NNP") + get_phrases(parsed_ques, "NNPS")
    ans_label = get_phrases(parsed_ans, "NNP") + get_phrases(parsed_ans, "NNPS")
    for tree in np_label:
        noun_word = tree.leaves()[0]
        if not positive_exist(noun_word, ans_label):
            return False

    # TODO: check verb / adj occurance
    return True

def get_ans_wrapper(question, target):
    ans = get_yesno_answer(question, target)
    if "not" in target:
        return not ans
    return ans



