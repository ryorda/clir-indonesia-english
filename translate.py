import sys
import re
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.parse import quote_plus
import json

google_translate = 'https://translate.google.com/'
oxford_translate_en_id = 'https://id.oxforddictionaries.com/terjemahkan/inggris-indonesia/'
oxford_translate_id_en = 'https://id.oxforddictionaries.com/terjemahkan/indonesia-inggris/'
yandex_translate = 'https://translate.yandex.net/api/v1.5/tr.json/translate?key=trnsl.1.1.20170514T113308Z.dc0360943fce4c7a.beca61b6d2d33fb4f71805c46661196557e6014e'

regex_hint = re.compile(r'\(.*\)')

def translate_oxford(schema, word) :
	oxford_translate = oxford_translate_id_en if schema == 'id-en' else oxford_translate_en_id
	url = oxford_translate + quote_plus(word)
	html = urlopen(url).read()
	soup = BeautifulSoup(html, "html.parser")

	# print('word : %s' % word.encode('ascii', errors='ignore').decode('ascii', errors='ignore'))
	head_word = soup.find_all(class_='translated_headword')

	if (len(head_word) == 0) :
		return []

	main_translate =  regex_hint.sub('', head_word[0].get_text()).strip()
	result = [ main_translate ]
	
	for label in soup.find_all(class_='spanish_label') :
		text = label.get_text()
		text = regex_hint.sub('', text)
		for t in text.split(",") :
			result.append(t.strip())
	
	# print('result : %s' % ",".join(result).encode('ascii', errors='ignore').decode('ascii', errors='ignore'))
	return result

def translate_yandex(schema, word) :
	
	url = yandex_translate + '&lang=%s&text=%s' % (schema , quote_plus(word))
	jsonres = urlopen(url).read().decode('utf-8')
	
	res = json.loads(jsonres)
	result = res['text']
	
	return result

if __name__ == '__main__' :
	# print(translate_yandex(sys.argv[1], sys.argv[2]))
	pass
