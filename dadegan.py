

from nltk.parse import DependencyGraph
from InformationExtractor import InformationExtractor


def dadegan_text(conll_file='resources/train.conll'):
	text = open(conll_file).read()
	return text.replace('‌‌','‌').replace('\t‌','\t').replace('‌\t','\t').replace('\t ','\t').replace(' \t','\t').replace('\r', '').replace('\u2029', '‌')

extractor = InformationExtractor()
output = open('informations.txt', 'w')
for sentence in map(DependencyGraph, [item for item in dadegan_text().replace(' ', '_').split('\n\n') if item.strip()]):
	print('\n', '*', *[node['word'] for node in sentence.nodelist if node['word']], file=output)
	for information in extractor.extract(sentence):
		print(*information, sep=' - ', file=output)

