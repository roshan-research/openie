
from hazm import DadeganReader
from baaz import ChunkTreeInformationExtractor, DependencyTreeInformationExtractor
from random import randint
import codecs, re


output = open('200DadeganSents-chunkExtractor.txt', 'w', encoding='utf8')
dadegan = DadeganReader('resources/Dadegan/train.conll')
chunk_extractor = ChunkTreeInformationExtractor()
dep_extractor = DependencyTreeInformationExtractor()
trees = list(dadegan.chunked_trees())
sentences = []
for sent in dadegan.sents():
	sentences.append(' '.join([w for w, t in sent]))
indices = []
gold = []
"""
for i in range(200):
	indices.append(randint(0, len(sentences)))
"""
lines = codecs.open('200DadeganSents.txt', 'r', encoding='utf8').readlines()
for line in lines:
	line = line.replace('\n', '')
	index = re.findall(r'^\d+-', line)
	if len(index) > 0:
		indices.append(int(index[0][:-1]))
	else:
		if len(line) > 1:
			gold.append(line.split(' + '))

corrects = 0
total = 0
for number in indices:
	chunk_tree = trees[number]
	#sentence = sentences[number]
	#print("%d- %s" % (number, sentence), file=output)
	for information in chunk_extractor.extract(chunk_tree):
		infoList = list(information)
		total += 1
		if infoList in gold:
			corrects += 1
			print(*information, sep=' + ')

print('gold: ', len(gold))
print('total: ', total)
print('correct: ', corrects)