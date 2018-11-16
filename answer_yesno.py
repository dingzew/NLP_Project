import nltk
from nltk.tree import Tree
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem.porter import *
import string
import os
import re
import sys
import math
from textblob import TextBlob
from stanford_utils import *
from stanfordcorenlp import StanfordCoreNLP

stemmer = PorterStemmer()
parser = new_parser()
yesno_list = ['be','have','do','will','can','would','could','']
tree = (parser.parse(["Is it true that it angered many residents of the thirteen colonies?"]))
print(tree.children())
#print(WordNetLemmatizer().lemmatize("would",'v'))

def getAnswer(question, target):
	question_list = question.split()
	if (len(question_list) == 0):
		return question
	feature = WordNetLemmatizer().lemmatize(question_list[0],'v')
	if (feature.lower() not in yesno_list):
		return question
	# output yes/no instance
	parsed_ques = parser.parse([question])
	parsed_ans = parser.parse([target])


