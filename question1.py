import nltk
import tree_file
import NER_file

def postprocess(text):
    return text.replace(" , ", ", ").replace(" '", "'").replace(" ?", "?")


def askWho(sent, raw_tree, ner_tree):
    def is_person(subject):
        if type(subject) == nltk.Tree:
            return subject.label() == "PERSON"
        return subject[1] == "PRP" and subject[0].lower() != "it"

    subject, action = tree_file.find_subject_action(raw_tree, ner_tree)
    if subject == None or not action: return None

    if is_person(subject):
        question = "Who " + tree_file.merge_raw_tree(action) + "?"
        return postprocess(question)

def askWhoHelper(vp):
    # try:
    question = "What " + tree_file.merge_raw_tree(action) + "?"
    return postprocess(question)
    # except Exception as e:
    #     return None

def askHowMany(sentence, ner_tags):
    print(sentence)
    print(ner_tags)
    res = NER_file.contains_num(sentence)
    if res != None:
        tree = tree_file.generateTree(sentence)
        print(tree)
        pp = tree_file.get_phrases(tree, "PP")
        if len(pp) >= 1:
            if (res[1] == "NNS"):
                question = "How many " + res[0] + " " + "are " + tree_file.merge_raw_tree(pp[0]) + "?"
            else:
                question = "How many " + res[0] + "s " + "are " + tree_file.merge_raw_tree(pp[0]) + "?"
            return question
        else:
            return None
    else:
        return None

def askWhen(sent, raw_tree, ner_tree):
    dates = []
    for st in ner_tree:
        if type(st) != nltk.Tree:
            continue

        if st.label() == "DATE":
            #find all dates from the ner_tree
            dates.append(tree_file.merge_ner_tree(st))
    if not dates:
        return None

    pps = tree_file.get_phrases(raw_tree, "PP")

    for pp in pps:
        # remove all dates in the original sentence
        merged_pp = tree_file.merge_raw_tree(pp)
        has_date = False
        for d in dates:
            if d in merged_pp:
                has_date = True
                break
        if has_date: 
            sent = sent.replace(merged_pp, "").strip(",;. ")

    # reconstruct the tree after removing all dates
    raw_tree = tree_file.generateTree(sent)
    qbody = tree_file.get_qbody(raw_tree)
    if not qbody:
        return None
    return postprocess("When " + tree_file.get_qbody(raw_tree) + "?")

def askDoWhat(tree):
    dic = tree_file.main_sentence_structure(tree)
    time = tree_file.testTime(tree)
    if "main" not in dic:
        return None
    if time == "past":
        question = "What did " + dic["main"] + " do" + "?"
    elif time == "single":
        question = "What does " + dic["main"] + " do" + "?"
    else:
        question = "What do " + dic["main"] + " do" + "?"
    return postprocess(question)

def askWhere(sent, raw_tree, ner_tree):
    print(sent)
    print(ner_tree)
    locations = []
    dates = []
    for st in ner_tree:
        if type(st) != nltk.Tree: continue
        if st.label() == "LOCATION":
            locations.append(tree_file.merge_ner_tree(st))
        if st.label() == "DATE":
            dates.append(tree_file.merge_ner_tree(st))

    if not locations:
        return None
    pps = tree_file.get_phrases(raw_tree, "PP")
    prep = None
    for pp in pps:
        merged_pp = tree_file.merge_raw_tree(pp)
        has_location = False
        for l in locations:
            if l in merged_pp:
                has_location = True
                prep = pp.leaves()[0]
                if prep.lower() not in ("in", "at", "on", "from"):
                    return None
                break
        if has_location:
            sent = sent.replace(merged_pp, "").strip(",;. ")
    if prep is None:
        return None
    for pp in pps:
        merged_pp = tree_file.merge_raw_tree(pp)
        for d in dates:
            if d in merged_pp:
                sent = sent.replace(merged_pp, "").strip(",;. ")

    raw_tree = tree_file.generateTree(sent)
    qbody = tree_file.get_qbody(raw_tree)
    if not qbody:
        return None
    if prep.lower() != "from":
        prep = ""
    return postprocess("Where " + tree_file.get_qbody(raw_tree) + " " + prep + "?")

if __name__ == "__main__":
    print(askWho("I ate an apple in Carnegie Mellon University"))
    print(askWhen("I ate an apple in Carnegie Mellon University"))
    print(askWho("China is the most powerful place in the world"))
    print(askWhere("I ate an apple in Carnegie Mellon University"))
