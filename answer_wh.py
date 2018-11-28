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
verb_list = ['do','will','can','would','could', 'be']
noun_tags = ["NN","NNS"]
verb_tags = ["VB","VBZ","VBP","VBD","VBN","VBG"]
adj_tags = ["JJ","JJR","JJS","RB","RBS","RBR"]

def get_because(ans_list):
    because_list = ["because", "because of", "since", "due to", "thanks to", "to"]
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
                return index
        return len(ans_list)
    else: # go backwards
        for index in range(len(ans_list)-1,-1,-1):
            word = ans_list[index]
            if word in string.punctuation:
                return index
        return -1

def why_helper(question, target):
    # ans_tree = generateTree(target.lower())
    ans_list = nltk.word_tokenize(target)
    (because_word, start, getAfter) = get_because(ans_list)
    len_be = len(because_word.split())
    if start == -1:
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

def get_vptags(ptree):
    result = []
    for tag in ["VB", "VBZ", "VBD"]:
        nptree = get_subtree(ptree, tag)
        if nptree != None:
            np_sub = get_list_of_tags(nptree, tag)
            maxStrNP = ""
            for s in np_sub:
                if len(s) > len(maxStrNP):
                    maxStrNP = s
            result.append(maxStrNP)
    return result

def reformulate_what(question):
    ptree = generateTree(question)
    whnp = get_list_of_tags(ptree, "WHNP")
    if len(whnp) == 0:
        whnp = question.split()[0]
    rest = question[question.find(whnp[0])+len(whnp[0]):]
    sentence = get_list_of_tags(ptree, "S")

    if len(sentence) != 0:
        # is object
        return ("OBJ", [sentence[0]])
    # is subject
    to_classify = rest.split()[0]
    
    if get_subtree(ptree, "VP") != None:
    # if lemma.lemmatize(to_classify,'v') != "be":
        if lemma.lemmatize(to_classify,'v') not in verb_list:
            # is object
            return ("OBJ", [" ".join(rest.split()[1:])])
        # get NP + VP pattern
        subtree = get_subtree(ptree, "VP")
        pp = get_list_of_tags(subtree, "PP")
        # if len(pp) != 0:
            # return ("NV", get_nvtags(ptree, ["NP"]) + get_vptags(subtree) + get_nvtags(subtree, ["PP"]))
        # else:
        return ("NV", get_nvtags(ptree, ["NP","VP"]))
    else:
        return ("NN", [" ".join(rest.split()[1:])])

    return None

def reformulate_how(question):
    ptree = generateTree(question)
    
    whnp = get_list_of_tags(ptree, "WHADVP")
    if len(whnp) == 0:
        whnp = question.split()[0]
    rest = question[question.find(whnp[0])+len(whnp[0]):]
    sentence = get_list_of_tags(ptree, "S")
    if len(sentence) != 0:
        # is object
        return ("OBJ", get_nvtags(ptree, ["NP","VP"]))
    # is subject
    return ("VB", get_nvtags(ptree, ["NP","VP"]))

def reformulate_which(question):
    ptree = generateTree(question)
    whnp = get_list_of_tags(ptree, "WHNP")
    question = question.replace(" ".join(whnp), "what")
    return reformulate_what(question)

