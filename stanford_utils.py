import os
import logging
from nltk.parse.stanford import StanfordParser
from nltk.tag.stanford import StanfordNERTagger

from stanfordcorenlp import StanfordCoreNLP

dir = os.getcwd()
parser_path = dir + '/stanford-parser-full/'
ner_path = dir + '/stanford-ner'
nlp_path = dir + '/stanford-core-nlp-full/'
which_java = '/usr/bin/java'
#which_java = "C:/Program Files/Java/jdk1.8.0_161/bin/java.exe"


def new_parser():
    os.environ['JAVAHOME'] =  which_java
    os.environ['CLASSPATH'] = parser_path
    os.environ['STANFORD_MODELS'] = parser_path
    return StanfordParser()

def new_NERtagger():
    os.environ['JAVAHOME'] =  which_java
    return StanfordNERTagger(ner_path+'/classifiers/english.muc.7class.distsim.crf.ser.gz', ner_path+ '/stanford-ner.jar')

if __name__ == "__main__":
    print(parser_path)
    print(ner_path)
    new_parser()
    new_NERtagger()
