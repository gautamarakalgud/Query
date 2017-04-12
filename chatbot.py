#!/usr/bin/python3
from questions import Questions
from nltk.tree import Tree
from nltk.tree import ParentedTree

text = open('data/set1/a1.txt').read()
f = open('data/set1/a1_parse_tree.txt')
parse_tree = []
for line in f:
	parse_tree.append(ParentedTree.fromstring(line.rstrip('\n')))
Q = Questions(text, parse_tree)
Q.get_ner_entities()
# Q.date_time_simple()
# Q.when_where_simple()
# Q.is_questions()
Q.filler_questions()
for quest in Q.question_list:
	print(quest)