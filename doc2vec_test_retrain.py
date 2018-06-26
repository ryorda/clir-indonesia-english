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


en_doc = []
en_stemmer = PorterStemmer()
en_stops = set(stopwords.words('english'))

size = int(sys.argv[1])
window = int(sys.argv[2])
min_count = int(sys.argv[3])
mode = int(sys.argv[4])
max_epoch = int(sys.argv[5])
save_per_epoch = int(sys.argv[6])

# def create_model(size, window, mode, min_count) :
def train_model(en_doc, size, window, mode, min_count) :
	print('retrain model_en_test_s' + str(size) + "_w" + str(window) + "_c" + str(min_count) + "_v" + str(mode)  + "...", flush=True)
	model_en = Doc2Vec.load('model/doc_query/model_en_test_s%d_w%d_c%d_v%d.doc2vec' % (size, window, min_count, mode))
	for i in range(1, max_epoch+1) :
		model_en.train(en_doc.sentences_perm())
		if i % save_per_epoch == 0 :
			model_en.save('model/doc_query/model_en_test_s' + str(size) + "_w" + str(window) + "_c" + str(min_count) + "_v" + str(mode) +  "_i" + str(i) + ".doc2vec")
	model_en.save('model/doc_query/model_en_test_s' + str(size) + "_w" + str(window) + "_c" + str(min_count) + "_v" + str(mode) +  "_i" + str(max_epoch) + ".doc2vec")

# add test case

news = ['GH95', 'LAT94']
regex_news = [None, re.compile('la[0-9]+')]
regex_docno = re.compile('<DOCNO>.*?</DOCNO>', re.M)
regex_docno2 = re.compile('</?DOCNO>')

re_clean = re.compile(r'[^A-Za-z0-9]', re.M)

for i in range(len(news)) :
	for d in os.listdir('news/%s/' % news[i]) :
		if (regex_news[i] is None or regex_news[i].match(d)) :
			f = open(os.path.abspath(('news/%s/' % news[i]) + d), 'r', encoding="latin-1", errors='ignore')
			
			words = []

			docno = ''
			for line in f :
				if '<DOC>' in line :
					words = []
				elif '<DOCNO>' in line :
					docno = regex_docno2.sub('', line.strip()).strip()
				elif '</DOC>' in line :
					for mode in [1, 2, 3, 4, 5] :
						en_doc.append(LabeledSentence(words=words, tags=['news_' + docno]))
				else :
					text = line.strip().lower()
					if mode == 1 :
						words += text.split()
					elif mode == 2 :
						text = re_clean.sub(' ', text)
						words += text.split()
					elif mode == 3 :
						text = re_clean.sub(' ', text)
						tokens = text.split()
						text = []
						for t in tokens :
							if t not in en_stops :
								text.append(t)
						words += text
					elif mode == 4 :
						text = re_clean.sub(' ', text)
						tokens = text.split()
						text = []
						for t in tokens :
							text.append(en_stemmer.stem(t))
						words += text
					elif mode == 5 :
						text = re_clean.sub(' ', text)
						tokens = text.split()
						text = []
						for t in tokens :
							if t not in en_stops :
								text.append(en_stemmer.stem(t))
						words += text
							
					else :
						print("[ERROR] invalid mode number", flush=True)
						exit()


print("docs : %d" % len(en_doc) , flush=True)	

# pool = Pool(int(sys.argv[2]))

# for size in [100, 200, 300, 400] :
# 	for window in [1, 3, 5, 7] :
# 		for min_count in [1, 5, 10, 20, 50] :
# 			m = mode
			# args.append((size, window, mode, min_count))
create_model(en_doc[mode], size, window, m, min_count)

# pool.starmap(create_model, args)