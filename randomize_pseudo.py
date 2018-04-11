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
import numpy as np
import copy

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
		return json.load(open('%s.dict' % schema, 'r', encoding='utf-8'))

	res = {}
	if schema == 'en-id' :
		f = open('dataset/dictionary-en_id.txt', 'r', encoding='utf-8')
	elif  schema == 'id-en' :
		f = open('dataset/dictionary-id_en.txt', 'r', encoding='utf-8')
	else :
		return {}

	for line in f :
		sp = line.strip().split("\t")
		k = sp[0]
		v = set(sp[1].split(",")) if len(sp) > 1 else set()

		words = list(v)
		for w in  words:
			v.add(stemmer.stem(w))

		res[k] = list(v)
		# print("translate : %s" % k)
		# print(" ".join(v))

	print(json.dumps(res), file=open('%s.dict' % schema, 'w', encoding='utf-8'))
	return res

dictionary_from = {
	"id" : get_dictionary("id-en", stemmer['en']),
	"en" : get_dictionary("en-id", stemmer['id'])
} 

fout = open('dataset/GV-id_en_tokenized.txt', 'w', encoding='utf-8')

def random_pseudo(docpair) :
	
	doc = {
		"id" : docpair[0],
		"en" : docpair[1]
		}

	langs = ["id", "en"]
	i = 0
	for l in range(len(langs)) :
		lang = langs[l]
		s = doc[lang]
		t = doc[langs[1 - l]]

		length = len(doc[lang])
		for skip in range(1, length + 1) :
			# use original text
			if skip == length :
				# dataset.append(list(zip(*doc[lang])[0]))
				fout.write(" ".join([x[0] for x in doc[lang]]) + "\n")
			else :
				max_offset = range(length - skip - 1) if skip < length - 1 else range(length)
				for offset in max_offset :
					idx = offset
					words = copy.deepcopy(s)
					while idx < length :
						term = words[idx][0]

						## ori but ordered using stem
						if sys.argv[2] == 'ori' :
							term_stem = stemmer[lang].stem(term)
						term_count = words[idx][1]

						checker = None 

						## ori but ordered using stem
						if sys.argv[2] == 'ori' :
							checker = term in dictionary_from[lang] or term_stem in dictionary_from[lang]
						## using stemmed
						elif sys.argv[2] == 'stemmed' :
							checker = term in dictionary_from[lang]

						if checker :
							dic = dictionary_from[lang][term]
							count = 0
							for w in t.copy() :
								checker_target = None
								if sys.argv[2] == 'ori' :
									checker_target = w[0] in dic or stemmer[lang].stem(w[0]) in dic
								elif sys.argv[2] == 'stemmed' :
									checker_target = w[0] in dic

								if checker_target :
									count += 1
								if count == term_count :
									words[idx][0] = w[0]
									break
						idx += skip + 1
					# dataset.append(words)

					fout.write(" ".join([x[0] for x in words]) + "\n")

	fout.flush()

def construct_pseudo( stemmer ) :
	# include punctuation
	sentence_list = {
		"id" : [],
		"en" : []
	}

	sentence_list_doc = None
	if sys.argv[2] == 'ori' :
		sentence_list_doc = 'sentence_ori.list'
	elif sys.argv[2] == 'stemmed' :
		sentence_list_doc = 'sentence_stemmed.list'

	docs = 0
	if os.path.isfile(sentence_list_doc) :
		sentence_list = json.load(open(sentence_list_doc, 'r', encoding='utf-8'))
		docs = len(sentence_list['id'])
	else :
		for tuv in root.iter('tuv'):
			
			print(('reading docs %d...' % docs))

			text 	= tuv.find('seg').text.strip()
			# print("translating '%s' ..." % text.encode('utf-8', errors='ignore').decode('utf-8', errors='ignore'))
			token = tokenizer.tokenize(text.lower())
			lang = tuv.get('lang')

			freq = {}
			word_seq = []
			
			### stemmed 
			if sys.argv[2] == 'stemmed' :
				for t in token :
					t = stemmer[lang].stem(t)
					if t not in freq :
						freq[t] = 0
					freq[t] += 1 
					word_seq.append((t, freq[t]))


			### ori but ordered using stem
			if sys.argv[2] == 'ori' :
				for t in token :
					t_stem = stemmer[lang].stem(t)
					if t_stem not in freq :
						freq[t_stem] = 0
					freq[t_stem] += 1 
					word_seq.append((t, freq[t_stem]))

			sentence_list[lang].append(word_seq)

			docs += 1

		print(json.dumps(sentence_list), file=open(sentence_list_doc, 'w', encoding='utf-8'))
		docs /= 2

	# dataset = []


	pool = Pool(int(sys.argv[1]))
	args = list(zip(sentence_list['id'], sentence_list['en']))
	print(('randomizing %d docs...' % len(args)))

	pool.map(random_pseudo, args)

if __name__ == '__main__' :
	construct_pseudo(stemmer)