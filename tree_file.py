from stanford_utils import *
from nltk import Tree

PARSER = new_parser()


def generateTree(sentence):
    t = PARSER.raw_parse(sentence)
    tree = None
    for sub in t:
        tree = sub
    return tree


def get_phrases(tree, pattern, reversed=False, sort=False):
    phrases = []
    if tree.label() == pattern:
        phrases.append(tree)
    for t in tree.subtrees():
        if t.label() == pattern:
            phrases.append(t)
        # if pattern == "NP" and t.label() == "NNP":
        #     phrases.append(t)
    if sort == True:
        phrases = sorted(phrases, key=lambda x:len(x.leaves()), reverse=reversed)
    return phrases


def merge(tree):
    list = []
    for leaves in tree.leaves():
        list.append(leaves)
    target = ""
    for word in list:
        target += word + " "
    return (target.strip(), tree.label())



def getVerbs(tree):
    list = []
    # list.extend(get_phrases(tree, "VB"))
    # list.extend(get_phrases(tree, "VBD"))
    # list.extend(get_phrases(tree, "VBG"))
    # list.extend(get_phrases(tree, "VBN"))
    # list.extend(get_phrases(tree, "VBP"))
    # list.extend(get_phrases(tree, "VBZ"))
    list.extend(get_phrases(tree, "VP"))
    return list



def testTime(tree):
    if len(get_phrases(tree, "VBD")) != 0:
        return "past"
    if len(get_phrases(tree, "VBP")) != 0:
        return "single"
    if len(get_phrases(tree, "VBZ")) != 0:
        return "single"
    return "now"



def main_sentence_structure(tree):
    dic = {}
    phrases = get_phrases(tree, "NP")
    if not phrases: return dic
    dic["main"] = merge(phrases[0])[0]
    phrases = get_phrases(tree, "VP")
    if not phrases: return dic
    dic["what"] = merge(phrases[0])[0]
    return dic



def fine_structures(tree):
    dic = {}
    phrases = get_phrases(tree, "NP")
    if not phrases: return dic
    dic["main"] = merge(phrases[0])[0]
    phrases = get_phrases(tree, "VP")
    for phrase in phrases:
        if phrase.label().startswith("V"):
            dic["V"] = merge(phrase)[0]
        if phrase.label() == "PP":
            dic["PP"] = merge(phrase)[0]
        if phrase.label() == "NP":
            dic["passive"] = merge(phrase)[0]
    return dic





if __name__ == "__main__":
    # tree = generateTree("Dingze Wang ate an apple in Carnegie Mellon University")
    # print(tree)
    # phrases = get_phrases(tree, "NP")
    # for phrase in phrases:
    #     print(merge(phrase))
    # phrases = get_phrases(tree, "VP")
    # for phrase in phrases:
    #     print(merge(phrase))
    #

    # tree = generateTree("Mary is beaten by David")
    # print(tree)
    # phrases = get_phrases(tree, "NP")
    # for phrase in phrases:
    #     print(merge(phrase))
    # phrases = get_phrases(tree, "VP")
    # for phrase in phrases:
    #     print(merge(phrase))

    tree = generateTree("Dingze Wang ate an apple in Carnegie Mellon University")
    print(tree)
    phrases = get_phrases(tree, "NP")
    for phrase in phrases:
        print(merge(phrase))
    phrases = get_phrases(tree, "VP")
    for phrase in phrases:
        print (phrase)