def get_what_answer(question, qtag, answer):
    question = question.lower()
    answer = answer.lower()

    # special case
    if question.startswith("what happened"):
        check = question.split()
        rest = " ".join(check[2:]) 
        if rest in answer:
            res = answer[:answer.find(rest)]
            if (len(res) > 1):
                return res.strip()
            else:
                return answer[answer.find(rest)+len(rest):].strip()
        else:
            return answer

    ptree = generateTree(question)
    if qtag == "HOW":
        whnp = get_list_of_tags(ptree, "WHADVP")
        if len(whnp) == 0:
            whnp = get_list_of_tags(ptree, "WHADJP")
    else:
        whnp = get_list_of_tags(ptree, "WHNP")
    if len(whnp) == 0:
        whnp = question.split()[0]
    rest = question[question.find(whnp[0])+len(whnp[0]):]
    ans_list = answer.split()
    check = question.split()
    head = rest.split()

    if "say" in question and "that" in answer:
        return answer[answer.find("that") + 4:].strip()
    (tag, keyword) = reformulate(question, qtag)

    # check be + NP
    if tag == "NN" or tag == "VB" or tag == "OBJ":
        verb = check[check.index(head[0]) - 1]
        if rest in answer:
            guess = ans_list[ans_list.index(verb) - 1]
            if guess == verb or lemma.lemmatize(guess, "v") == lemma.lemmatize(verb, "v"):
                return answer[:answer.find(rest)-len(verb)-1].strip()
            if ans_list.index(verb) + 1 < len(ans_list):
                guess = ans_list[ans_list.index(verb) + 1]
                if guess == verb or lemma.lemmatize(guess, "v") == lemma.lemmatize(verb, "v"):
                    return answer[answer.find(rest)+len(guess)+1:].strip()
        if keyword[0] in answer:
            res = answer[answer.find(keyword[0])+len(keyword[0]):].split()
            res = [i for i in res if i not in string.punctuation]
            return " ".join(res)

    # check be/have/do/can + NP, VP
    if tag == "NV":
        # get vp keyword
        if len(keyword) == 2:
            noun = keyword[0]
            noun_start = noun.split()[0]
            noun_end = noun.split()[-1]
            verb = keyword[1]
            if noun in answer:
                if noun_start in ans_list:
                    guess = ans_list[ans_list.index(noun_start) - 1]
                    if guess in verb or lemma.lemmatize(guess, "v") == lemma.lemmatize(verb, "v"):
                        return answer[:answer.find(noun_start)-len(verb)-1].strip()
                if noun_end in ans_list and ans_list.index(noun_end) + 1 < len(ans_list):
                    guess = ans_list[ans_list.index(noun_end) + 1]
                    if guess in verb or lemma.lemmatize(guess, "v") == lemma.lemmatize(verb, "v"):
                        return answer[answer.find(noun_end)+len(guess)+1:].strip()
            if verb in answer:
                if answer.index(verb) + 1 < len(answer):
                    guess = answer[answer.index(verb)+len(verb):]
                    if guess.split()[0] in ["ed", "es"] or len(guess.split()[0]) <= 1:
                        return (" ".join(guess.split()[1:])).strip()

        if len(keyword) == 3:
            noun = keyword[0]
            noun_start = noun.split()[0]
            noun_end = noun.split()[-1]
            verb = keyword[1]
            pp = keyword[2]
            pp_start = pp.split()[0]
            if pp_start in ans_list:
                res = ans_list[:ans_list.index(pp)]
                if noun_end in res:
                    if res.index(noun_end) + 1 < len(res):
                        guess = res[res.index(noun_end) + 1]
                        if guess == verb or lemma.lemmatize(guess, "v") == lemma.lemmatize(verb, "v"):
                            res_str = " ".join(res)
                            return res_str[res_str.find(noun_end)+len(guess)+1:].strip()
    return answer

def get_none(question, qtag, answer):
    if question[-1] in string.punctuation:
        question = question[:-1]
    whword_list = ["what", "who", "where", "how", "why", "what", "which", "how much", "how many"]
    ans_list = answer.split()
    for word in whword_list:
        if word in question:
            front = question[:question.find(word)].strip()

            front_list = front.split()
            check_len = min(2, len(front_list))
            if check_len == 0: return answer
            check = " ".join(front_list[-check_len:])
            if check in answer:
                return answer[answer.find(check) + len(check):].strip()        
    return answer


def get_obj(sentence):
    tree = generateTree(sentence)
    np_tag = get_list_of_tags(tree, "NP")
    return np_tag[0]
