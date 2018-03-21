import xml.etree.ElementTree as ET
from nltk.tokenize import TweetTokenizer
import sys
from nltk.stem.porter import *
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from nltk.corpus import stopwords

tree_gv 	= ET.parse('dataset/GlobalVoice-en-id.tmx')
root 			= tree_gv.getroot()
tokenizer = TweetTokenizer()

file_writer = {
	"en" : open('dataset/GV-en_tokenized%s.txt' % sys.argv[1], 'w', encoding='utf-8'),
	"id" : open('dataset/GV-id_tokenized%s.txt' % sys.argv[1], 'w', encoding='utf-8')	
}

factory = StemmerFactory()
stemmer = {
	"en" : PorterStemmer(),
	"id" : factory.create_stemmer()	
}

sw = {
	"en" : set(stopwords.words('english')),
	"id" : set(stopwords.words('indonesian'))
}

if (sys.argv[1]) == '1' :
	# remove punctuation
	for tuv in root.iter('tuv'):
		text 	= tuv.find('seg').text.strip()
		token = tokenizer.tokenize(text.lower())
		text 	= ""

		for t in token :
			if (t not in [".", ",", ";", ":", "!", "?", "'", "\"", "-", "“", "”", "″", "(", ")", "[", "]", "{", "}", "/", "\\"]) :
				text += " " + t

		text 	= text.strip()
		file_writer[tuv.get('lang')].write( text + "\n")


	for k, f in file_writer.items() : 
		f.close();

elif (sys.argv[1]) == '2' :
	# include punctuation
	for tuv in root.iter('tuv'):
		text 	= tuv.find('seg').text.strip()
		token = tokenizer.tokenize(text.lower())
		text 	= ""

		for t in token :
			text += " " + t

		text 	= text.strip()
		file_writer[tuv.get('lang')].write( text + "\n")


	for k, f in file_writer.items() : 
		f.close();

elif (sys.argv[1]) == '3' :
	# remove stopwords
	idx = 0
	for tuv in root.iter('tuv'):
		idx += 1
		text 	= tuv.find('seg').text.strip().lower()
		token = tokenizer.tokenize(text)
		text 	= ""

		for t in token :
			if t not in sw[tuv.get('lang')] :
				text += " " + t

		text 	= text.strip()
		file_writer[tuv.get('lang')].write( text + "\n")

	for k, f in file_writer.items() : 
		f.close();

elif (sys.argv[1]) == '4' :
	# stemming and remove stopwords
	idx = 0
	for tuv in root.iter('tuv'):
		idx += 1
		text 	= tuv.find('seg').text.strip().lower()
		token = tokenizer.tokenize(text)
		text 	= ""

		st = stemmer[tuv.get('lang')]

		for t in token :
			if t not in sw[tuv.get('lang')] :
				text += " " + st.stem(t)

		text 	= text.strip()
		file_writer[tuv.get('lang')].write( text + "\n")

		print('stem ' + str(idx))

	for k, f in file_writer.items() : 
		f.close();



