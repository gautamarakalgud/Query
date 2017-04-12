from questions import Questions
from nltk.parse.stanford import StanfordParser
from nltk.tree import ParentedTree
from nltk.tokenize import sent_tokenize

text = 'Clint Dempsey\nIn his spare time he is a fisherman.'
lines = text.split('\n')
sent_list = []
for line in lines:
	sent_list.extend(sent_tokenize(line))
parser=StanfordParser(model_path="edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz")

parse_tree = list(parser.raw_parse_sents(sent_list))
# f = open('data/set1/a1_parse_tree.txt')
# parse_tree = []
# for line in f:
# 	parse_tree.append(ParentedTree.fromstring(line.rstrip('\n')))
q = Questions(text, parse_tree)

q.get_ner_entities()
# q.get_parse_tree()
# q.when_where_simple()
# q.when_simple()
# print(q.ner_entities)
# print(q.get_parse_tree())
q.is_questions()
for quest in q.question_list:
	print(quest)
# print(q.question_list)