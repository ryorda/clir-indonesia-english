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

en_doc = {}
en_stemmer = PorterStemmer()
en_stops = set(stopwords.words('english'))

news = ['GH95', 'LAT94']
regex_news = [None, re.compile('la[0-9]+')]
regex_docno = re.compile('<DOCNO>.*?</DOCNO>', re.M)
regex_docno2 = re.compile('</?DOCNO>')

re_clean = re.compile(r'[^A-Za-z0-9]', re.M)

for mode in [1, 2, 3, 4, 5] :
	en_doc[mode] = []

for i in range(len(news)) :
	for d in os.listdir('news/%s/' % news[i]) :
		if (regex_news[i] is None or regex_news[i].match(d)) :
			print(i, ":", news[i], " - ", d)
			f = open(os.path.abspath(('news/%s/' % news[i]) + d), 'r', encoding="latin-1", errors='ignore')
			
			words = {}
			for mode in [1, 2, 3, 4, 5] :
				words[mode] = []

			docno = ''
			for line in f :
				if '<DOC>' in line :
					words = {}
					for mode in [1, 2, 3, 4, 5] :
						words[mode] = []
				elif '<DOCNO>' in line :
					docno = regex_docno2.sub('', line.strip()).strip()
				elif '</DOC>' in line :
					for mode in [1, 2, 3, 4, 5] :
						fout = open("dataset/doc_query/news/en/{0}/{1}.txt".format(mode, docno), "w", encoding='utf-8')
						fout.write(" ".join(words[mode]))
						fout.flush()
						fout.close()
						en_doc[mode].append(LabeledSentence(words=words[mode], tags=['news_' + docno]))
				else :
					for mode in [1, 2, 3, 4, 5] :
						text = line.strip().lower()
						if mode == 1 :
							words[mode] += text.split()
						elif mode == 2 :
							text = re_clean.sub(' ', text)
							words[mode] += text.split()
						elif mode == 3 :
							text = re_clean.sub(' ', text)
							tokens = text.split()
							text = []
							for t in tokens :
								if t not in en_stops :
									text.append(t)
							words[mode] += text
						elif mode == 4 :
							text = re_clean.sub(' ', text)
							tokens = text.split()
							text = []
							for t in tokens :
								text.append(en_stemmer.stem(t))
							words[mode] += text
						elif mode == 5 :
							text = re_clean.sub(' ', text)
							tokens = text.split()
							text = []
							for t in tokens :
								if t not in en_stops :
									text.append(en_stemmer.stem(t))
							words[mode] += text
							
						else :
							print("[ERROR] invalid mode number", flush=True)
							exit()


print("docs : %d" % len(en_doc) , flush=True)	