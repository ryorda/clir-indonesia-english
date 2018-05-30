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

tokenizer = WhitespaceTokenizer()

version = sys.argv[1]

en_doc = open('dataset/GV-en_tokenized%s.txt' % version, 'r', encoding='utf-8')
id_doc = open('dataset/GV-id_tokenized%s.txt' % version, 'r', encoding='utf-8')


def create_model(en_sentences, size, window, version) :
	print('creating model_en_test_s' + str(size) + "_w" + str(window) + "_v" + str(version)  + "...")
	model_en = Doc2Vec(en_sentences, size=size, window=window, dm=0, dbow_words=1, min_count=5, workers=4)
	model_en.save('model/model_en_test_s' + str(size) + "_w" + str(window) + "_v" + str(version) + ".doc2vec")

# add test case

news = ['GH95', 'LAT94']
regex_news = [None, re.compile('la[0-9]+')]
regex_docno = re.compile('<DOCNO>.*?</DOCNO>', re.M)
regex_docno2 = re.compile('</?DOCNO>')

en_sentences = []
en_stemmer = PorterStemmer()
en_stops = set(stopwords.words('english'))

for i in range(len(news)) :
	for d in os.listdir('news/%s/' % news[i]) :
		if (regex_news[i] is None or regex_news[i].match(d)) :
			f = open(os.path.abspath(('news/%s/' % news[i]) + d), 'r', encoding="latin-1", errors='ignore')
			intext = False
			doc = ''
			docno = ''
			for line in f :
				if '<DOC>' in line :
					doc = []
				elif '<DOCNO>' in line :
					docno = regex_docno2.sub('', line.strip()).strip()
				elif '</DOC>' in line :
					en_sentences.append(LabeledSentence(words=doc, tags=['news_' + docno]))
				else :
					text = line.strip().lower()
					text = text.replace("'s"," ")
					text = text.replace("'"," ")
					text = text.replace("-", " ")
					translator = str.maketrans('', '', string.punctuation)
					text = text.translate(translator)
					doc += [en_stemmer.stem(word) for word in text.split() if word not in en_stops]

id_sentences = []

print("sentences : %d" % len(en_sentences))
idx = 0
for line in zip(en_doc, id_doc) :
	text = line[0].strip().lower()
	text = text.replace("'s"," ")
	text = text.replace("'"," ")
	text = text.replace("-", " ")
	translator = str.maketrans('', '', string.punctuation)
	text = text.translate(translator)
	en_tokens = [en_stemmer.stem(word) for word in text.split() if word not in en_stops]

	# en_tokens = tokenizer.tokenize(line[0].strip())
	# id_tokens = tokenizer.tokenize(line[1].strip())

	en_sentences.append(LabeledSentence(words=en_tokens, tags=['en_mono_' + str(idx)]))
	# id_sentences.append(LabeledSentence(words=id_tokens, tags=['id_mono_' + str(idx)]))
	idx += 1

print("sentences : %d" % len(en_sentences))


args = []
for size in [100, 200, 300, 400] :
	for window in [1, 3, 5, 7] :
			# args.append((en_sentences, size, window, version))
		create_model(en_sentences, size, window, version)