
from itertools import product


class DependencyTreeInformationExtractor():
	""" extracts information from dependency tree """

	def extract(self, dependencygraph):
		nodes = dependencygraph.nodelist
		childs = lambda parent, rels=None: [nodes[n] for n in parent['deps'] if not rels or nodes[n]['rel'] == rels or nodes[n]['rel'] in rels]
		subtree = lambda parent: sum([subtree(child) for child in childs(parent)], [parent])
		words = lambda nodes: ' '.join([node['word'] for node in sorted(nodes, key=lambda n: n['address']) if node['rel'] != 'PUNC'])

		verbs = [node for node in nodes if node['ctag'] == 'V']
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
				yield list(map(words, (subtree(arg1), subtree(arg2), relation)))
