# coding: utf8

from __future__ import unicode_literals
import re
from lucene import *


class InformationSearcher():
	def __init__(self, index_dir):
		initVM()
		self.vm_env = getVMEnv()
		self.index = IndexSearcher(SimpleFSDirectory(File(index_dir)), True)
		self.maxnum = 100

	def search(self, arg1, arg2, rel):
		self.vm_env.attachCurrentThread()

		main_query = BooleanQuery()
		arg1_query = BooleanQuery()
		arg2_query = BooleanQuery()
		rel_query = BooleanQuery()
		arg1_query.setMinimumNumberShouldMatch(1)
		arg2_query.setMinimumNumberShouldMatch(1)
		rel_query.setMinimumNumberShouldMatch(1)

		arg1_query.add(WildcardQuery(Term('arg1', '*' + arg1 + '*')), BooleanClause.Occur.SHOULD)
		arg1_query.add(WildcardQuery(Term('arg1_data', arg1.lower().replace(' ', '_'))), BooleanClause.Occur.SHOULD)
		arg1_query.add(WildcardQuery(Term('arg1_data', 'en:' + arg1.lower().replace(' ', '_'))), BooleanClause.Occur.SHOULD)
		arg1_query.add(WildcardQuery(Term('arg1_data', 'fa:' + arg1.lower().replace(' ', '_'))), BooleanClause.Occur.SHOULD)

		arg2_query.add(WildcardQuery(Term('arg2', '*' + arg2 + '*')), BooleanClause.Occur.SHOULD)
		arg2_query.add(WildcardQuery(Term('arg2_data', arg2.lower().replace(' ', '_'))), BooleanClause.Occur.SHOULD)
		arg2_query.add(WildcardQuery(Term('arg2_data', 'en:' + arg2.lower().replace(' ', '_'))), BooleanClause.Occur.SHOULD)
		arg2_query.add(WildcardQuery(Term('arg2_data', 'fa:' + arg2.lower().replace(' ', '_'))), BooleanClause.Occur.SHOULD)

		rel_query.add(TermQuery(Term('rel', rel)), BooleanClause.Occur.SHOULD)
		rel_query.add(TermQuery(Term('rel_cluster', rel)), BooleanClause.Occur.SHOULD)

		main_query.add(arg1_query, BooleanClause.Occur.MUST)
		main_query.add(arg2_query, BooleanClause.Occur.MUST)
		main_query.add(rel_query, BooleanClause.Occur.MUST)

		docs = self.index.search(main_query, self.maxnum)
		return {
			'informations': [Information(self.index.doc(item.doc)) for item in docs.scoreDocs],
			'hits': len(docs.scoreDocs),
		}


class Information():
	def __init__(self, doc):
		fields = doc.getFields()
		for i in range(fields.size()):
			field = fields.get(i)
			self.addField(field.name().lower(), field.stringValue())

		def parse_data(arg1_data):
			if len(arg1_data) > 0:
				return arg1_data[0], map(lambda label: label.replace('en:', '').replace('fa:', ''), arg1_data[1:])
			else:
				return '', ''

		self.arg1_wiki, self.arg1_labels = parse_data(self.arg1_data)
		self.arg2_wiki, self.arg2_labels = parse_data(self.arg2_data)

	def html(self):
		refine = lambda s: s.replace('_', ' ')

		highlights = {
			refine(self.rel): '<a class="rel">{}</a>'.format(refine(self.rel)),
			refine(self.arg1): '<a class="arg1" {} rel="{}">{}</a>'.format('href="%s"' % self.arg1_wiki if self.arg1_wiki else '', self.arg1_labels, refine(self.arg1)),
			refine(self.arg2): '<a class="arg2" {} rel="{}">{}</a>'.format('href="%s"' % self.arg2_wiki if self.arg2_wiki else '', self.arg2_labels, refine(self.arg2)),
		}

		result = ' %s ' % refine(self.info)
		for key, value in highlights.items():
			if result.count(key) == 1:
				result = result.replace(key, value)
			else:
				result = re.sub(' %s([.:,?!،؟]?) ' % key, r' %s\1 ' % value, result)

		return result.strip()

	def addField(self, name, value):
		if hasattr(self, name):
			val = getattr(self, name)
			if isinstance(val, list):
				val.append(value)
			else:
				newval = [val, value]
				setattr(self, name, newval)
		else:
			setattr(self, name, value)
