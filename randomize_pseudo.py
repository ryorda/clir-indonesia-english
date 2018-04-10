import xml.etree.ElementTree as ET
from nltk.tokenize import TweetTokenizer
import sys
from nltk.stem.porter import *
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from nltk.corpus import stopwords
import translate as tr
import time
from multiprocessing import Pool
import json
import os

tree_gv 	= ET.parse('dataset/GlobalVoice-en-id.tmx')
root 			= tree_gv.getroot()
tokenizer = TweetTokenizer()

factory = StemmerFactory()
stemmer = {
	"en" : PorterStemmer(),
	"id" : factory.create_stemmer()	
}


def get_dictionary(schema, stemmer) :

	if os.path.isfile('%s.dict' %  schema) :
		return json.load(open('%s.dict' % schema, 'r'))

	res = {}
	if schema == 'en-id' :
		f = open('dataset/dictionary-en_id.txt', 'r')
	elif  schema == 'id-en' :
		f = open('dataset/dictionary-id_en.txt', 'r')
	else :
		return {}

	for line in f :
		sp = line.strip().split("\t")
		k = sp[0]
		v = sp[1].split(",") if len(sp) > 1 else []

		for w in v.copy() :
			v.append(stemmer.stem(w))

		res[k] = v
		print("translate : %s" % k)
		print(" ".join(v))

	print(json.dumps(res), file=open('%s.dict' % schema, 'w'))
	return res

dictionary_from = {
	"id" : get_dictionary("id-en", stemmer['en']),
	"en" : get_dictionary("en-id", stemmer['id'])
} 

def random_pseudo(args) :
	file = args[0]
	docpair = args[1]
	doc = {
		"id" : docpair[0],
		"en" : docpair[1]
		}

	for l in range(len(langs)) :
		lang = langs[l]
		s = doc[lang]
		t = doc[langs[1 - l]]
		length = len(doc[lang])
		for skip in range(1, length + 1) :
			# use original text
			if skip == length :
				# dataset.append(list(zip(*doc[lang])[0]))
				file.write(" ".join(list(zip(*doc[lang])[0])) + "\n")
			else :
				max_offset = range(length - skip - 1) if skip < length - 1 else range(length)
				for offset in max_offset :
					idx = offset
					words = s.copy()
					while idx < length :
						term = words[idx][0]
						term_count = words[idx][1]
						dic = dictionary_from[lang][term]
						count = 0
						for w in t :
							if w[0] in dic:
								count += 1
							if count == term_count :
								words[idx][0] = w[0]
								break
						idx += skip
					# dataset.append(words)
					file.write(" ".join(words) + "\n")

	file.flush()

def construct_pseudo(dictionary_from, stemmer ) :
	# include punctuation
	sentence_list = {
		"id" : [],
		"en" : []
	}

	docs = 0
	for tuv in root.iter('tuv'):
		
		print(('reading docs %d...' % docs))

		text 	= tuv.find('seg').text.strip()
		# print("translating '%s' ..." % text.encode('utf-8', errors='ignore').decode('utf-8', errors='ignore'))
		token = tokenizer.tokenize(text.lower())
		lang = tuv.get('lang')

		freq = {}
		word_seq = []
		for t in token :
			t = stemmer[lang].stem(t)
			if t not in freq :
				freq[t] = 0
			freq[t] += 1 
			word_seq.append((t, freq[t]))

		sentence_list[lang].append(word_seq)

		docs += 1

	print(('randomizing %d docs...' % docs))
	# dataset = []
	langs = ["id", "en"]
	i = 0

	f = open('GV-id_en_tokenized.txt', 'w')

	pool = Pool(sys.argv[1])
	args = list(zip( np.repeat(f, docs).tolist(), zip(sentence_list['id'], sentence_list['en'])))

	pool.map(random_pseudo, args)

if __name__ == '__main__' :
	construct_pseudo(dictionary_from, stemmer)