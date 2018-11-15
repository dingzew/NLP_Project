from stanford_utils import *
from nltk.tokenize import word_tokenize

NER_PARSER = new_NERtagger()

def get_continuous_chunks(tagged_sent):
    continuous_chunk = []
    current_chunk = []

    for token, tag in tagged_sent:
        if tag != "O":
            current_chunk.append((token, tag))
        else:
            if current_chunk: # if the current chunk is not empty
                continuous_chunk.append(current_chunk)
                current_chunk = []
    # Flush the final current_chunk into the continuous_chunk, if any.
    if current_chunk:
        continuous_chunk.append(current_chunk)
    return continuous_chunk


def detect_NER_Phrase(phrase):
    tagged_sent = NER_PARSER.tag(phrase.split())
    named_entities = get_continuous_chunks(tagged_sent)
    named_entities_str_tag = [(" ".join([token for token, tag in ne]), ne[0][1]) for ne in named_entities]

    return named_entities_str_tag


def detect_NER_word(sentence):
    tokenized_text = word_tokenize(sentence)
    classified_text = NER_PARSER.tag(tokenized_text)
    return classified_text



def contains_person(sentence):
    list = detect_NER_word(sentence)
    people = set()
    peoplelist = ["he", "she", "it", "they", "we", "i"]

    list = detect_NER_Phrase(sentence)
    for t in list:
        if (t[1] == "PERSON"):
            return True


    for person in peoplelist:
        people.add(person)
    for t in list:
        if (t[1] == "PERSON"):
            return True

    for t in sentence.split(" "):
        if t.lower() in people:
            return True

    return False



def contains_loc(sentence):
    list = detect_NER_word(sentence)
    for t in list:
        if (t[1] == "ORGANIZATION"):
            return True
        if (t[1] == "LOCATION"):
            return True
    list = detect_NER_Phrase(sentence)
    for t in list:
        if (t[1] == "ORGANIZATION"):
            return True
        if (t[1] == "LOCATION"):
            return True
    return False




if __name__ == "__main__":
    # print(detect_NER_Phrase("Carnegie Mellon University"))
    # print(detect_NER_Phrase('While in France, Christine Lagarde discussed short-term stimulus efforts in a recent interview with the Wall Street Journal.'))
    # print(detect_NER_word("Carnegie Mellon University"))
    # print(detect_NER_word('While in France, Christine Lagarde discussed short-term stimulus efforts in a recent interview with the Wall Street Journal.'))
    print(contains_person("Dingze Wang ate an apple in Carnegie Mellon University"))
    print(contains_person("While in France, Christine Lagarde discussed short-term stimulus efforts in a recent interview with the Wall Street Journal."))
    print(contains_person("I ate an apple yesterday"))
    # print(contains_person("While in France, Christine Lagarde discussed short-term stimulus efforts in a recent interview with the Wall Street Journal."))
