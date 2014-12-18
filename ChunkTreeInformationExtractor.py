from __future__ import print_function
from itertools import product
from nltk.tree import Tree


class ChunkTreeInformationExtractor():
    def __init__(self):
        self.arg = lambda chunk: ' '.join([word for word, tag in chunk.leaves()])

    def extract(self, chunked_tree):
        """ extracts information from dependency tree """
        informations = []
        arg1s = []
        arg2s = []
        chunks_list = list(chunked_tree)
        for chunk in chunked_tree:
            if type(chunk) is not Tree and chunk[1] == "PUNC":
                chunks_list.remove(chunk)

        for c in range(len(chunks_list)):
            if c >= len(chunks_list):
                break
            chunk = chunks_list[c]
            if type(chunk) is not Tree:
                try:
                    if chunk[0] == 'که':
                        last_args = []
                        if len(arg1s) > 0 and self.arg(chunks_list[c-1]) in arg1s[-1]:
                            last_args = arg1s
                        elif len(arg2s) > 0 and self.arg(chunks_list[c-1]) in arg2s[-1]:
                            last_args = arg2s
                        else:
                            continue
                        last_label = ''
                        while type(chunk) is not Tree or last_label is not 'VP':
                            chunk = chunks_list[c]
                            if type(chunk) is Tree:
                                last_args[-1] += ' ' + self.arg(chunk)
                                last_label = chunk.label()
                            else:
                                last_args[-1] += ' ' + chunk[0]
                            chunks_list.pop(c)
                except Exception as e:
                    print(e)
                continue
            if chunk.label() == 'NP':
                try:
                    if type(chunks_list[c - 1]) == Tree and chunks_list[c - 1].label() == 'PP':
                        arg2s.append(self.arg(chunks_list[c - 1]) + ' ' + self.arg(chunk))
                    elif type(chunks_list[c + 1]) == Tree and chunks_list[c + 1].label() == 'POSTP':
                        arg2s.append(self.arg(chunk) + ' ' + self.arg(chunks_list[c + 1]))
                    else:
                        if len(arg1s) == 0:
                            arg1s.append(self.arg(chunk))
                except Exception as e:
                    continue
            elif chunk.label() == 'VP':
                rel = self.arg(chunk)
                if type(chunks_list[c - 1]) is Tree and chunks_list[c - 1].label() is 'ADJP':
                    rel = self.arg(chunks_list[c-1]) + ' ' + rel
                for arg1, arg2 in product(arg1s, arg2s):
                    informations.append((arg1, arg2, rel))
                arg1s = []
                arg2s = []

        return informations

