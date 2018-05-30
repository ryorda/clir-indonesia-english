from gensim.models import Doc2Vec
from gensim.models.doc2vec import LabeledSentence
from nltk.tokenize import WhitespaceTokenizer
import sys
import re
import os
from multiprocessing import Pool
from nltk.stem.porter import *
from nltk.corpus import stopwords
import string
from multiprocessing import Pool

mode = int(sys.argv[1])

def create_model(en_doc, size, window, mode) :
	print('creating model_en_test_s' + str(size) + "_w" + str(window) + "_v" + str(mode)  + "...")
	model_en = Doc2Vec(en_doc, size=size, window=window, dm=0, dbow_words=1, min_count=5, workers=4)
	model_en.save('model/doc_query/model_paralel_s' + str(size) + "_w" + str(window) + "_v" + str(mode) + ".doc2vec")


doc_id = 0
documents = []
for d in os.listdir('dataset/doc_query/clean/en_id/{0}/'.format(mode)) :
	doc_id += 1
	words = []
	f = open('dataset/doc_query/clean/en_id/{0}/{1}'.format(mode, d), encoding='utf-8', errors='ignore')
	for line in f:
		words += line.strip().split()
	documents.append(LabeledSentence(words=words, tags=['pardoc_' + str(doc_id)]))


print("docs : %d" % len(documents))

# pool = Pool(int(sys.argv[2]))

# args = []
for size in [100, 200, 300, 400] :
	for window in [1, 3, 5, 7] :
		# args.append((en_doc, size, window, mode))
		create_model(documents, size, window, mode)

# pool.starmap(create_model, args)