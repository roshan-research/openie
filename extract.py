
from __future__ import print_function
from hazm import *
from itertools import chain
from baaz import DependencyTreeInformationExtractor


hamshahri = HamshahriReader(root='corpora/hamshahri')
persica = PersicaReader(root='corpora/persica.csv')
uninformatives = set(sum([line.split(' - ') for line in open('data/adverbs.dat', encoding='utf8').read().split('\n') if line.strip() and not line.startswith('#')], []))


normalizer = Normalizer()
tagger = POSTagger(model='resources/postagger.model')
parser = TurboParser(tagger=tagger, lemmatizer=Lemmatizer(), model_file='resources/turboparser.model')
extractor = DependencyTreeInformationExtractor()


output = open('resources/informations.txt', 'w', encoding='utf8')
for text in chain(hamshahri.texts(), persica.texts()):
	sentences = [word_tokenize(sentence) for sentence in sent_tokenize(normalizer.normalize(text)) if len(sentence) > 10]

	for sentence in parser.parse_sents(sentences):
		print('#', *[node['word'] for node in tree.nodes.values() if node['word']], file=output)

		for information in extractor.extract(sentence):
			if information[1] not in uninformatives:
				print(*information, sep=' - ', file=output)
		print(file=output)
