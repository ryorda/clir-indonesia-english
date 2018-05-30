import gzip
import os
import re
from bs4 import BeautifulSoup
from urllib.request import urlopen

def extract(f, fout) :
	data = gzip.decompress(f.read()).decode()
	data = regex_url.sub('', data)
	soup = BeautifulSoup(data)

	# for p in soup.find_all('p') :
	text = soup.get_text()
	text = regex_newline.sub('\n', text)
	text = regex_empty.sub('', text)
	fout.write(text+'\n')
	
id_docs = set()
en_docs = set()
doc_pairs = set()

list_doc = open('dataset/GlobalVoices/en-id.txt/GlobalVoices.en-id.ids', 'r', encoding='utf-8')
for d in list_doc:
	id_doc = d.strip().split()[1].split('/')[1]
	id_docs.add(id_doc)
	en_doc = d.strip().split()[0].split('/')[1]
	en_docs.add(en_doc)
	doc_pairs.add(en_doc + ":" + id_doc)

print('num of docs : %d' % len(id_docs))
print('num of docs : %d' % len(en_docs))

regex_url = re.compile('<URL>(.*)</URL>', re.M)
regex_newline = re.compile(r'[\r\n]+', re.M)
regex_empty = re.compile(r'$^[\n\r]+', re.M)


# os.chdir(os.path.join(cwd, 'dataset/GlobalVoices/raw/id'))
for d in os.listdir('dataset/GlobalVoices/raw/id') :
	if d in id_docs :
		print('dataset/GlobalVoices/raw/id/%s' % d)
		fout = open('dataset/GlobalVoices/extracted_raw/id/%s.raw' % d.strip().split('.')[0], 'w', encoding='utf-8')
		with open('dataset/GlobalVoices/raw/id/%s' % d, 'rb', encoding='utf-8') as f:
			extract(f, fout)
		fout.close()

# os.chdir(os.path.join(cwd, 'dataset/GlobalVoices/raw/en'))
for d in os.listdir('dataset/GlobalVoices/raw/en') :
	if d in en_docs :
		print('dataset/GlobalVoices/raw/en/%s' % d)
		fout = open('dataset/GlobalVoices/extracted_raw/en/%s.raw' % d.strip().split('.')[0], 'w', encoding='utf-8')
		with open('dataset/GlobalVoices/raw/en/%s' % d, 'rb', encoding='utf-8') as f:
			extract(f, fout)
		fout.close()


# merge en and id
for d in doc_pairs :
	id_doc = d.split(":")[1]
	en_doc = d.split(":")[0]
	doc_name = en_doc
	print('dataset/GlobalVoices/raw/en_id/%s' % doc_name)
	fout = open('dataset/GlobalVoices/extracted_raw/en_id/%s.raw' % doc_name, 'w', encoding='utf-8')
	with open('dataset/GlobalVoices/raw/id/%s' % id_doc, 'rb', encoding='utf-8') as f:
		extract(f, fout)
	with open('dataset/GlobalVoices/raw/en/%s' % en_doc, 'rb', encoding='utf-8') as f:
		extract(f, fout)
	fout.close()
