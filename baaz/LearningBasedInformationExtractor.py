from hazm import IOBTagger
import codecs
from nltk.tag import TaggerI

class LearningBasedInformationExtractor(TaggerI):
	def __init__(self, patterns=[
		'*',

		'*:tl1=%X[-1,1]',
		'*:t=%X[0,1]',
		'*:tr1=%X[1,1]',

		'*:cp=%m[0,2,"..$"]',
		'*:c=%X[0,2]',

		'*:c0l1=%X[-1,2]/%X[0,2]',
		'*:c0r1=%X[0,2]/%X[1,2]',

		'*:cl1=%X[-1,2]',
		'*:cl2=%X[-2,2]',
		'*:cr1=%X[1,2]',
		'*:cr2=%X[2,2]',
	], model = None):
		self.tagger = IOBTagger(patterns)
		if model is not None:
			self.model = model

	def train(self, sentences, model_file='Resources/informations.model'):
		self.tagger.train(sentences)
		self.tagger.save_model(model_file)
		self.model = self.tagger.model

	def tag(self, sent):
		return self.tagger.tag(sent)