from stanford_utils import *
import NER_file
from nltk import Tree
from nltk import pos_tag
from nltk.chunk import conlltags2tree
from nltk.stem.wordnet import WordNetLemmatizer

""" 
The section of code below is copied from alvas' answer at https://stackoverflow.com/questions/30664677/extract-list-of-persons-and-organizations-using-stanford-ner-tagger-in-nltk 
"""
def stanfordNE2BIO(tagged_sent):
    bio_tagged_sent = []
    prev_tag = "O"
    for token, tag in tagged_sent:
        if tag == "O": #O
            bio_tagged_sent.append((token, tag))
            prev_tag = tag
            continue
        if tag != "O" and prev_tag == "O": # Begin NE
            bio_tagged_sent.append((token, "B-"+tag))
            prev_tag = tag
        elif prev_tag != "O" and prev_tag == tag: # Inside NE
            bio_tagged_sent.append((token, "I-"+tag))
            prev_tag = tag
        elif prev_tag != "O" and prev_tag != tag: # Adjacent NE
            bio_tagged_sent.append((token, "B-"+tag))
            prev_tag = tag
    return bio_tagged_sent

def stanfordNE2tree(ne_tagged_sent):
    bio_tagged_sent = stanfordNE2BIO(ne_tagged_sent)
    sent_tokens, sent_ne_tags = zip(*bio_tagged_sent)
    sent_pos_tags = [pos for token, pos in pos_tag(sent_tokens)]

    sent_conlltags = [(token, pos, ne) for token, pos, ne in zip(sent_tokens, sent_pos_tags, sent_ne_tags)]
    ne_tree = conlltags2tree(sent_conlltags)
    return ne_tree
""" 
The section of code above is copied from alvas' answer at https://stackoverflow.com/questions/30664677/extract-list-of-persons-and-organizations-using-stanford-ner-tagger-in-nltk 
"""

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


def merge_raw_tree(tree):
    return " ".join(tree.leaves())

def merge_ner_tree(tree):
    return " ".join(l[0] for l in tree.leaves())

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

def get_tokens(sentence):
    tokenized_text = nltk.word_tokenize(sentence)
    tagged = nltk.pos_tag(tokenized_text)
    return tagged

def testTime(tree):
    if len(get_phrases(tree, "VBD")) != 0:
        return "past"
    if len(get_phrases(tree, "VBP")) != 0:
        return "single"
    if len(get_phrases(tree, "VBZ")) != 0:
        return "single"
    return "now"

def testPlural(np):
    for word_pos in np.pos():
        if word_pos[1].startswith('N'):
            if word_pos[1].endswith('S'):
                return True
    return False

def main_sentence_structure(tree):
    dic = {}
    phrases = get_phrases(tree, "NP")
    if not phrases: return dic
    dic["main"] = merge_raw_tree(phrases[0])
    phrases = get_phrases(tree, "VP")
    if not phrases: return dic
    dic["what"] = merge_raw_tree(phrases[0])
    return dic

def is_be(word):
    return word.lower() in {"be", "am", "is", "are", "was", "were"}

def is_have(word):
    return word.lower() in {"have", "has", "had"}

def is_pron(word):
    return word.lower() in {"he", "she", "it", "I", "him", "her", "his", "its", "my", "your", "yours", "mine", "hers"}

def is_subj_pron(word):
    return word.lower() in {"he", "she", "it", "I"}

def get_first_verb(tree):
    first_verb = None
    for word_pos in tree.pos():
        if word_pos[1].startswith("V"):
            first_verb = word_pos[0]
            break
    return first_verb

def find_subject_action(raw_tree, ner_tree):
    subj, action = None, None
    for i in raw_tree.subtrees():
        j = i.right_sibling()
        while j is not None and j.label()[0] == "A":
            j = j.right_sibling()
        if not j:
            continue
        if (i.label().startswith("N") or i.label() == "PRP") and j.label().startswith("V"):
            subj = i.leaves()[0]
            action = j
            break

    if not subj or not action: return (None, None)

    for ner in ner_tree:
        if type(ner) == Tree:
            for leaf in ner.leaves():
                if leaf[0] == subj:
                    return ner, action
        elif is_subj_pron(ner[0]) and subj == ner[0]:
            return ner, action
    return (None, None)

def get_qbody(tree):
    vp = get_phrases(tree, "VP")
    if vp: vp = vp[0]
    else: return None

    np = get_phrases(tree, "NP")
    if np: np = np[0]
    else: return None

    if is_pron(np.leaves()[0]): return None

    tense = testTime(vp)
    if not vp: return ''

    first_verb = get_first_verb(vp)
    qbody = merge_raw_tree(np) + " " + vp2base(vp)
    if tense == "past":
        if is_be(first_verb):
            if testPlural(np):
                qbody = "were " + qbody
            else:
                qbody = "was " + qbody
        elif is_have(first_verb):
            return None
        else:
            qbody = "did " + qbody
    else:
        qbody = "will " + qbody
    return qbody

def vp2base(vp):
    words_poses = vp.pos()

    words = []
    first_verb_encountered = False
    ask_be = False
    pre_word_pos = ("", "")
    for word_pos in words_poses:
        if not first_verb_encountered and word_pos[1].startswith('V'):
            first_verb_encountered = True
            if is_be(word_pos[0]):
                ask_be = True
                continue
            words.append(WordNetLemmatizer().lemmatize(word_pos[0], 'v'))
        elif word_pos[1].startswith("V") and not is_be(pre_word_pos[0]):
            if ask_be or is_be(word_pos[0]) or word_pos[1] == "VBG":
                words.append(word_pos[0])
            else:
                words.append(WordNetLemmatizer().lemmatize(word_pos[0], 'v'))
        else:
            words.append(word_pos[0])
        pre_word_pos = word_pos
    return " ".join(words)

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

