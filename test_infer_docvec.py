from gensim.models import keyedvectors
from gensim.models import Doc2Vec
import re 
import os
import Queries
from multiprocessing import Pool
import sys
from nltk.tokenize import TweetTokenizer
import time

def test(size, window) :

	tokenizer = TweetTokenizer()

	regex_docno = re.compile('<DOCNO>.*?</DOCNO>', re.M)
	regex_docno2 = re.compile('</?DOCNO>')

	prefix = 'model_' + str(sys.argv[3])

	news = ['GH95', 'LAT94']
	regex_news = [None, re.compile('la[0-9]+')]

	print('load ' + prefix + "_s" + str(size) + "_w" + str(window) + "_v" + str(sys.argv[1]) + "...")
	model = Doc2Vec.load('model/' + prefix + "_s" + str(size) + "_w" + str(window) + "_v" + str(sys.argv[1]) + ".doc2vec")
	
	fout = open('docvec/vector_' + str(sys.argv[3]) + '_s' + str(size) + "_w" + str(window) + "_v" + str(sys.argv[1]) + ".txt", 'w')

	for i in range(len(news)) :
		for d in os.listdir('news/%s/' % news[i]) :
			if (regex_news[i] is None or regex_news[i].match(d)) :
				f = open(os.path.abspath(('news/%s/' % news[i]) + d), 'r', encoding="latin-1", errors='ignore')
				for line in f :
					if '<DOC>' in line :
						doc = ''
					elif '</DOC>' in line :
						docno = regex_docno.search(doc).group(0)
						docno = regex_docno2.sub('', docno.strip()).strip()

						vector = model.infer_vector(doc)
						fout.write('%s\t%s\n' % (docno, ",".join([str(x) for x in vector])))
						print('docno %s ' % docno)

					elif '<DOCNO>' in line :
						doc += '\n' + line.strip()	
					else :
						doc += '\n' + ' '.join(tokenizer.tokenize(line.strip().lower()))


pairs = []
for size in [100, 200, 300, 400] :
	for window in [1, 3, 5, 7] :
		pairs.append((size, window))

pool = Pool(processes=int(sys.argv[2]))  
pool.starmap(test, pairs)