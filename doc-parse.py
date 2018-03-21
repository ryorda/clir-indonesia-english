import xml.etree.ElementTree as ET
from nltk.tokenize import TweetTokenizer

tree_gv 	= ET.parse('../dataset/GlobalVoice-en-id.tmx')
root 			= tree_gv.getroot()
tokenizer = TweetTokenizer()

file_writer = {
	"en" : open('../dataset/GV-en_tokenized%d.txt' % sys.argv[0], 'w'),
	"id" : open('../dataset/GV-id_tokenized%d.txt' % sys.argv[0], 'w')	
}


if (sys.argv[0]) == 1 :
	# remove punctuation
	for tuv in root.iter('tuv'):
		text 	= tuv.find('seg').text.strip()
		token = tokenizer.tokenize(text)
		text 	= ""

		for t in token :
			if (t not in [".", ",", ";", ":", "!", "?", "'", "\"", "-", "“", "”", "″", "(", ")", "[", "]", "{", "}", "/", "\\"]) :
				text += " " + t

		text 	= text.strip()
		file_writer[tuv.get('lang')].write( text + "\n")


	for k, f in file_writer.items() : 
		f.close();

elif (sys.argv[0]) == 2 :
	# include punctuation
	for tuv in root.iter('tuv'):
		text 	= tuv.find('seg').text.strip()
		token = tokenizer.tokenize(text)
		text 	= ""

		for t in token :
			text += " " + t

		text 	= text.strip()
		file_writer[tuv.get('lang')].write( text + "\n")


	for k, f in file_writer.items() : 
		f.close();



