import os
import re

dict_prefix = re.compile(r'dictionary.*\..*\.txt')

dictionary = {}

for fname in os.listdir('dataset') :
	if dict_prefix.match(fname) :
		print('merge ' + fname + '...')
		dname = fname.split('.')[0]
		if dname not in dictionary :
			dictionary[dname] = {}

		fin = open('dataset/%s' % fname, 'r', encoding='utf-8')
		for line in fin :
			sp = line.strip().split("\t")
			key = sp[0]
			words = sp[1].split(",") if len(sp) > 1 else []
			if key not in dictionary[dname] :
				dictionary[dname][key] = set()
			for w in words :
				dictionary[dname][key].add(w)

for key, vocabs in dictionary.items() :
	f = open('dataset/%s.txt' % key, 'w', encoding='utf-8')
	for vocab, translation in vocabs.items() :
		f.write("%s\t%s\n" % (vocab, ",".join(list(translation))) )