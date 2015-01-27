from hazm import IOBTagger
import codecs
from nltk.tag import TaggerI



tagger = IOBTagger(patterns=[
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
	])

training = codecs.open('trainingSet_dadegan.txt', 'r', encoding='utf8').read()

sentences = []

for i, raw_sentence in enumerate(training.split('\n\n')):
	sentence = []
	if len(raw_sentence) < 1:
		continue
	for word in raw_sentence.split('\n'):
		features = word.split('\t')
		sentence.append(tuple(features))
	sentences.append(sentence)



THRESHOLD = int(len(sentences) * 0.9)
tagger.train(sentences)
tagger.save_model('informations-all-withWords.model')
"""
test = []
for sentence in sentences[THRESHOLD:]:
	test_sent = []
	for token in sentence:
		test_sent.append(token[:-1])
	test.append(test_sent)

tagged_sents = tagger.tag_sents(test)
corrects = 0
total = 0
for tagged, gold in zip(tagged_sents, sentences[THRESHOLD:]):
	for tagged_token, gold_token in zip(tagged, gold):
		if tagged_token[-1] == gold_token[-1]:
			corrects += 1
		total += 1

print(corrects / total)
"""
print(tagger.evaluate(sentences[THRESHOLD:]))
print(sentences[0])
print()
#print(tagger.tag(test[0]))
