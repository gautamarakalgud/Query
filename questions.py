import ner
from nltk.parse.stanford import StanfordParser
from nltk.tokenize import sent_tokenize
from nltk.stem import WordNetLemmatizer
import itertools

class Questions:
	""" Class to generate questions """
	def __init__(self, text, parse_tree=[], num_questions=10):
		self.num_questions = num_questions
		lines = text.split('\n')
		self.sent_list = []
		for line in lines:
			self.sent_list.extend(sent_tokenize(line))
		self.question_list = []
		self.ner_entities = []
		self.parse_tree = parse_tree
		self.wordnet_lemmatizer = WordNetLemmatizer()

	def get_ner_entities(self):
		tagger = ner.SocketNER(host='localhost', port=2020, output_format='slashTags')
		for sent in self.sent_list:
			self.ner_entities.append(tagger.get_entities(sent))
		print('NER entities done!')

	def get_parse_tree(self):
		parser=StanfordParser(model_path="edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz")
		self.parse_tree = parser.raw_parse_sents(self.sent_list)
		self.parse_tree = [list(tree)[0] for tree in self.parse_tree]
		# print(self.parse_tree)
		print('Parse tree done!')

	def date_time_simple(self):
		for sent_entities in self.ner_entities:
			if 'DATE' in self.ner_entities and len(sent_entities['DATE'])==1:
				if 'TIME' in self.ner_entities and len(sent_entities['TIME']==1):
						self.question_list.append('What happened at '+sent_entities['TIME'][0]+' on '+sent_entities['DATE'][0]+' with respect to '+sent_list[0]+'?')
				else:
						if len(sent_entities['DATE'].split()) == 4:
							self.question_list.append('What happened on '+sent_entities['DATE']+' with respect to '+sent_list[0]+'?')

	def where_simple(self):
		for index, sent_entities in enumerate(self.ner_entities):
			tree = self.parse_tree[index]
			leaf_values = tree.leaves()
			pos_tags = tree.pos()
			subtrees = tree.subtrees(filter=lambda x:x.label()=='PP')
			if 'LOCATION' in sent_entities:
				for location in sent_entities['LOCATION']:
					
					leaf_index = leaf_values.index(location.split()[0])
					
					for subtree in subtrees:
						leaves = subtree.leaves()
						if location in leaves:
							first_leaf = leaves[0]
							try:
								formed = False
								found = 0
								ind = self.sent_list[index].index(' '+first_leaf+' ')
								quest = self.sent_list[index][:ind]
								# print(self.sent_list[0])
								for tag in pos_tags[:leaf_index]:
									if tag[1] == 'VBD' or tag[1] == 'VBZ' or tag[1] == 'VBP' or tag[1] == 'VBN':
										if not formed:
											lemmatized_tag = self.wordnet_lemmatizer.lemmatize(tag[0], pos='v')
										if lemmatized_tag == 'be':
											quest = quest.replace(tag[0], '')
											formed = True
										else:
											quest = quest.replace(tag[0], lemmatized_tag)
									elif tag[1]=='PRP$' and found==0:
										found=1
										quest = quest.replace(tag[0], self.sent_list[0]+"'s")
									elif tag[1]=='PRP' and found==0:
										found=1
										quest = quest.replace(tag[0], self.sent_list[0])
								if len(quest.split()) <6 or len(quest.split()) > 15:
									continue
								if formed:
									self.question_list.append('Where was '+quest+'?')
								else:
									self.question_list.append('Where did '+quest+'?')
							except:
								pass

	def when_simple(self):
		for index, sent_entities in enumerate(self.ner_entities):
			tree = self.parse_tree[index]
			leaf_values = tree.leaves()
			pos_tags = tree.pos()
			subtrees = tree.subtrees(filter=lambda x:x.label()=='PP')
			if 'DATE' in sent_entities:
				for date in sent_entities['DATE']:
					leaf_index = leaf_values.index(date.split()[0])
					for subtree in subtrees:
						leaves = subtree.leaves()
					
						if (date.split()[0]) in leaves:
							first_leaf = leaves[0]
							formed = False
							found = 0
							ind = self.sent_list[index].index(' '+first_leaf+' ')
							quest = self.sent_list[index][:ind]
							print(quest)
							for tag in pos_tags[:leaf_index]:
								if tag[1] == 'VBD' or tag[1] == 'VBZ' or tag[1] == 'VBP' or tag[1] == 'VBN' and tag[0] != 'is' and tag[0] != 'Is' and tag[0] != 'was' and tag[0] != 'Was':
									if not formed:
										lemmatized_tag = self.wordnet_lemmatizer.lemmatize(tag[0], pos='v')
									quest = quest.replace(tag[0], lemmatized_tag)
								elif tag[1]=='PRP$' and found==0:
									found=1
									quest = quest.replace(tag[0], self.sent_list[0]+"'s")
								elif tag[1]=='PRP' and found==0:
									found=1
									quest = quest.replace(tag[0], self.sent_list[0])
							if len(quest.split()) <3 or len(quest.split()) > 15:
								continue
							if formed:
								self.question_list.append('When was '+quest+'?')
							else:
								self.question_list.append('When did '+quest+'?')

	def is_questions(self):
		for index,sent in enumerate(self.sent_list):
			tree = self.parse_tree[index]
			subtrees = list(tree.subtrees(filter=lambda x:x.label()=='S'))
			found=0

			if 'is' in sent.split():
				for subtree in reversed(subtrees):
					if 'is' in subtree.leaves():
						leaf_values = subtree.leaves()
						del leaf_values[leaf_values.index('is')]
						for tag in subtree.pos():
							if tag[1] == 'PRP$' and found==0:
								found = 1
								leaf_values[leaf_values.index(tag[0])] = self.sent_list[0]+"'s"
							if tag[1] == 'PRP' and found==0:
								found=1
								leaf_values[leaf_values.index(tag[0])] = self.sent_list[0]
						quest = ' '.join(leaf_values)
						if len(quest.split()) < 3 or len(quest.split()) > 13:
							continue
						self.question_list.append('Is '+quest+'?')
						break

	def filler_questions(self):
		entities = ['PERSON', 'ORGANISATION', 'LOCATION']
		relationships = list(itertools.combinations(entities, 2))+[('PERSON', 'PERSON'), ('ORGANISATION', 'ORGANISATION')]
		for index,sent_entities in enumerate(self.ner_entities):
			for rel in relationships:
				if rel[0] in sent_entities and rel[1] in sent_entities:
					if rel[0]==rel[1]:
						try:
							self.question_list.append('How are '+sent_entities[rel[0]][0]+' and '+sent_entities[rel[1]][1]+' related?')
						except:
							pass
					else:
						self.question_list.append('How are '+sent_entities[rel[0]][0]+' and '+sent_entities[rel[1]][0]+' related?')

