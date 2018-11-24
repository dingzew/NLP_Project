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
from stanford_utils import *
from tree_file import *
from process import *


lemma = WordNetLemmatizer()

# when, who 
# why
# how
# what # get object
def get_because(ans_list):
    because_list = ["because", "because of", "since", "due to", "thanks to", "through"]
    result_list = ["as a result", "resulting", "so"]
    for index in range(len(ans_list)):
        word = ans_list[index]
        if word.lower() in because_list:
            return (word, index, True)
        if word.lower() in result_list:
            return (word, index, False)
    return ("", -1, True)

def get_end(ans_list, front):
    if front:
        for index in range(len(ans_list)):
            word = ans_list[index]
            if word in string.punctuation:
                return word
        return len(ans_list)
    else: # go backwards
        for index in range(len(ans_list)-1,-1,-1):
            word = ans_list[index]
            if word in string.punctuation:
                return word
        return -1

def why_helper(question, target):
    # ans_tree = generateTree(target.lower())
    ans_list = nltk.word_tokenize(target)
    (because_word, start, getAfter) = get_because(ans_list)
    len_be = len(because.split())
    if index == -1:
        return target # return default answer
    if getAfter:
        end = get_end(ans_list[start:], True) + start
        return (ans_list[start+len_be],ans_list[end])
    else:
        end = get_end(ans_list[:start], False)
        return (ans_list[end+1],ans_list[start])

def why(question, target):
    (start, end) = why_helper(question, target)
    answer = target[target.find(start):target.find(end)+len(end)]
    return answer[0].upper() + answer[1:]


target = "Since the two sides of the lower jaw are not joined together, the lower incisors are farther apart, giving the kangaroo a wider bite."
