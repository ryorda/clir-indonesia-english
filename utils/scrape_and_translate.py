import sys
import psycopg2
import json
import re
import yandex
try:
    con = psycopg2.connect("dbname='medscrape' user='qorib' host='localhost' password='qorib'")
    cur = con.cursor()
except:
    print("Unable to connect to the database")

print("connected to the database")

table_name = sys.argv[1]
source = sys.argv[2]

query = """SELECT * FROM {0} WHERE url LIKE '%{1}%' AND char_length(content) < 9000;""".format(table_name, source)
data = []

cur.execute(query)


# 0 : id
# 1 : url
# 2 : content
# 3 : category
# 4 : title

re_dot = re.compile(r'\.', re.M)
re_clean = re.compile(r'[^A-Za-z0-9]', re.M)
re_blank = re.compile(r'\n\n*\s*\n', re.M)

translater = yandex.Translater()
tr.set_key('trnsl.1.1.20170514T113308Z.dc0360943fce4c7a.beca61b6d2d33fb4f71805c46661196557e6014e')
tr.set_from_lang('en')
tr.set_to_lang('id')


for record in cur :
	content = re_blank.sub('\n', record[2])
	
	fout_id = open('dataset/{0}/extracted_raw/id/{1}.raw'.format(source, record[4]), 'w', encoding='utf-8')
	fout_en = open('dataset/{0}/extracted_raw/en/{1}.raw'.format(source, record[4]), 'w', encoding='utf-8')
	
	fout_id.write(content)
	fout_id.write("\n")
	
	tr.set_text(content)
	tr_content = tr.translate()
	
	fout_en.write(tr_content)
	fout_en.write("\n")