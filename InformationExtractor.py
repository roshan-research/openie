
from hazm import *
from baaz import DependencyTreeInformationExtractor


class InformationExtractor():

	def __init__(self):
		self.uninformatives = set(sum([line.split(' - ') for line in open('data/adverbs.dat', encoding='utf8').read().split('\n') if line.strip() and not line.startswith('#')], []))
		self.normalizer = Normalizer()
		self.tagger = POSTagger(model='resources/postagger.model')
		self.parser = DependencyParser(tagger=self.tagger, lemmatizer=Lemmatizer())
		self.extractor = DependencyTreeInformationExtractor()

	def analyze(self, text):
		sentences = [sentence for sentence in sent_tokenize(self.normalizer.normalize(text)) if len(sentence) > 15]
		if not sentences:
			return []

		for sentence, tree in zip(sentences, self.parser.parse_sents(map(word_tokenize, sentences))):
			for information in self.extractor.extract(tree):
				if information[1] not in self.uninformatives:
					yield information


if __name__ == '__main__':
	text = 'ویکی‌پدیا بر سیاست «دیدگاه بی‌طرفانه» تأکید می‌کند.'

	information_extractor = InformationExtractor()
	for information in information_extractor.analyze(text):
		print(*information, sep=' - ')
