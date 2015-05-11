
from hazm import DadeganReader
from baaz import DependencyTreeInformationExtractor, ChunkTreeInformationExtractor


output = open('resources/informations.txt', 'w', encoding='utf8')
dadegan = DadeganReader('corpora/train.conll')
chunk_extractor = ChunkTreeInformationExtractor()
dependency_extractor = DependencyTreeInformationExtractor(adverbs_file='data/adverbs.dat')

for chunk_tree, dependency_graph in zip(dadegan.chunked_trees(), dadegan.trees()):
	for information in chunk_extractor.extract(chunk_tree):
		print(*information, sep=' - ', file=output)
	print(file=output)
	for information in dependency_extractor.extract(dependency_graph):
		print(*information, sep=' + ', file=output)
	print(file=output)
