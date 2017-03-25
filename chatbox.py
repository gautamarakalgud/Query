import os
import nltk
import re
import string
from nltk.tag.stanford import StanfordTagger
from nltk.internals import find_jars_within_path
# from nltk.parse.stanford import StanfordNeuralDependencyParser
# parser = StanfordNeuralDependencyParser(model_path="edu/stanford/nlp/models/parser/nndep/english_UD.gz")

# nltk.download()
# from nltk.tokenize import RegexpTokenizer

path = 'data/set1'
for filenames in os.listdir(path):
	if(filenames[-1] == 't'):
		filenames = 'data/set1/' + filenames
		# print(filenames)
		f = open(filenames,"r")
		mystring = f.read()
		# print(mystring)
		mystring = mystring.replace('\n','').replace('\r','')
		mystring = mystring.rstrip('\r\n')
		mystring = re.sub('['+string.punctuation+']', '', mystring)
		# print(mystring)
		# tokenizer = RegexpTokenizer(r'\w+')
		# tokened = tokenizer.tokenize("don't")
		# print(tokened)
		tokens = nltk.word_tokenize(mystring)
		tagged = nltk.pos_tag(tokens)

		entities = nltk.chunk.ne_chunk(tagged)

		f.close()



