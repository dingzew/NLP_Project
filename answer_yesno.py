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

def get_tag(sentence_tree, word):
    phrase_str = [tree.label()
                  for tree in sentence_tree.subtrees() if (len(tree.leaves()) == 1 and lemma.lemmatize(tree.leaves()[0]) == word)]
    return phrase_str

#def positive_exist(word, patt_tree):
#    print(word)
#    morphy = lemma.lemmatize(word)
#    synset = wordnet.synsets(word)
#    for sub in patt_tree:
#        for cand in sub.leaves():
#            if word == cand:
#                return True
#            for syn in synset:
#                for lem in syn.lemmas():
#                    if cand == lem.name() or lemma.lemmatize(cand) == lem.name():
#                        return True
#                    for ant in lem.antonyms():
#                        if cand == ant.name():
#                            return False
#    return False

def positive_exist(word, sent):
    synonyms = []
    for syn in wordnet.synsets(word):
        for l in syn.lemmas():
            synonyms.append(l.name().lower())
    for w in sent:
        if w in synonyms:
            return True
    return False

def negative_exist(word, sent):
    antonyms = []
    for syn in wordnet.synsets(word):
        for l in syn.lemmas():
            if l.antonyms():
                antonyms.append(l.antonyms()[0].name().lower())
    for w in sent:
        if lemma.lemmatize(w,'v') in antonyms:
            return True
    return False

def get_yesno_answer(question_list, question, target, sent_list):
    if (len(question_list) == 0):
        return question
#    feature = lemma.lemmatize(question_list[0].lower(),'v')
#    print(feature)
#    if (feature.lower() not in yesno_list):
#        return question

    # output yes/no instance
    parsed_ques = generateTree(question.lower())
    parsed_ans = generateTree(target.lower())

    N_labels = ["NN","NNS","NNP","NNPS"]
    V_labels = ["VB","VBZ","VBP","VBD","VBN","VBG"]
    A_labels = ["JJ","JJR","JJS"]
    Ad_labels = ["RB","RBS","RBR"]

    has_verb = False
    for word in question_list:
        tags = get_tag(parsed_ques, word)
        if len(tags) == 0:
            continue
        tag = tags[-1]
        if tag in N_labels and has_verb:
            has_verb = False
            if not positive_exist(word, sent_list):
                return False
        
        elif tag in A_labels or tag in V_labels:
            if negative_exist(word, sent_list):
                return False

        has_verb |= tag in V_labels

    return True
#    for label in N_labels:
#        ques_label += get_phrases(parsed_ques, label)
#        ans_label += get_phrases(parsed_ans, label)

#    for label_set in labels:
#        ques_label = []
#        ans_label = []
#        for label in label_set:
#            ques_label += get_phrases(parsed_ques, label)
#            ans_label += get_phrases(parsed_ans, label)
#
#        for tree in ques_label:
#            word = tree.leaves()[0]
#            if not positive_exist(word, ans_label):
#                return False
#
#    return True

def get_ans_wrapper(original, question, target, sent_list):
    print(target)
    ans = get_yesno_answer(original, question, target, sent_list)
    return ans




