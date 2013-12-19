
from itertools import product

class InformationExtractor():

	def __init__(self):
		self.adverbs = set(sum([line.split(' - ') for line in open('adverbs.dat').read().split('\n') if line.strip() and not line.startswith('#')], []))

	def extract(self, dependencygraph):
		""" extracts information from dependency tree """

		nodes = dependencygraph.nodelist
		childs = lambda parent, rels=None: [nodes[n] for n in parent['deps'] if not rels or nodes[n]['rel'] == rels or nodes[n]['rel'] in rels]
		subtree = lambda parent: sum([subtree(child) for child in childs(parent)], [parent])
		words = lambda nodes: ' '.join([node['word'] for node in sorted(nodes, key=lambda n: n['address'])])

		verbs = [node for node in nodes if node['tag'] == 'V']
		for verb in verbs:
			relation = [verb]
			arg1s = childs(verb, 'SBJ')
			arg2s = childs(verb, ('OBJ', 'ADV', 'VPP', 'OBJ2', 'TAM'))

			for nve in childs(verb, 'NVE'):
				relation.append(nve)
				for child in childs(nve):
					if child['rel'] == 'NPP':
						arg2s.append(child)
					else:
						relation.extend(subtree(child))

			for mos in childs(verb, 'MOS'):
				relation.append(mos)
				for child in childs(mos):
					if child['rel'] == 'AJPP':
						arg2s.append(child)
					else:
						relation.extend(subtree(child))

			for vprt in childs(verb, 'VPRT'):
				relation.extend(subtree(vprt))

			# yield results
			for arg1, arg2 in product(arg1s, arg2s):
				information = list(map(words, (subtree(arg1), subtree(arg2), relation)))
				if information[1] not in self.adverbs:
					yield information
