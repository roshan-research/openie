from hazm import IOBTagger
import codecs


tagger = IOBTagger(patterns=[
		'*',

		'u:w=%X[0,0]',
		'u:wl1=%X[-1,0]',
		'u:wr1=%X[1,0]',
		#'u:wl2=%X[-2,0]',
		#'u:wr2=%X[2,0]',

		'*:tl1=%X[-1,1]',
		#'*:tl2=%X[-2,1]',
		#'*:tl3=%X[-3,1]',
		'*:t=%X[0,1]',
		'*:tr1=%X[1,1]',
		#'*:tr2=%X[2,1]',
		#'*:tr3=%X[3,1]',

		'*:cp=%m[0,2,"..$"]',
		'*:c=%X[0,2]',

		'*:c0l1=%X[-1,2]/%X[0,2]',
		'*:c0r1=%X[0,2]/%X[1,2]',

		'*:cl1=%X[-1,2]',
		'*:cl2=%X[-2,2]',
		#'*:cl3=%X[-3,2]',
		#'*:cl4=%X[-4,2]',
		#'*:cl5=%X[-5,2]',
		#'*:cl6=%X[-6,2]',
		'*:cr1=%X[1,2]',
		'*:cr2=%X[2,2]',
		#'*:cr3=%X[3,2]',
		#'*:cr4=%X[4,2]',
		#'*:cr5=%X[5,2]',
		#'*:cr6=%X[6,2]',
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
tagger.train(sentences[:THRESHOLD])
tagger.save_model('informations.model')
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
