import gzip
import os
import re
from bs4 import BeautifulSoup
from urllib.request import urlopen
import sys

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

dataset = sys.argv[1]

list_doc = open('dataset/{0}/en-id.txt/{0}.en-id.ids'.format(dataset), 'r', encoding='utf-8')
for d in list_doc:
	id_doc = d.strip().split("\t")[1].split('/')[1]
	id_docs.add(id_doc)
	en_doc = d.strip().split("\t")[0].split('/')[1]
	en_docs.add(en_doc)
	doc_pairs.add(en_doc + ":" + id_doc)

print('num of docs : %d' % len(id_docs))
print('num of docs : %d' % len(en_docs))

regex_url = re.compile('<URL>(.*)</URL>', re.M)
regex_newline = re.compile(r'[\r\n]+', re.M)
regex_empty = re.compile(r'$^[\n\r]+', re.M)

if dataset == 'GlobalVoices' :
	# os.chdir(os.path.join(cwd, 'dataset/{0}/raw/id'.format(dataset)))
	for d in os.listdir('dataset/{0}/raw/id'.format(dataset)) :
		if d in id_docs :
			print('dataset/{0}/raw/id/{1}'.format(dataset, d))
			fout = open('dataset/{0}/extracted_raw/id/{1}.raw'.format(dataset, d.strip().split('.')[0]), 'w', encoding='utf-8')
			with open('dataset/{0}/raw/id/{1}'.format(dataset, d), 'rb') as f:
				extract(f, fout)
			fout.close()

	# os.chdir(os.path.join(cwd, 'dataset/{0}/raw/en'))
	for d in os.listdir('dataset/{0}/raw/en'.format(dataset)) :
		if d in en_docs :
			print('dataset/{0}/raw/en/{1}'.format(dataset, d))
			fout = open('dataset/{0}/extracted_raw/en/{1}.raw'.format(dataset, d.strip().split('.')[0]), 'w', encoding='utf-8')
			with open('dataset/{0}/raw/en/{1}'.format(dataset, d), 'rb') as f:
				extract(f, fout)
			fout.close()


# merge en and id
for d in doc_pairs :
	id_doc = d.split(":")[1]
	id_doc = id_doc.strip().split('.')[0]
	en_doc = d.split(":")[0]
	en_doc = en_doc.strip().split('.')[0]

	doc_name = en_doc

	print('dataset/{0}/raw/en_id/{1}'.format(dataset, doc_name))
	fout = open('dataset/{0}/extracted_raw/en_id/{1}.raw'.format(dataset, doc_name), 'w', encoding='utf-8')
	
	f = open('dataset/{0}/extracted_raw/id/{1}.raw'.format(dataset, id_doc), 'r', encoding='utf-8')
	for line in f :
		fout.write(line.strip())
		fout.write("\n")
	fout.write("\n")

	f = open('dataset/{0}/extracted_raw/en/{1}.raw'.format(dataset, en_doc), 'r', encoding='utf-8')
	for line in f :
		fout.write(line.strip())
		fout.write("\n")

	fout.close()
