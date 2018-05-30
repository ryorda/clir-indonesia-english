from gensim.models import keyedvectors
from gensim.models import Doc2Vec
from gensim.models import Word2Vec
import re 
import os
import Queries
from multiprocessing import Pool
import sys
from nltk.tokenize import TweetTokenizer
import time
import numpy as np
import tensorflow as tf
from nltk.stem.porter import *

stemmer_en = PorterStemmer()

tokenizer = TweetTokenizer()

size = int(sys.argv[1])
window = int(sys.argv[2])
version = int(sys.argv[3])

mode = sys.argv[4]

topn = int(sys.argv[5])

print('top %d' % topn)

print('processing docvec/vector_s%d_w%d_v%d.txt' % (size, window, version))
doc2vec_en = Doc2Vec.load('model/model_en_test_s%d_w%d_v%d.doc2vec' % (size, window, version))

def get_english_queries() :

		queries_en = Queries.Queries('EN')
		queries = { 
			'title' : [],
			'desc' : [],
			'narr' : []
		}
		while queries_en.hasnext() :
			queries_en.next()
			qs = [
				tokenizer.tokenize(queries_en.title.strip().lower()),
				tokenizer.tokenize(queries_en.desc.strip().lower()),
				tokenizer.tokenize(queries_en.narr.strip().lower())
			]
			keys = [ 'title', 'desc', 'narr']

			for i in range(len(qs)) :
				q = qs[i].copy()
				if mode == 'stemmed' :
					for j in range(len(q)) :
						q[i] = stemmer_en.stem(q[i])
				queries[keys[i]].append(q)

			queries['title_desc'] = [x + y for (x, y) in zip(queries['title'], queries['desc'])]
		return queries

queries = get_english_queries()
keys = [ 'title', 'desc', 'narr', 'title_desc']
queries_vector = {}
fout = {}
for k in keys :
	queries_vector[k] = []
	fout[k] = open('result/res_monolingual_test_%s_s%d_w%d_v%d_%s.txt' % (mode, size, window, version, k), 'w', encoding='utf-8')
	idx = 0
	print(len(queries[k]))
	for q in queries[k] :
		vec = doc2vec_en.infer_vector(q)
		docs  = doc2vec_en.docvecs.most_similar(positive=[vec], topn = topn)
		print('docs %d' % len(docs))
		for (d, sim) in docs :
			docname = "_".join(d.split('_')[1:]).strip()
			print("%s\t%f" % (docname, sim))
			fout[k].write('%d %s %f\n' % (idx, docname, sim))
		idx +=1
		fout[k].flush()

