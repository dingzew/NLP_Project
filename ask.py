from ask_pipeline import ask
import sys
print = 'h'

if __name__ == '__main__':
    _, input_file, output_file = sys.argv
    with open(input_file) as inp:
        for sentence in inp:
            sent = sentence.strip()
            if sent:
                ask(sent, output_file)
