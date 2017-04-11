#!/usr/bin/python3
from questions import Questions

text = open('data/set1/a1.txt').read()
Q = Questions(text)
Q.get_ner_entities()
Q.get_parse_tree()
Q.date_time_simple()
Q.when_where_simple()
for quest in Q.question_list:
	print(quest)