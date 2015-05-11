
from __future__ import print_function
from hazm import *
from baaz import DependencyTreeInformationExtractor


hamshahri = HamshahriReader()
normalizer = Normalizer()
tagger = POSTagger(model='resources/postagger.model')
parser = TurboParser(tagger=tagger, lemmatizer=Lemmatizer(), model_file='resources/turboparser.model')
extractor = DependencyTreeInformationExtractor()
texts = []

output = open('informations.txt', 'w')
for text in hamshahri.texts():
	texts.append(normalizer.normalize(text))
	if len(texts) <= 1000:
		continue

	sentences = []
	for text in texts:
		for sentence in sent_tokenize(text):
			words = word_tokenize(sentence)
			if len(words) >= 3:
				sentences.append(words)
	texts = []

	for sentence in parser.parse_sents(sentences):
		print('#', *[node['word'] for node in tree.nodes.values() if node['word']], file=output)
		for information in extractor.extract(sentence):
			print(*information, sep=' - ', file=output)
		print(file=output)
