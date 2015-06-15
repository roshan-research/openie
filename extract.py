
from __future__ import print_function
import codecs
from itertools import chain
from hazm import *
from baaz import DependencyTreeInformationExtractor


hamshahri = HamshahriReader(root='corpora/hamshahri')
persica = PersicaReader(csv_file='corpora/persica.csv')
uninformatives = set(sum([line.split(' - ') for line in codecs.open('data/adverbs.dat', encoding='utf8').read().split('\n') if line.strip() and not line.startswith('#')], []))


normalizer = Normalizer()
tagger = POSTagger(model='resources/postagger.model')
parser = TurboParser(tagger=tagger, lemmatizer=Lemmatizer(), model_file='resources/turboparser.model')
extractor = DependencyTreeInformationExtractor()


output = codecs.open('resources/informations.txt', 'w', encoding='utf8')
for text in chain(hamshahri.texts(), persica.texts()):
	try:
		sentences = [word_tokenize(sentence) for sentence in sent_tokenize(normalizer.normalize(text)) if len(sentence) > 15]

		for tree in parser.parse_sents(sentences):
			print('#', *[node['word'] for node in tree.nodes.values() if node['word']], file=output)

			for information in extractor.extract(tree):
				if information[1] not in uninformatives:
					print(*information, sep=' - ', file=output)
			print(file=output)

	except:
		print('Error while prcoessing:', *sentences, sep='\n')
