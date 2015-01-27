
from hazm import DadeganReader
from baaz import ChunkTreeInformationExtractor, DependencyTreeInformationExtractor
from hazm import Chunker, Normalizer, SequencePOSTagger, IOBTagger, DependencyParser, Lemmatizer
import codecs, re
from nltk import accuracy
from nltk.tree import Tree


#output = open('200DadeganSents-chunkExtractor.txt', 'w', encoding='utf8')
dadegan = DadeganReader('resources/Dadegan/test.conll')
tagger = SequencePOSTagger(model='Resources/postagger-remove-w3-all.model')
lemmatizer = Lemmatizer()
chunker = Chunker(model='Resources/chunker-dadeganFull.model')
parser = DependencyParser(tagger, lemmatizer=lemmatizer )
normalizer = Normalizer()
chunk_extractor = ChunkTreeInformationExtractor()
dep_extractor = DependencyTreeInformationExtractor()
trees = list(dadegan.chunked_trees())
chunk_trees = trees[:100] + trees[200:300]
trees = list(dadegan.trees())
dep_trees = trees[:100] + trees[200:300]
#dep_output = codecs.open('dep_output.txt', 'w', encoding='utf8')
#sentences = []
#for sent in dadegan.sents():
#	sentences.append(' '.join([w for w, t in sent]))
indices = []

def tag_sent(chunks, args):
	tagged_sent = []
	global_index = 0
	for chunk in chunks:
		if type(chunk) is Tree:
			tokens = chunk.leaves()
		else:
			tokens = [chunk]
			chunk_label = 'O'
		for c in range(global_index, global_index + len(tokens)):
			info_label = 'O'
			local_index = c - global_index
			word = tokens[local_index][0]
			tag = tokens[local_index][1]
			if type(chunk) is Tree and local_index == 0:
				chunk_label = 'B-' + chunk.label()
			elif type(chunk) is Tree:
				chunk_label = 'I-' + chunk.label()
			for arg1 in args[0]:
				if c in arg1:
					if c == arg1[0]:
						info_label = 'B-Arg1'
					else:
						info_label = 'I-Arg1'
			for arg2 in args[1]:
				if info_label == 'O' and c in arg2:
					if c == arg2[0]:
						info_label = 'B-Arg2'
					else:
						info_label = 'I-Arg2'
			for rel in args[2]:
				if info_label == 'O' and c in rel:
					if c == rel[0]:
						info_label = 'B-Rel'
					else:
						info_label = 'I-Rel'
			tagged_sent.append((word, tag, chunk_label, info_label))
		global_index += len(tokens)
	return tagged_sent


def positions(info, sent):
	info_list = []

	for arg in info:
		arg_list = []
		index = sent.strip().find(arg)
		if index >= 0:
			tokens = sent.split()
			for i in range(len(tokens)):
				index -= len(tokens[i]) + 1
				if index < 0:
					for c in range(i, i + len(arg.split())):
						arg_list.append(c)
					break
		info_list.append(arg_list)
	return info_list

def gold_IOB_sents(filename='200DadeganSents.txt'):
	"""
	gold = []
	lines = codecs.open(filename, 'r', encoding='utf8').readlines()
	informations = []
	for line in lines:
		if len(re.findall(r'^\d+-', line)) == 0:
			if len(line) > 1:
				informations.append(line.replace('\n', '').split(' + '))
			else:
				gold.append(info2iob(sentences[number], chunk_trees[number], informations))
				informations = []
		else:
			number = int(re.findall(r'^\d+-', line)[0][:-1])
			indices.append(number)
	"""
	lines = codecs.open(filename, 'r', encoding='utf8').readlines()
	gold = []
	sentence = []
	for line in lines:
		line = line.strip()
		if line == '':
			gold.append(sentence)
			sentence = []
		else:
			sentence.append(tuple(line.split('\t')))
	return gold

def info2iob(sentence, chunks, informations):
	info_list = ([], [], [])
	for information in informations:
		temp_list = positions(information, sentence)
		for i in range(3):
			if temp_list[i] not in info_list[i]:
				info_list[i].append(temp_list[i])
	return tag_sent(chunks, info_list)





corrects = 0
total = 0
gold = gold_IOB_sents('Resources/Dadegan-pages/001.tsv') + gold_IOB_sents('Resources/Dadegan-pages/003.tsv')
sentences = []
evaluation_sents = []
for gold_sent in gold:
	sentences.append([w for w, t, c, l in gold_sent])
#tokens = tagger.tag_sents(sentences)
#chunk_trees = list(chunker.parse_sents(tokens))
#dep_trees = parser.parse_sents(sentences)
dep_tagged_sents = []
chunk_tagged_sents = []
for number, gold_sent in enumerate(gold):

	sentence = ' '.join(sentences[number])
	chunk_tree = chunk_trees[number]
	dep_tree = dep_trees[number]
	chunk_informations = list(chunk_extractor.extract(chunk_tree))
	dep_informations = list(dep_extractor.extract(dep_tree))
	evaluation_sent = [(w, l) for w, t, c, l in gold_sent]
	dep_tagged_sent = [(w,l) for w, t, c, l in [tokens for tokens in info2iob(sentence, chunk_tree, dep_informations)]]
	chunk_tagged_sent = [(w,l) for w, t, c, l in [tokens for tokens in info2iob(sentence, chunk_tree, chunk_informations)]]
	if len(evaluation_sent) == len(dep_tagged_sent):
		evaluation_sents.append(evaluation_sent)
		dep_tagged_sents.append(dep_tagged_sent)
		chunk_tagged_sents.append(chunk_tagged_sent)
	else:
		print(chunk_tagged_sent)
		print()
print('dependency accuracy: %f' % (accuracy(sum(evaluation_sents, []), sum(dep_tagged_sents, []))))
print('chunk accuracy: %f' % (accuracy(sum(evaluation_sents, []), sum(chunk_tagged_sents, []))))

information_tagger = IOBTagger(model='informations-all.model')
print(information_tagger.evaluate(gold))