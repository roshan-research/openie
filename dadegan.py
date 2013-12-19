

from nltk.parse import DependencyGraph
from InformationExtractor import InformationExtractor


class FixedDependencyGraph(DependencyGraph):
	def _parse(self, input):
		lines = [DependencyGraph._normalize(line) for line in input.split('\n') if line.strip()]
		temp = []
		for index, line in enumerate(lines):
			cells = line.split('\t')
			_, word, _, tag, _, _, head, rel, _, _ = cells
			head = int(head)
			self.nodelist.append({'address': index+1, 'word': word, 'tag': tag, 'head': head, 'rel': rel, 'deps': [d for (d,h) in temp if h == index+1]})
			try:
				self.nodelist[head]['deps'].append(index+1)
			except IndexError:
				temp.append((index+1, head))

		root_address = self.nodelist[0]['deps'][0]
		self.root = self.nodelist[root_address]


def dadegan_text(conll_file='resources/train.conll'):
	text = open(conll_file).read()
	return text.replace('‌‌','‌').replace('\t‌','\t').replace('‌\t','\t').replace('\t ','\t').replace(' \t','\t').replace('\r', '').replace('\u2029', '‌')

extractor = InformationExtractor()
output = open('informations.txt', 'w')
for sentence in map(FixedDependencyGraph, [item for item in dadegan_text().replace(' ', '_').split('\n\n') if item.strip()]):
	print('\n', '*', *[node['word'] for node in sentence.nodelist if node['word']], file=output)
	for information in extractor.extract(sentence):
		print(*information, sep=' - ', file=output)

