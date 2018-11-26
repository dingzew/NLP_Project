from random import shuffle, choice
from stanford_utils import new_NERtagger
import sys
import json
import nltk
import question1
import tree_file
import NER_file

tagger = new_NERtagger()

def append_if_not_None(arr, ele):
    if ele is not None:
        arr.append(ele)

def ask(line):
    line = line.replace(",", " ,")
    line = line.replace(".", " .")
    ner_tags = tagger.tag(line.split())
    raw_tree = nltk.ParentedTree.convert(tree_file.generateTree(line))
    ner_tree = tree_file.stanfordNE2tree(ner_tags)
    qs = []
    print(line)
    print(qs)
    append_if_not_None(qs, question1.askHowMany(line, ner_tags))
    '''
    append_if_not_None(qs, question1.askWhen(line, raw_tree, ner_tree))
    append_if_not_None(qs, question1.askWho(line, raw_tree, ner_tree))
    append_if_not_None(qs, question1.askWhere(line, raw_tree, ner_tree))
    append_if_not_None(qs, question1.askWhere(tree))
    append_if_not_None(qs, question1.askDoWhat(tree))
    '''
    return qs

if __name__ == '__main__':
    _, input_file, N = sys.argv
    N = int(N)
    total = []
    with open(input_file) as inp:
        data = list(inp)
        shuffle(data)
        for line in data:
            sentences = nltk.sent_tokenize(line)
            for sent in sentences:
                if "–" in sent or ":" in sent or "-" in sent or "(" in sent or ")" in sent:
                    continue
                if sent and sent[-1] == '.':
                    qs = ask(sent)
                    total += qs
                    if qs:
                        N -= 1
                        if N == 0:
                            break
            if N == 0: 
                break
    for q in total:
        print(q)
