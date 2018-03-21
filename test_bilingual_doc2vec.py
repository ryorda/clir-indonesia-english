from gensim.models import keyedvectors
from gensim.models import Doc2Vec
import re 
import os
import Queries
from multiprocessing import Pool
import sys
from nltk.tokenize import WhitespaceTokenizer

def test(size, window) :

	tokenizer = WhitespaceTokenizer()

	regex_docno = re.compile('<DOCNO>.*?</DOCNO>', re.M)
	regex_docno2 = re.compile('</?DOCNO>')

	prefix = 'model_bilingual_mono_'

	news = ['GH95', 'LAT94']
	regex_news = [None, re.compile('la[0-9]+')]

	print('load ' + prefix + str(size) + "_" + str(window) + "...")
	model = Doc2Vec.load('model/' + prefix + str(size) + "_" + str(window) + ".doc2vec")
	
	# sim = Doc2Vec.cosine_similarities(vec1, [vec2])
	
	result_title = open('result/' + prefix + str(size) + "_" + str(window) + "_title" + ".txt", 'w', 1)
	result_desc = open('result/' + prefix + str(size) + "_" + str(window) + "_desc" + ".txt", 'w', 1)
	result_narr = open('result/' + prefix + str(size) + "_" + str(window) + "_narr" + ".txt", 'w', 1)

	queries = Queries.Queries()
	idx = -1
	while queries.hasnext() :
		queries.next()
		idx += 1
		
		for i in range(len(news)) :
			for d in os.listdir('news/%s/' % news[i]) :
				if (regex_news[i] is None or regex_news[i].match(d)) :
					f = open(os.path.abspath(('news/%s/' % news[i]) + d), 'r', encoding="latin-1", errors='ignore')
					doc = ''
					docno = ''
					for line in f :
						if '<DOC>' in line :
							doc = ''
						elif '</DOC>' in line :
							sim_title = model.wmdistance(queries.title, doc)
							sim_desc = model.wmdistance(queries.desc, doc)
							sim_narr = model.wmdistance(queries.narr, doc)

							docno = regex_docno.search(doc).group(0)
							docno = regex_docno2.sub('', docno.strip()).strip()
							print(prefix + str(size) + "_" + str(window) + '  ' + docno)

							result_title.write(str(idx) + ' ' + docno + ' ' + str(sim_title) + '\n')
							result_desc.write(str(idx) + ' ' + docno + ' ' + str(sim_desc) + '\n')
							result_narr.write(str(idx) + ' ' + docno + ' ' + str(sim_narr) + '\n')

						else :
							doc += '\n' + line.strip()





pairs = []
for size in [100, 200, 300, 400] :
	for window in [3, 5, 7, 9] :
		pairs.append((size, window))

pool = Pool(processes=int(sys.argv[1]))  
pool.starmap(test, pairs)

		