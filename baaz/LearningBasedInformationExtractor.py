from hazm import IOBTagger
import codecs


tagger = IOBTagger(patterns=[
		'u:t=%X[0,1]',
		'u:c=%X[0,2]',
		'u:a=%X[0,3]'
	])

training = codecs.open('trainingSet.txt', 'r', encoding='utf8').read()

sentences = []

for i, raw_sentence in enumerate(training.split('\n\n')):
	sentence = []
	if len(raw_sentence) < 1:
		continue
	for word in raw_sentence.split('\n'):
		features = word.split('\t')
		sentence.append(tuple(features))
	sentences.append(sentence)



#THRESHOLD = int(len(sentences) * 0.9)
tagger.train(sentences)
tagger.save_model('informations.model')
test = []
for sentence in sentences:
	test_sent = []
	for token in sentence:
		if len(token) < 5:
			print(token)
		test_sent.append(token[:-1])
	test.append(test_sent)

tagged_sents = tagger.tag_sents(test)
corrects = 0
total = 0
for tagged, gold in zip(tagged_sents, sentences[:1]):
	for tagged_token, gold_token in zip(tagged, gold):
		if tagged_token[-1] != 'O':
			print(tagged)
		if tagged_token[-1] == gold_token[-1]:
			corrects += 1
		total += 1

print(corrects / total)

print(sentences[1])
print()
print(tagger.tag(test[1]))
