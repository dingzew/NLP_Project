import tree_file
import NER_file

def askWho(sentence):
    if (NER_file.contains_person(sentence)):
        tree = tree_file.generateTree(sentence)
        vp = tree_file.get_phrases(tree, "VP")
        if not vp: return ''
        question = "Who " + tree_file.merge(vp[0])[0] + "?"
        return question
    else:
        return askWhoHelper(sentence)


def askWhoHelper(sentence):
    # try:
        tree = tree_file.generateTree(sentence)
        vp = tree_file.get_phrases(tree, "VP")
        if not vp: return ''
        question = "What " + tree_file.merge(vp[0])[0] + "?"
        return question
    # except Exception as e:
    #     return None


def askWhen(sentence):
    if (NER_file.contains_person(sentence)):
        tree = tree_file.generateTree(sentence)
        dic = tree_file.main_sentence_structure(tree)
        vp = tree_file.get_phrases(tree, "VP")
        if not vp: return ''
        if ("main" not in dic):
            return None
        question = "When did " + dic["main"] + " " + tree_file.merge(vp[0])[0] + "?"
        return question
    else:
        return None


def askDoWhat(sentence):
    tree = tree_file.generateTree(sentence)
    dic = tree_file.main_sentence_structure(tree)
    time = tree_file.testTime(tree)
    if "main" not in dic:
        return None
    if time == "past":
        question = "What did " + dic["main"] + " do" + "?"
        return question
    elif time == "single":
        question = "What does " + dic["main"] + " do" + "?"
        return question
    else:
        question = "What do " + dic["main"] + " do" + "?"
        return question

def askWhere(sentence):
    if (NER_file.contains_loc(sentence)):
        tree = tree_file.generateTree(sentence)
        dic = tree_file.fine_structures(tree)
        if  "V" not in dic or "main" not in dic:
            return None
        time = tree_file.testTime(tree)
        if time == "past":
            question = "When did " + dic["main"] + " " + dic["V"] + "?"
            return question
        elif time == "single":
            question = "What does " + dic["main"] + " " +dic["V"] + "?"
            return question
        else:
            question = "What do " + dic["main"] +  " " + dic["V"] + "?"
            return question
    else:
        return None




if __name__ == "__main__":
    print(askWho("I ate an apple in Carnegie Mellon University"))
    print(askWhen("I ate an apple in Carnegie Mellon University"))
    print(askWho("China is the most powerful place in the world"))
    print(askWhere("I ate an apple in Carnegie Mellon University"))
