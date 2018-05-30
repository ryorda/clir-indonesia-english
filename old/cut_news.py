from gensim.models import keyedvectors
from gensim.models import Doc2Vec
import re 
import os
import Queries
from multiprocessing import Pool
import sys
from nltk.tokenize import TweetTokenizer

def test(unique_docs_set) :

	tokenizer = TweetTokenizer()

	regex_docno = re.compile('<DOCNO>.*?</DOCNO>', re.M)
	regex_docno2 = re.compile('</?DOCNO>')

	prefix = 'model_bilingual_mono_'

	news = ['GH95', 'LAT94']
	regex_news = [None, re.compile('la[0-9]+')]

	print("cut news...")


	for i in range(len(news)) :
		for d in os.listdir('news/%s/' % news[i]) :
			if (regex_news[i] is None or regex_news[i].match(d)) :
				print('write %s ...' % d)
				f = open(os.path.abspath(('news/%s/' % news[i]) + d), 'r', encoding="latin-1", errors='ignore')
				fnew = open(os.path.abspath(('news-cut/%s/' % news[i]) + d), 'w', encoding="latin-1", errors='ignore')
				doc = ''
				docno = ''
				for line in f :
					if '<DOC>' in line :
						doc = '<DOC>'
					elif '</DOC>' in line :
						docno = regex_docno.search(doc).group(0)
						docno = regex_docno2.sub('', docno.strip()).strip()

						if docno in unique_docs_set :
							fnew.write(doc + '\n</DOC>\n')

					elif '<DOCNO>' in line :
						doc += '\n' + line.strip()	
					else :
						doc += '\n' + ' '.join(tokenizer.tokenize(line.strip().lower()))


unique_docs_set = set()
unique_docs = open('unique_docs.txt', 'r')
for w in unique_docs :
	unique_docs_set.add(w.strip())

print(len(unique_docs_set))
test(unique_docs_set)