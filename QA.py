import nltk

def tokenizeDoc(cur_doc):
    return re.findall('\\w+', cur_doc)

text = input()

sent_text = nltk.sent_tokenize(text)
for sentence in sent_text:
    tokenized_text = nltk.word_tokenize(sentence)
    tagged = nltk.pos_tag(tokenized_text)
    print(tagged)



