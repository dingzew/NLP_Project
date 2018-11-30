#!/home/anaconda3.6/bin/python3.6
from random import shuffle, choice
from stanford_utils import new_NERtagger
import sys
import json
import nltk
import question
import tree_file
from tree_file import Trie
import NER_file

tagger = new_NERtagger()

def append_if_not_None(arr, ele):
    if ele is not None:
        arr.append(ele)

def ask(line, persons, orgs):
    line = line.replace(",", " ,")
    line = line.replace(".", " .")
    ner_tags = tagger.tag(line.split())
    raw_tree = tree_file.generateTree(line)
    ner_tree = tree_file.stanfordNE2tree(ner_tags)
    qs = []
    append_if_not_None(qs, question.askBinary(line, raw_tree, persons, orgs))
    append_if_not_None(qs, question.askWhen(line, raw_tree, ner_tree, persons, orgs))
    append_if_not_None(qs, question.askSubject(line, raw_tree, ner_tree, persons, orgs))
    append_if_not_None(qs, question.askWhere(line, raw_tree, ner_tree, persons, orgs))
    '''
    append_if_not_None(qs, question1.askDoWhat(tree))
    '''
    return qs

if __name__ == '__main__':
    _, input_file, N = sys.argv
    N = int(N)
    total = []
    persons = Trie()
    orgs = Trie()

    with open(input_file, encoding="utf-8") as inp:
        for line in inp:
            sentences = nltk.sent_tokenize(line)
            for sent in sentences:
                try:
                    ner_tags = tagger.tag(nltk.word_tokenize(sent))
                    ner_tree = tree_file.stanfordNE2tree(ner_tags)
                    for ele in ner_tree:
                        if type(ele) == nltk.Tree:
                            if ele.label() == "PERSON":
                                for x in ele.leaves():
                                    persons.add(x[0].lower())
                            elif ele.label() == "ORGANIZATION":
                                for x in ele.leaves():
                                    orgs.add(x[0].lower())
                except Exception as e:
                    pass
    pronouns = ["i", "you", "he", "she", "it", "they"]
    for pron in pronouns:
        persons.add(pron)

    with open(input_file, encoding="utf-8") as inp:
        data = list(inp)
        shuffle(data)
        for line in data:
            sentences = nltk.sent_tokenize(line)
            for sent in sentences:
                try:
                    if "–" in sent or ":" in sent or "-" in sent or "(" in sent or ")" in sent or "^" in sent or "'m" in sent or "'ve" in sent or "'d" in sent or "'s" in sent or "as of" in sent.lower():
                        continue
                    if sent and sent[-1] == '.':
                        qs = ask(sent, persons, orgs)
                        if qs:
                            for q in qs:
                                total.append(q)
                                print(q)
                                N -= 1
                                if N == 0:
                                    break
                            if N == 0:
                                break
                except Exception as e:
                    pass
            if N == 0: 
                break
    if total: 
        while N > 0:
            print(total[N % len(total)])
            N -= 1

