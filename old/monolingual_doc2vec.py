from gensim.models import Doc2Vec
from gensim.models.doc2vec import LabeledSentence
from nltk.tokenize import WhitespaceTokenizer
import sys

tokenizer = WhitespaceTokenizer()

en_doc = open('dataset/GV-en_tokenized%s.txt' % sys.argv[1], 'r', encoding='utf-8')
id_doc = open('dataset/GV-id_tokenized%s.txt' % sys.argv[1], 'r', encoding='utf-8')

en_sentences = []
id_sentences = []

idx = 0
for line in zip(en_doc, id_doc) :
	en_tokens = tokenizer.tokenize(line[0].strip())
	id_tokens = tokenizer.tokenize(line[1].strip())

	en_sentences.append(LabeledSentence(words=en_tokens, tags=['en_mono_' + str(idx)]))
	id_sentences.append(LabeledSentence(words=id_tokens, tags=['id_mono_' + str(idx)]))
	idx += 1

print("sentences %d" % len(en_sentences))

for size in [100, 200, 300, 400] :
	for window in [1, 3, 5, 7] :
		# print('creating model_en_s' + str(size) + "_w" + str(window) + "_v%s" % sys.argv[1]  + "...")
		# model_en = Doc2Vec(en_sentences, size=size, window=window, min_count=5, workers=4)
		# model_en.save('model/model_en_s' + str(size) + "_w" + str(window) + "_v%s" % sys.argv[1] + ".doc2vec")

		print('creating model_id_s' + str(size) + "_w" + str(window) + "_v%s" % sys.argv[1]  + "...")
		model_id = Doc2Vec(id_sentences, size=size, window=window, min_count=5, workers=4)
		model_id.save('model/model_id_s' + str(size) + "_w" + str(window) + "_v%s" % sys.argv[1] + ".doc2vec")