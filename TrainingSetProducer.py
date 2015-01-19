
from hazm import sent_tokenize, word_tokenize, Normalizer, HamshahriReader, SequencePOSTagger, DependencyParser, Chunker, Lemmatizer
from baaz import DependencyTreeInformationExtractor, ChunkTreeInformationExtractor
from progress.bar import Bar
from nltk import Tree
from itertools import combinations
import codecs, re

arg = lambda chunk: ' '.join([word for word, tag in chunk.leaves()])
hamshahri = HamshahriReader('Resources/Hamshahri/')
normalizer = Normalizer()
tagger = SequencePOSTagger(model='Resources/postagger-remove-w3-all.model')
parser = DependencyParser(tagger=tagger, lemmatizer=Lemmatizer())
chunker = Chunker(tagger, model='Resources/chunker-dadeganFull.model')
dependencyExtractor = DependencyTreeInformationExtractor()
chunkExtractor = ChunkTreeInformationExtractor()
texts = []

output = codecs.open('trainingSet.txt', 'w', encoding='utf8')

def extractCandidates(chunk_tree):
	candidates = []
	chunks_list = list(chunk_tree)
	for chunk in chunk_tree:
		if type(chunk) is not Tree and chunk[1] == "PUNC":
			chunks_list.remove(chunk)

	for c in range(len(chunks_list)):
		chunk = chunks_list[c]
		if c > 0:
			previuos = chunks_list[c - 1]
		else:
			previuos = None

		if c < len(chunks_list) - 1:
			next = chunks_list[c + 1]
		else:
			next = None
		if type(chunk) == Tree and chunk.label() in {'NP'}:
			candidate = arg(chunk)
			if type(previuos) == Tree and previuos.label() == 'PP':
				candidate = arg(previuos) + ' ' + candidate
			elif type(next) == Tree and next.label() == 'POSTP':
				candidate = candidate + ' ' + arg(next)
			candidates.append(candidate)

	return candidates


def tag_sent(chunks, args):

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
			print(word, tag, chunk_label, info_label, sep='\t', file=output)
		global_index += len(tokens)
	print(file=output)


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

input = codecs.open('200DadeganSents.txt', 'r', encoding='utf8')
informations = []
for line in input.readlines():
	if len(re.findall(r'^\d+-', line)) == 0:
		if len(line) > 1:
			informations.append(line.replace('\n', '').split(' + '))
		else:
			info_list = ([], [], [])
			for information in informations:
				temp_list = positions(information, sentence)
				for i in range(3):
					if temp_list[i] not in info_list[i]:
						info_list[i].append(temp_list[i])
			tag_sent(chunks, info_list)
			informations = []
	else:
		sentence = re.sub(r'^\d+-', '', line)
		sentence = sentence.replace('\n', '')
		print(sentence)
		tokens = word_tokenize(normalizer.normalize(sentence))
		chunks = chunker.parse(tokens)
		candidates = extractCandidates(chunks)
		candidateArgs = combinations(candidates, 2)



