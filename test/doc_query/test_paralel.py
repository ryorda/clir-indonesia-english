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
from nltk.corpus import stopwords
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

factory = StemmerFactory()
id_stemmer = factory.create_stemmer()
id_stops = set(stopwords.words('indonesian'))

re_clean = re.compile(r'[^A-Za-z0-9]', re.M)

size = int(sys.argv[1])
window = int(sys.argv[2])
min_count = int(sys.argv[3])
mode = int(sys.argv[4])
topn_paralel = int(sys.argv[5])
topn_test = int(sys.argv[6])

doc2vec_paralel = Doc2Vec.load('model/doc_query/model_paralel_s%d_w%d_c%d_v%d.doc2vec' % (size, window, min_count, mode))
doc2vec_test = Doc2Vec.load('model/doc_query/model_en_test_s%d_w%d_c%d_v%d.doc2vec' % (size, window, min_count, mode))

def get_indonesia_queries() :
		
		queries_id = Queries.Queries('IN')
		queries = { 
			'title' : [],
			'desc' : [],
			'narr' : []
		}
		while queries_id.hasnext() :
			queries_id.next()
			qs = [
				queries_id.title.strip().lower(),
				queries_id.desc.strip().lower(),
				queries_id.narr.strip().lower()
			]
			keys = [ 'title', 'desc', 'narr']

			if mode == 1 :
				for i in range(len(qs)) :
					qs[i] = qs[i].split()

			elif mode == 2 :
				for i in range(len(qs)) :
					qs[i] = re_clean.sub(' ', qs[i])

				for i in range(len(qs)) :
					qs[i] = qs[i].split()

			elif mode == 3 :
				for i in range(len(qs)) :
					text = []
					for t in qs[i].split() :
						if t not in id_stops :
							text.append(t)
					qs[i] = text

			elif mode == 4 :
				for i in range(len(qs)) :
					text = []
					for t in qs[i].split() :
						text.append(id_stemmer.stem(t))
					qs[i] = text				
			else :
				print ('[ERROR] invalid mode')
				exit()


			for i in range(len(qs)) :
				q = qs[i].copy()
				queries[keys[i]].append(q)
			queries['title_desc'] = [x + y for (x, y) in zip(queries['title'], queries['desc'])]

		return queries

queries = get_indonesia_queries()
keys = [ 'title', 'desc', 'narr', 'title_desc']
queries_vector = {}
fout = {}
for k in keys :
	queries_vector[k] = []
	fout[k] = open('result/doc_query/res_paralel_test_s%d_w%d_c%d_v%d_%s.txt' % (size, window, min_count, mode, k), 'w', encoding='utf-8')
	idx = 0

	for q in queries[k] :
		vec_paralel = doc2vec_paralel.infer_vector(q)
		docs_paralel = doc2vec_paralel.docvecs.most_similar(positive = [vec_paralel], topn = topn_paralel)
		doc_query = []
		print('most similar documents to {1} of query {0} :'.format(idx, k))
		for (d_par, _) in docs_paralel :
			d_par_name = d_par.split(":")[1].strip()
			print('\t - {0}'.format(d_par_name))
			f = open('dataset/doc_query/clean/en_id/{0}/{1}'.format(mode, d_par_name), 'r', encoding='utf-8')
			for line in f :
				doc_query += line.strip().split()

		vec_test = doc2vec_test.infer_vector(doc_query)
		docs_test = doc2vec_test.docvecs.most_similar(positive = [vec_test], topn = topn_test)
		for (d, sim) in docs_test :
			docname = "_".join(d.split('_')[1:]).strip()
			fout[k].write('%d %s %f\n' % (idx, docname, sim))
		idx +=1
		fout[k].flush()

