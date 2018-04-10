import xml.etree.ElementTree as ET
from nltk.tokenize import TweetTokenizer
import sys
from nltk.stem.porter import *
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from nltk.corpus import stopwords
import translate as tr
import time
from multiprocessing import Pool

tree_gv 	= ET.parse('dataset/GlobalVoice-en-id.tmx')
root 			= tree_gv.getroot()
tokenizer = TweetTokenizer()

factory = StemmerFactory()
stemmer = {
	"en" : PorterStemmer(),
	"id" : factory.create_stemmer()	
}

file_writer = {
	"oxford": {
		"en" : open('dataset/dictionary-en_id.oxford.txt', 'w', encoding='utf-8'),
		"id" : open('dataset/dictionary-id_en.oxford.txt', 'w', encoding='utf-8')	
	},
	"yandex": {
		"en" : open('dataset/dictionary-en_id.yandex.txt', 'w', encoding='utf-8'),
		"id" : open('dataset/dictionary-id_en.yandex.txt', 'w', encoding='utf-8')	
	}
}

word_collections = {
	"en" : set(),
	"id" : set()	
}

def func_translate(args) :
	global word_collections
	global file_writer
	global stemmer

	t = args[0]
	lang = args[1]
	schema = 'en-id' if lang == 'en' else 'id-en'
	st = stemmer[lang]

	t = t.strip()
	if t not in word_collections[lang] :
		word_collections[lang].add(t)
		try :
			res_yandex = tr.translate_yandex(schema, t)
			file_writer['yandex'][lang].write(t + '\t'+ ",".join(res_yandex) + '\n')
		except Exception as e :
			print(e)

		try :
			res_oxford = tr.translate_oxford(schema, t)
			file_writer['oxford'][lang].write(t + '\t'+ ",".join(res_oxford) + '\n')
		except Exception as e :
			print(e)
	
	t2 = st.stem(t)
	if t2 not in word_collections[lang] :
		word_collections[lang].add(t2)
		try :
			# res_oxford = tr.translate_oxford(schema, t2)
			# file_writer['oxford'][lang].write(t2 + '\t'+ ",".join(res_oxford) + '\n')
		except Exception as e :
			print(e)

		try :
			res_yandex = tr.translate_yandex(schema, t2)
			file_writer['yandex'][lang].write(t2 + '\t'+ ",".join(res_yandex) + '\n')
		except Exception as e :
			print(e)

	file_writer['oxford'][lang].flush()
	file_writer['yandex'][lang].flush()

def main() :
	pool = Pool(processes=int(sys.argv[1]))  
	# include punctuation
	for tuv in root.iter('tuv'):
		text 	= tuv.find('seg').text.strip()
		# print("translating '%s' ..." % text.encode('utf-8', errors='ignore').decode('utf-8', errors='ignore'))
		token = tokenizer.tokenize(text.lower())	
		args = []
		lang = tuv.get('lang')

		for t in token :
			args.append((t, lang))

		# start = time.time()
		try :
			pool.map(func_translate, args)
		except Exception as e:
			print(e)
		# print('exec %f secs' % start - time.time())
		# sys.exit()


	for k, f in file_writer.items() : 
		f.close();

if __name__ == '__main__' :
	main()