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
docvec = open('docvec/vector_s%d_w%d_v%d.txt' % (size, window, version), 'r', encoding='utf-8')
word2vec_id = Word2Vec.load('model/model_id_s%d_w%d_v%d.word2vec' % (size, window, version))
word2vec_en = Word2Vec.load('model/model_en_s%d_w%d_v%d.word2vec' % (size, window, version))
doc2vec_en = Doc2Vec.load('model/model_en_s%d_w%d_v%d.doc2vec' % (size, window, version))

def cosine(vector1,vector2):
    cosV12 = np.dot(vector1, vector2) / (np.linalg.norm(vector1) * np.linalg.norm(vector2))
    return cosV12

def get_english_queries() :
	with tf.Session() as sess:    
		saver = tf.train.import_meta_graph('./model/mlp_match_s%d_w%d_v%d/model.meta' % (size, window, version))
		saver.restore(sess,tf.train.latest_checkpoint('./model/mlp_match_s%d_w%d_v%d/' % (size, window, version)))
		graph = tf.get_default_graph()
		input_x = graph.get_tensor_by_name("input_x:0")
		out = graph.get_tensor_by_name('out:0')

		queries_id = Queries.Queries()
		queries_en = { 
			'title' : [],
			'desc' : [],
			'narr' : []
		}
		while queries_id.hasnext() :
			queries_id.next()
			qs = [
				tokenizer.tokenize(queries_id.title.strip().lower()),
				tokenizer.tokenize(queries_id.desc.strip().lower()),
				tokenizer.tokenize(queries_id.narr.strip().lower())
			]
			keys = [ 'title', 'desc', 'narr']

			for i in range(len(qs)) :
				q = []
				for t in qs[i] :
					tok = t
					if t not in word2vec_id.wv :
						tok = stemmer_id.stem(t)

					if tok in word2vec_id.wv :
						vec = sess.run(out, feed_dict={input_x : word2vec_id.wv[tok].reshape(-1, size)})
						model_word_vector = np.array( vec, dtype='f').reshape(size)
						most_similar_words = word2vec_en.most_similar( [ model_word_vector ], [], 2)
						q += [x[0] for x in most_similar_words]
				if (len(q) == 0) :
					print('empty query %d ' % i)
				queries_en[keys[i]].append(q)

		return queries_en

queries = get_english_queries()
keys = [ 'title', 'desc', 'narr']
queries_vector = {}
fout = {}
for k in keys :
	queries_vector[k] = []
	fout[k] = open('result/res_mono_stemmed_s%d_w%d_v%d_%s.txt' % (size, window, version, k), 'w', encoding='utf-8')
	for q in queries[k] :
		print(len(q))
		vec = doc2vec_en.infer_vector(q)
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
