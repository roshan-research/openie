
import codecs
from hazm import DadeganReader
from baaz import DependencyTreeInformationExtractor, ChunkTreeInformationExtractor


output = codecs.open('resources/informations.txt', 'w', encoding='utf8')
dadegan = DadeganReader('corpora/train.conll')
chunk_extractor = ChunkTreeInformationExtractor()
dependency_extractor = DependencyTreeInformationExtractor()

for chunk_tree, dependency_tree in zip(dadegan.chunked_trees(), dadegan.trees()):
	for information in chunk_extractor.extract(chunk_tree):
		print(*information, sep=' - ', file=output)
	print(file=output)
	for information in dependency_extractor.extract(dependency_tree):
		print(*information, sep=' + ', file=output)
	print(file=output)
