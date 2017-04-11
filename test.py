from questions import *

text = 'Clint Dempsey\nHis performances throughout 2009–10 earned him the designation of GoalScorer in London.'
q = Questions(text)
q.get_ner_entities()
q.get_parse_tree()
q.when_where_simple()
# print(q.ner_entities)
# print(q.parse_tree)
for quest in q.question_list:
	print(quest)
# print(q.question_list)