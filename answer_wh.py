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
verb_list = ['do','will','can','would','could','be']

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

def get_list_of_tags(sentence_tree, tag_type):
    phrase_str = [" ".join(leaf for leaf in tree.leaves()) 
                      for tree in sentence_tree.subtrees() if tree.label() == tag_type]
    return phrase_str

def get_tag(sentence_tree, word):
    phrase_str = [tree.label()
                  for tree in sentence_tree.subtrees() if (len(tree.leaves()) == 1 and tree.leaves()[0] == word)]
    return phrase_str

# only which, what, how type
def get_ques(question, question_list, question_type):
    if question_type != "NONE":
        return reformulate(question, question_type)
    else:
        tree = generateTree(question)
        whword = get_list_of_tags(tree, "WHNP")
        index = question_list.index(whword[0])
        return ("NONE", question_list[:index] + whword)

# preprocess question as a list of lower case words
def reformulate(question, question_type):
    # what or how or which
    if question_type == "WHAT":
        (tag, keywords) = reformulate_what(question)
        return (tag, keywords)
    if question_type == "HOW":
        (tag, keywords) = reformulate_how(question)
        return (tag, keywords)
    if question_type == "WHICH":
        (tag, keywords) = reformulate_which(question)
        return (tag, keywords)

def get_subtree(tree, tag):
    if type(tree) == type("") or len(tree.leaves()) == 0:
        return
    for subtree in tree:
        if type(subtree) != type("") and subtree.label() == tag:
            return subtree
        res = get_subtree(subtree, tag)
        if res:
            return res

def get_nvtags(ptree, tag_list):
    result = []
    for tag in tag_list:
        nptree = get_subtree(ptree, tag)
        np_sub = get_list_of_tags(nptree, tag)
        maxStrNP = ""
        for s in np_sub:
            if len(s) > len(maxStrNP):
                maxStrNP = s
        result.append(maxStrNP)
    return result

def reformulate_what(question):
    ptree = generateTree(question)
    if question.startswith("what happened"):
        return ("PP", question[question.find("what happened")+len("what happened"):])

    whnp = get_list_of_tags(ptree, "WHNP")

    rest = question[question.find(whnp[0])+len(whnp[0]):]
    sentence = get_list_of_tags(ptree, "S")
    if len(sentence) != 0:
        # is object
        return ("OBJ", sentence[0])
    # is subject
    to_classify = rest.split()[0]
    tag = get_tag(ptree, to_classify)
    if len(tag) > 0:
        if tag[0] == "VBD" or tag[0] == "VBP":
            if lemma.lemmatize(to_classify,'v') not in verb_list:
                # is object
                return ("OBJ", sentence[0])
            # get NP + VP pattern
            subtree = get_subtree(ptree, "VP")
            pp = get_list_of_tags(subtree, "PP")
            if len(pp) != 0:
                return ("NVP", get_nvtags(ptree, ["NP","VP","PP"]))
            else:
                return ("NV", get_nvtags(ptree, ["NP","VP"]))

        if tag[0] == "VBZ":
            nptree = get_nvtags(ptree, ["NP"])
            return ("VBZ", nptree)
        else:
            print(tag)
    return None

def reformulate_how(question):
    ptree = generateTree(question)
    
    whnp = get_list_of_tags(ptree, "WHADVP")
    rest = question[question.find(whnp[0])+len(whnp[0]):]
    sentence = get_list_of_tags(ptree, "S")
    if len(sentence) != 0:
        # is object
        return ("OBJ", sentence[0])
    # is subject
    return ("NV", get_nvtags(ptree, ["NP","VP"]))

def reformulate_which(question):
    ptree = generateTree(question)
    whnp = get_list_of_tags(ptree, "WHNP")
    question = question.replace(whnp, "what")
    return reformulate_what(question)

def get_answer(keyword, tag, answer):
    for ans in keyword, 

target = [("How did the supporters of Henry Clay feel about Fillmore in 1848?", "HOW"),
          ("What did Taylor and Fillmore disagree upon", "WHAT"),
          ("What do river otters eat", "WHAT"),
          ("What is the primary item in an otter's diet", "WHAT")]
for sent in target:
    res = reformulate(sent[0], sent[1])
    print(res)