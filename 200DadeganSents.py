
from hazm import DadeganReader
from baaz import ChunkTreeInformationExtractor, DependencyTreeInformationExtractor
from hazm import Chunker, Normalizer, word_tokenize, SequencePOSTagger
from random import randint
import codecs, re
from nltk.tree import Tree


output = open('200DadeganSents-chunkExtractor.txt', 'w', encoding='utf8')
dadegan = DadeganReader('resources/Dadegan/train.conll')
tagger = SequencePOSTagger(model='Resources/postagger-remove-w3-all.model')
chunker = Chunker(model='Resources/chunker-dadeganFull.model')
normalizer = Normalizer()
chunk_extractor = ChunkTreeInformationExtractor()
dep_extractor = DependencyTreeInformationExtractor()
trees = list(dadegan.chunked_trees())
sentences = []
for sent in dadegan.sents():
	sentences.append(' '.join([w for w, t in sent]))
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
	gold = []
	lines = codecs.open(filename, 'r', encoding='utf8').readlines()
	informations = []
	for line in lines:
		if len(re.findall(r'^\d+-', line)) == 0:
			if len(line) > 1:
				informations.append(line.replace('\n', '').split(' + '))
			else:
				gold.append(info2iob(sentence, chunks, informations))
				informations = []
		else:
			indices.append(int(re.findall(r'^\d+-', line)[0][:-1]))
			sentence = re.sub(r'^\d+-', '', line)
			sentence = sentence.replace('\n', '')
			print(sentence)
			tokens = word_tokenize(normalizer.normalize(sentence))
			tagged_tokens = tagger.tag(tokens)
			chunks = chunker.parse(tagged_tokens)
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
gold = gold_IOB_sents()
for number, gold_sent in zip(indices, gold):
	chunk_tree = trees[number]
	sentence = sentences[number]
	#print("%d- %s" % (number, sentence), file=output)
	informations = chunk_extractor.extract(chunk_tree)
	for extractor_token, gold_token in zip(info2iob(sentence,chunk_tree, informations), gold_sent):
		if extractor_token[-1] == gold_token[-1]:
			corrects += 1
		total += 1


#print('gold: ', len(gold))
print('total: ', total)
print('correct: ', corrects)
print(corrects/total)