import xml.etree.ElementTree as ET
from nltk.tokenize import TweetTokenizer
import sys
from nltk.stem.porter import *
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from nltk.corpus import stopwords
import string
import os

factory = StemmerFactory()
stemmer = [ factory.create_stemmer(), PorterStemmer() ]
sw = [ set(stopwords.words('indonesian')), set(stopwords.words('english'))]

re_clean = re.compile(r'[^A-Za-z0-9]', re.M)

mode = int(sys.argv[1])

print('running with mode %d' % mode)
# lowercase
if mode == 1 : 
	for d in os.listdir('dataset/GlobalVoices/extracted_raw/en_id') :
		fout = open('dataset/doc_query/clean/en_id/{0}/{1}'.format(mode, d), 'w', encoding='utf-8')
		f = open('dataset/GlobalVoices/extracted_raw/en_id/{0}'.format(d), 'r', encoding='utf-8')
		for line in f :
			text = line.strip().lower()
			fout.write(text + "\n")
		f.close()
		fout.close()

#lowercase + convert all non-alphanumeric to space
elif mode == 2 :
	for d in os.listdir('dataset/GlobalVoices/extracted_raw/en_id') :
		fout = open('dataset/doc_query/clean/en_id/{0}/{1}'.format(mode, d), 'w', encoding='utf-8')
		f = open('dataset/GlobalVoices/extracted_raw/en_id/{0}'.format(d), 'r', encoding='utf-8')
		for line in f :
			text = line.strip().lower()
			text = re_clean.sub(' ', text)
			fout.write(text + "\n")
		f.close()
		fout.close()

#lowercase + convert all non-alphanumeric to space + remove stopwords
elif mode == 3 :

	for d in os.listdir('dataset/GlobalVoices/extracted_raw/en_id') :
		idx = 0 # first is id, then if we found blank become english
		fout = open('dataset/doc_query/clean/en_id/{0}/{1}'.format(mode, d), 'w', encoding='utf-8')
		f = open('dataset/GlobalVoices/extracted_raw/en_id/{0}'.format(d), 'r', encoding='utf-8')
		for line in f :
			text = line.strip().lower()
			if not text :
				idx += 1
				fout.write("\n")
				continue
			text = re_clean.sub(' ', text)
			tokens = text.split()
			text = []
			for t in tokens :
				if t not in sw[idx] :
					text.append(t)
			text = " ".join(text)
			fout.write(text + "\n")
		f.close()
		fout.close()

#lowercase + convert all non-alphanumeric to space + stemmed
elif mode == 4 :

	for d in os.listdir('dataset/GlobalVoices/extracted_raw/en_id') :
		idx = 0 # first is id, then if we found blank become english
		fout = open('dataset/doc_query/clean/en_id/{0}/{1}'.format(mode, d), 'w', encoding='utf-8')
		f = open('dataset/GlobalVoices/extracted_raw/en_id/{0}'.format(d), 'r', encoding='utf-8')
		for line in f :
			if not line :
				idx += 1
				fout.write("\n")
				continue
			text = line.strip().lower()
			text = re_clean.sub(' ', text)
			tokens = text.split()
			text = []
			for t in tokens :
				t2 = stemmer[idx].stem(t)
				text.append(t2)
			text = " ".join(text)
			fout.write(text + "\n")
		f.close()
		fout.close()
else :
	print("[ERROR] mode is invalid...")
	exit()

