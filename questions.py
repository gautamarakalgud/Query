import ner
from nltk.parse.stanford import StanfordParser
from nltk.tokenize import sent_tokenize
from nltk.stem import WordNetLemmatizer
import itertools
import language_check
import math
from nltk.tree import Tree
from nltk.corpus import wordnet
from nltk import pos_tag
import numpy.random as npr
from random import shuffle

class Questions:
	""" Class to generate questions """
	def __init__(self, text, parse_tree=[], num_questions=10):
		self.num_questions = num_questions
		lines = text.split('\n')
		self.sent_list = []
		for line in lines:
			self.sent_list.extend(sent_tokenize(line))
		self.sent_list = [sent for sent in self.sent_list if len(sent.split())<50]
		self.question_list = {}
		self.ner_entities = []
		self.parse_tree = parse_tree
		self.wordnet_lemmatizer = WordNetLemmatizer()

	def get_ner_entities(self):
		tagger = ner.SocketNER(host='localhost', port=2020, output_format='slashTags')
		for sent in self.sent_list:
			try:
				self.ner_entities.append(tagger.get_entities(sent))
			except:
				d = {}
				self.ner_entities.append(d)

	def get_parse_tree(self):
		parser=StanfordParser(model_path="edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz")
		for ind, sent in enumerate(self.sent_list):
			try:
				self.parse_tree.append(list(parser.raw_parse(sent))[0])
			except:
				self.parse_tree.append(Tree('S', []))
				self.ner_entities[ind] = {}

	def date_time_simple(self):
		self.question_list['DATE_TIME'] = []
		for sent_entities in self.ner_entities:
			if 'DATE' in self.ner_entities and len(sent_entities['DATE'])==1:
				if 'TIME' in self.ner_entities and len(sent_entities['TIME']==1):
						self.question_list['DATE_TIME'].append('What happened at '+sent_entities['TIME'][0]+' on '+sent_entities['DATE'][0]+' with respect to '+sent_list[0]+'?')
				else:
						if len(sent_entities['DATE'].split()) == 4:
							self.question_list['DATE_TIME'].append('What happened on '+sent_entities['DATE']+' with respect to '+sent_list[0]+'?')

	def where_simple(self):
		self.question_list['WHERE'] = []
		for index, sent_entities in enumerate(self.ner_entities):
			question = ''
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
									elif tag[1]=='PRP$' and found==0 and self.sent_list[0].split()[-1] not in quest:
										found=1
										quest = quest.replace(tag[0], self.sent_list[0]+"'s")
									elif tag[1]=='PRP' and found==0 and self.sent_list[0].split()[-1] not in quest:
										found=1
										quest = quest.replace(tag[0], self.sent_list[0])
								if len(quest.split()) <6 or len(quest.split()) > 15:
									continue
								else:
									question = quest
							except:
								pass
			if question:
				if formed:
					self.question_list['WHERE'].append('Where was '+quest+'?')
				else:
					self.question_list['WHERE'].append('Where did '+quest+'?')

	def when_simple(self):
		self.question_list['WHEN'] = []
		for index, sent_entities in enumerate(self.ner_entities):
			question = ''
			tree = self.parse_tree[index]
			leaf_values = tree.leaves()
			pos_tags = tree.pos()
			subtrees = tree.subtrees(filter=lambda x:x.label()=='PP')
			if 'DATE' in sent_entities:
				for date in sent_entities['DATE']:
					
					leaf_index = leaf_values.index(date.split()[0])
					
					for subtree in subtrees:
						leaves = subtree.leaves()
						if date.split()[0] in leaves:
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
									elif tag[1]=='PRP$' and found==0 and self.sent_list[0].split()[-1] not in quest:
										found=1
										quest = quest.replace(tag[0], self.sent_list[0]+"'s")
									elif tag[1]=='PRP' and found==0 and self.sent_list[0].split()[-1] not in quest:
										found=1
										quest = quest.replace(tag[0], self.sent_list[0])
								if len(quest.split()) <6 or len(quest.split()) > 15:
									continue
								else:
									question = quest
							except:
								pass
			if question:
				if formed:
					self.question_list['WHEN'].append('When was '+quest+'?')
				else:
					self.question_list['WHEN'].append('When did '+quest+'?')

		# for question in self.question_list['WHEN']:
		# 	print(question)

	def is_questions(self):
		self.question_list['IS'] = []

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
						self.question_list['IS'].append('Is '+quest+'?')
						break

			elif 'was' in sent.split():
				for subtree in reversed(subtrees):
					if 'was' in subtree.leaves():
						leaf_values = subtree.leaves()
						del leaf_values[leaf_values.index('was')]
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
						self.question_list['IS'].append('Was '+quest+'?')
						break


	def filler_questions(self):
		self.question_list['MISC'] = []
		entities = ['PERSON ORGANIZATION', 'ORGANIZATION ORGANIZATION', 'PERSON PERSON','ORGANIZATION LOCATION']
		entities_q={}
		for e in entities:
			entities_q[e]=[]
		relationships = entities

		for index,sent_entities in enumerate(self.ner_entities):
			for relu in relationships:
				rel=relu.split()
				if rel[0] in sent_entities and rel[1] in sent_entities:
					if rel[0]==rel[1]:
						try:
							# string=rel[0]+' '+rel[1]
							entities_q[relu].append('How are '+sent_entities[rel[0]][0]+' and '+sent_entities[rel[1]][1]+' related?')
						except:
							pass
					else:
						# try:
							# string=rel[0]+' '+rel[1]
						entities_q[relu].append('How are '+sent_entities[rel[0]][0]+' and '+sent_entities[rel[1]][0]+' related?')
						# except:
							# pass
		self.question_list['MISC'].extend(entities_q['PERSON ORGANIZATION'])
		self.question_list['MISC'].extend(entities_q['ORGANIZATION ORGANIZATION'])
		self.question_list['MISC'].extend(entities_q['PERSON PERSON'])
		self.question_list['MISC'].extend(entities_q['ORGANIZATION LOCATION'])
		self.question_list['MISC'] = list(set(self.question_list['MISC']))


	def evaluate(self):
		tool = language_check.LanguageTool('en-US')
		for question_type in self.question_list:
			scores = [len(tool.check(quest)) for quest in self.question_list[question_type]]
			# print(sorted(scores))
			self.question_list[question_type] = [x for (y,x) in sorted(zip(scores,self.question_list[question_type]))]

	def generate_final_questions(self):
		final_questions = []
		question_types = list(self.question_list.keys())
		counts = [0]*len(question_types);

		num_total_questions = sum(len(self.question_list[tag]) for tag in self.question_list)

		while sum(counts) < num_total_questions:
			for ind, typ in enumerate(question_types):
				if counts[ind] < len(self.question_list[typ]):
					final_questions.append(self.question_list[typ][counts[ind]])
					counts[ind] += 1

		if num_total_questions < self.num_questions:
			print('We cannot generate that many questions. These are all the ones we have -')
			return final_questions
		else:
			return final_questions[:self.num_questions]
			# num_good_questions = sum(len(self.question_list[tag]) for tag in self.question_list if tag != 'MISC')
			# num = math.ceil(float(self.num_questions)/len(self.question_list))
			# for question_type in self.question_list:
			# 	final_questions.extend(self.question_list[question_type][:num])
			# return final_questions[:self.num_questions]


	def make_neat(self, q_list):
		tagger = ner.SocketNER(host='localhost', port=2020, output_format='slashTags')
		for index,q in enumerate(q_list):
			t=tagger.get_entities(q)
			q=q.lower()
			q=q.replace(' .', '')
			q=q[0].upper()+q[1:]
			for tag in t:
				if tag != 'O' or tag != 'o':
					for l in t[tag]:
						if l.lower() in q:
							q=q.replace(l.lower(),l)
			q_list[index]=q;
		return q_list

	def similar(self, q_list):
		shuffle(q_list)
		max_confuse = int(len(q_list)/4)
		noun=['NN','NNP','NNS','NP']
		verb=['VP','VBZ','VBD','VBP','VB']
		count=0
		for index,q in enumerate(q_list):
			success=0
			if q[0:3]=='How':
				continue
			if(count>=max_confuse):
				break
			tag=pos_tag(q.split())
			shuffle(tag);
			for t in tag:
				word=t[0]
				part_of_speech=None
				# if(t[1] in noun):
				# 	part_of_speech='n'
				if(t[1] in verb):
					part_of_speech='v'
				if(part_of_speech!=None):
					sim = []
					synsets = wordnet.synsets(word, pos=part_of_speech)
					if len(synsets) > 0:
						for hypernym in synsets[0].hypernyms():
							for sister in hypernym.hyponyms():
								for lemma in sister.lemmas():
									sim.append(lemma.name().replace('_', ' '))
					if(len(sim)>0):
						success=1
						ch=npr.choice(sim)
						q_list[index]=q.replace(word,ch,1)

			if(success==1):
				count+=1
		return q_list