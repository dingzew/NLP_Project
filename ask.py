from ask_pipeline import ask
import sys
import nltk
if __name__ == '__main__':
    _, input_file, output_file = sys.argv
    with open(input_file) as inp:
        for line in inp:
            sentences = nltk.sent_tokenize(line)
            for sent in sentences:
                if not sent or sent[-1] == '.':

                    ask(sent, output_file)
