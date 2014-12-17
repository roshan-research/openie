
from hazm import DadeganReader
from DependencyTreeInformationExtractor import DependencyTreeInformationExtractor
from ChunkTreeInformationExtractor import ChunkTreeInformationExtractor


output = open('informations.txt', 'w', encoding='utf8')
dadegan = DadeganReader('Resources/Dadegan/train.conll')
chunk_extractor = ChunkTreeInformationExtractor()
dependency_extractor = DependencyTreeInformationExtractor()
for chunk_tree, dependency_graph in zip(dadegan.chunked_trees(), dadegan.trees()):
	for information in chunk_extractor.extract(chunk_tree):
		print(*information, sep=' - ', file=output)
	print(file=output)
	for information in dependency_extractor.extract(dependency_graph):
		print(*information, sep=' + ', file=output)
	print(file=output)