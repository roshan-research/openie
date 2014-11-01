
from hazm import sent_tokenize, word_tokenize, Normalizer, HamshahriReader, POSTagger, DependencyParser
from DependencyTreeInformationExtractor import DependencyTreeInformationExtractor
from progress.bar import Bar


hamshahri = HamshahriReader()
normalizer = Normalizer()
tagger = POSTagger()
parser = DependencyParser(tagger=tagger)
extractor = DependencyTreeInformationExtractor()
texts = []

output = open('informations.txt', 'w')
for text in Bar(max=310000).iter(hamshahri.texts()):
	texts.append(normalizer.normalize(text))
	if len(texts) <= 1000: continue

	sentences = []
	for text in texts:
		for sentence in sent_tokenize(text):
			words = word_tokenize(sentence)
			if len(words) >= 3:
				sentences.append(words)
	texts = []

	tagged = tagger.batch_tag(sentences)
	parsed = parser.tagged_batch_parse(tagged)

	for sentence in parsed:
		print('#', *[node['word'] for node in sentence.nodelist if node['word']], file=output)
		for information in extractor.extract(sentence):
			print(*information, sep=' - ', file=output)
		print(file=output)
