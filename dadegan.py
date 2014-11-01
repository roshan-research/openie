
from hazm import DadeganReader
from DependencyTreeInformationExtractor import DependencyTreeInformationExtractor
from ChunkTreeInformationExtractor import ChunkTreeInformationExtractor


extractor = InformationExtractor()
output = open('informations.txt', 'w', encoding='utf8')
dadegan = DadeganReader('Resources/Dadegan/train.conll')
chunkExtractor = ChunkTreeInformationExtractor()
dependencyExtractor = InformationExtractor()
for chunk_tree, dependency_graph in zip(dadegan.chunked_trees(), dadegan.trees()):
	for information in chunkExtractor.extract(chunk_tree):
		print(*information, sep=' - ', file=output)
	print(file=output)
	for information in dependencyExtractor.extract(dependency_graph):
		print(*information, sep=' + ', file=output)
	print(file=output)