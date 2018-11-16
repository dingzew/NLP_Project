from ask_pipeline import ask
import sys
import nltk
if __name__ == '__main__':
    _, input_file, N = sys.argv
    N = int(N)
    with open(input_file) as inp:
        for line in inp:
            sentences = nltk.sent_tokenize(line)
            for sent in sentences:
                if sent and sent[-1] == '.':
                    N = ask(sent, N)
                if N == 0:
                    break
            if N == 0: 
                break