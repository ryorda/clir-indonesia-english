from gensim.models import keyedvectors
from gensim.models import Doc2Vec
import re 
import os
import Queries
from multiprocessing import Pool
import sys
from nltk.tokenize import TweetTokenizer

def test(size, window, unique_docs_set) :

	tokenizer = TweetTokenizer()

	regex_docno = re.compile('<DOCNO>.*?</DOCNO>', re.M)
	regex_docno2 = re.compile('</?DOCNO>')

	prefix = 'model_bilingual_mono_'

	news = ['GH95', 'LAT94']
	regex_news = [None, re.compile('la[0-9]+')]

	print('load ' + prefix + str(size) + "_" + str(window) + "_v%s" % sys.argv[1] + "...")
	model = Doc2Vec.load('model/' + prefix + str(size) + "_" + str(window) + "_v%s" % sys.argv[1] + ".doc2vec")
	
	# sim = Doc2Vec.cosine_similarities(vec1, [vec2])
	
	result_title = open('result/' + prefix + str(size) + "_" + str(window) + "_v%s" % sys.argv[1] + "_title" + ".txt", 'w', 1, encoding='utf-8')
	result_desc = open('result/' + prefix + str(size) + "_" + str(window) + "_v%s" % sys.argv[1] + "_desc" + ".txt", 'w', 1, encoding='utf-8')
	result_narr = open('result/' + prefix + str(size) + "_" + str(window) + "_v%s" % sys.argv[1] + "_narr" + ".txt", 'w', 1, encoding='utf-8')

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
							docno = regex_docno.search(doc).group(0)
							docno = regex_docno2.sub('', docno.strip()).strip()

							if docno in unique_docs_set :
								print(prefix + str(size) + "_" + str(window) + "_v%s" % sys.argv[1] + '  ' + docno)
								sim_title = model.wmdistance(' '.join(tokenizer.tokenize(queries.title.strip().lower())), doc)
								sim_desc = model.wmdistance(' '.join(tokenizer.tokenize(queries.desc.strip().lower())), doc)
								sim_narr = model.wmdistance(' '.join(tokenizer.tokenize(queries.narr.strip().lower())), doc)

								result_title.write(str(idx) + ' ' + docno + ' ' + str(sim_title) + '\n')
								result_desc.write(str(idx) + ' ' + docno + ' ' + str(sim_desc) + '\n')
								result_narr.write(str(idx) + ' ' + docno + ' ' + str(sim_narr) + '\n')

							else :
								print(docno + ' doesn\'t exist on rel judgement')
						elif '<DOCNO>' in line :
							doc += '\n' + line.strip()	
						else :
							doc += '\n' + ' '.join(tokenizer.tokenize(line.strip().lower()))


unique_docs_set = set()
unique_docs = open('unique_docs.txt', 'r')
for w in unique_docs :
	unique_docs_set.add(w)

pairs = []
for size in [100, 200, 300, 400] :
	for window in [3, 5, 7, 9] :
		pairs.append((size, window, unique_docs_set))

pool = Pool(processes=int(sys.argv[2]))  
pool.starmap(test, pairs)

		