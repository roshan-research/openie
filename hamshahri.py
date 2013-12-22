
from hazm import sent_tokenize, word_tokenize, Normalizer, HamshahriReader, POSTagger, DependencyParser
from InformationExtractor import InformationExtractor


hamshahri = HamshahriReader()
normalizer = Normalizer()
tagger = POSTagger()
parser = DependencyParser(tagger=tagger)
extractor = InformationExtractor()

output = open('informations.txt', 'w')
for text in hamshahri.texts():
	text = normalizer.normalize(text)
	sentences = [word_tokenize(sentence) for sentence in sent_tokenize(text)]
	tagged = tagger.batch_tag(sentences)
	parsed = parser.tagged_batch_parse(tagged)

	for sentence in parsed:
		print('\n', '*', *[node['word'] for node in sentence.nodelist if node['word']], file=output)
		for information in extractor.extract(sentence):
			print(*information, sep=' - ', file=output)

	break

