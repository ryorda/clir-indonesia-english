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
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

factory = StemmerFactory()
stemmer_id = factory.create_stemmer()	

tokenizer = TweetTokenizer()

size = int(sys.argv[1])
window = int(sys.argv[2])
version = int(sys.argv[3])

print('processing docvec/vector_s%d_w%d_v%d.txt' % (size, window, version))
docvec = open('docvec/vector_bil_s%d_w%d_v%d.txt' % (size, window, version), 'r', encoding='utf-8')
doc2vec_bil = Doc2Vec.load('model/model_bil_s%d_w%d_v%d.doc2vec' % (size, window, version))

def cosine(vector1,vector2):
    cosV12 = np.dot(vector1, vector2) / (np.linalg.norm(vector1) * np.linalg.norm(vector2))
    return cosV12

def get_queries() :

		queries = Queries.Queries()
		queries_res = { 
			'title' : [],
			'desc' : [],
			'narr' : []
		}
		while queries.hasnext() :
			queries.next()
			qs = [
				tokenizer.tokenize(queries.title.strip().lower()),
				tokenizer.tokenize(queries.desc.strip().lower()),
				tokenizer.tokenize(queries.narr.strip().lower())
			]
			keys = [ 'title', 'desc', 'narr']

			for i in range(len(qs)) :
				queries_res[keys[i]].append(qs[i])

		return queries_res

queries = get_queries()
keys = [ 'title', 'desc', 'narr']
queries_vector = {}
fout = {}
for k in keys :
	queries_vector[k] = []
	fout[k] = open('result/res_bil_s%d_w%d_v%d_%s.txt' % (size, window, version, k), 'w', encoding='utf-8')
	for q in queries[k] :
		print(len(q))
		vec = doc2vec_bil.infer_vector(q)
		queries_vector[k].append(vec)

for line in docvec :
	doc = line.strip().split('\t')
	docno = doc[0]
	print('result of %s...' % docno)

	vec = [float(x) for x in doc[1].split(",")]
	for k in keys :
		idx = 0
		for q in queries_vector[k] :
			cos = cosine(q, vec)
			fout[k].write('%d %s %f\n' % (idx, docno, cos))
			idx += 1
		fout[k].flush()
