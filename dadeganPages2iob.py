from codecs import open as codecs_open
from os.path import join, split
from hazm import word_tokenize, sent_tokenize, DadeganReader
from nltk.tree import Tree


open = lambda *args: codecs_open(*args, encoding='utf8')

mergeTags = True
dadeganDir = 'Resources/Dadegan-pages'
dadegan = DadeganReader('Resources/Dadegan/test.conll')
chunks = list(dadegan.chunked_trees())[200:300]
tsvFp = open('Resources/Dadegan-pages/003.tsv', 'w')
sorted_lines = sorted(open('Resources/Dadegan-pages/003.ann').readlines(), key=lambda l: int(l.split(' ')[1]))

def getCurrent_line():
	current_line = sorted_lines.pop(0)
	tab_parts = current_line.split('\t')
	_type, start, end = tab_parts[1].split(' ')
	start = int(start)
	end = int(end)
	text = tab_parts[2]
	return _type, start, end, text

global_index = 0
_type, start, end, text = getCurrent_line()
for i in range(100):
	chunk_tree = chunks[i]
	for chunk in chunk_tree:
		if type(chunk) is Tree:
			tokens = chunk.leaves()
			chunk_label = chunk.label()
		else:
			tokens = [chunk]
			chunk_label = 'O'
		for c, node in enumerate(tokens):
			word, tag = node[0], node[1]
			if chunk_label != 'O':
				if c == 0:
					chunk_tag = 'B-' + chunk_label
				else:
					chunk_tag = 'I-' + chunk_label
			word_start = global_index
			word_end = global_index + len(word)
			info_tag = 'O'
			if word_start > end and len(sorted_lines) > 0:
				_type, start, end, text = getCurrent_line()
			if word_start >= start:
				if word_end <= end:
					if word not in text:
						continue
					if word_start == start:
						info_tag = 'B-' + _type
					else:
						info_tag = 'I-' + _type
				else:
					print('error', word, text)
			else:
				if word_end > start:
					print(word, text)
				info_tag = 'O'
			print(*(word, tag, chunk_tag, info_tag), sep='\t', file=tsvFp)
			global_index += 1 + len(word)
	print(file=tsvFp)



"""
for fileNum in [1, 3]:
    tsvFp = open('Resources/Dadegan-pages/%.3d.tsv'%fileNum, 'w')
    baseFpath = join(dadeganDir, '%.3d.'%fileNum)
    text = open(baseFpath + 'txt').read()
    toIndex = 0
    sorted_lines = sorted(open(baseFpath + 'ann').readlines(), key=lambda l: int(l.split(' ')[1]))
	line = sorted_lines[0]
    for line in sorted_lines:
        if not line:
            continue
        #line = toUnicode(line)
        tab_parts = line.split('\t')
        try:
            if tab_parts[0] == 'T332':
                print('HI')
            _type, start, end = tab_parts[1].split(' ')
            start = int(start)
            end = int(end)
            ne = tab_parts[2]
        except ValueError:
            print(line)
            continue
        pre_text = text[toIndex:start]
        for word in word_tokenize(pre_text):
            tsvFp.write('%s\tO\n'%word)
        for index, word in enumerate(word_tokenize(ne)):
            if mergeTags:
                tmp_type = ('B' if index==0 else 'I') + '-' + _type
            else:
                tmp_type = _type
            tsvFp.write('%s\t%s\n'%(word, tmp_type))
        toIndex = end
    post_text = text[toIndex:]
    for word in word_tokenize(pre_text):
        tsvFp.write('%s\tO\n'%word)
    tsvFp.close()
"""



