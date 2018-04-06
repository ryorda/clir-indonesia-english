import sys
import re
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.parse import quote_plus

google_translate = 'https://translate.google.com/'
oxford_translate_en_id = 'https://id.oxforddictionaries.com/terjemahkan/inggris-indonesia/'
oxford_translate_id_en = 'https://id.oxforddictionaries.com/terjemahkan/indonesia-inggris/'

regex_hint = re.compile(r'\(.*\)')

def translate(schema, word) :
	oxford_translate = oxford_translate_id_en if schema == 'id_en' else oxford_translate_en_id
	url = oxford_translate + quote_plus(word)
	html = urlopen(url).read()
	soup = BeautifulSoup(html)

	print('word : %s' % word)
	head_word = soup.find_all(class_='translated_headword')

	if (len(head_word) == 0) :
		return []

	result = [ soup.find_all(class_='translated_headword')[0].get_text() ]
	
	for label in soup.find_all(class_='spanish_label') :
		text = label.get_text()
		text = regex_hint.sub('', text)
		for t in text.split(",") :
			result.append(t.strip())
	
	print('result : %s' % ",".join(result))
	return result

if __name__ == '__main__' :
	print(translate(sys.argv[1], sys.argv[2]))
