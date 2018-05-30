import tensorflow as tf
from gensim.models import Word2Vec
from nltk.tokenize import WhitespaceTokenizer
import sys
import os
import json

from nltk.stem.porter import *
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

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
		v = sp[1].split(",") if len(sp) > 1 else []

		for w in v.copy() :
			v.append(stemmer.stem(w))

		res[k] = v

	print(json.dumps(res), file=open('%s.dict' % schema, 'w', encoding='utf-8'))
	return res

dictionary_from = {
	"id" : get_dictionary("id-en", stemmer['en']),
	"en" : get_dictionary("en-id", stemmer['id'])
} 

words = {
	"id" : dictionary_from["id"].keys(),
	"en" : dictionary_from["en"].keys()
}


def create_model(size, window, version, min_batch) :

	print('train mlp_s' + str(size) + "_w" + str(window) + "_v%s" % str(version)  + "...")
	
	try :
		os.makedirs('./model/mlp_match_s' + str(size) + "_w" + str(window) + "_v" + str(version))
	except Exception as e :
		pass

	model = { 
		"en" : Word2Vec.load('model/model_en_s' + str(size) + "_w" + str(window) + "_v%s" % str(version) + ".word2vec"),
		"id" : Word2Vec.load('model/model_id_s' + str(size) + "_w" + str(window) + "_v%s" % str(version) + ".word2vec")
		}

	x = tf.placeholder(tf.float32, [None, size], name='input_x')

	hidden = tf.contrib.layers.fully_connected(x, 100)
	weights = tf.Variable(tf.truncated_normal([100, size], stddev=0.05), name='weights')
	biases = tf.Variable(tf.truncated_normal([size], stddev=0.05), name='biases')
	out = tf.add(tf.matmul(hidden, weights), biases, name='out')

	y = tf.placeholder(tf.float32, [None, size], name='input_y')

	loss = tf.reduce_mean(tf.abs(tf.subtract(out, y)))
	train = tf.train.GradientDescentOptimizer(0.1).minimize(loss, name='train')

	saver = tf.train.Saver()
	sess = tf.Session()
	sess.run(tf.global_variables_initializer())

	langs = ["en", "id"]
	train_count = 0
	for i in range(len(langs)) :
		l = langs[i]
		print("process %s :" % l)
		vec_ws = []
		vec_wt = []
		idx = 0
		for ws in words[l] :
			target_words = dictionary_from[l][ws] + [ stemmer[langs[1-i]].stem(x) for x in dictionary_from[l][ws] ]
			for wt in target_words :
				idx +=1
				print("process %d ..." % idx)
				if ws in model[l].wv and wt in model[langs[1 - i]].wv :
					print("appending %d ..." % idx)

					vec_ws.append(model[l][ws])
					vec_wt.append(model[langs[1 - i]][wt])

					if len(vec_ws) >= min_batch :
						train_count += 1
						print("train %d ..." % train_count)
						xx = vec_ws if l == "id" else vec_wt
						yy = vec_wt if l == "id" else vec_ws
						sess.run([train], feed_dict = {x : xx, y : yy})
						vec_ws = []
						vec_wt = []


		if len(vec_ws) >= 1 :
			print("train the last remnants ..." )
			sess.run([train], feed_dict = {x : vec_ws, y : vec_wt})

	saver.save(sess, 'model/mlp_match_s' + str(size) + "_w" + str(window) + "_v" + str(version) + "/model")

if __name__ == "__main__" :
	create_model(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), 5)






