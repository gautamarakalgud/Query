#!/usr/bin/python3
from questions import Questions
from nltk.tree import Tree
from nltk.tree import ParentedTree

text = open('data/set1/a1.txt').read()
f = open('data/set1/a1_parse_tree.txt')
parse_tree = []
for line in f:
	parse_tree.append(ParentedTree.fromstring(line.rstrip('\n')))
Q = Questions(text, parse_tree=parse_tree, num_questions=20)
Q.get_ner_entities()
# Q.get_parse_tree()
# Q.date_time_simple()
Q.where_simple()
Q.when_simple()
Q.is_questions()
Q.filler_questions()
Q.evaluate()
question_list = Q.generate_final_questions()
question_list = Q.make_neat(question_list)
question_list = Q.similar(question_list)
for quest in question_list:
	print(quest)