from gensim.models import Doc2Vec
from gensim.models.doc2vec import LabeledSentence
from nltk.tokenize import WhitespaceTokenizer
import sys

tokenizer = WhitespaceTokenizer()

bil_doc = open('dataset/GV-id_en_tokenized.txt', 'r', encoding='utf-8')

bil_sentences = []

idx = 0
for line in bil_doc :
	idx += 1
	print('reading docs %d' % idx)
	bil_tokens = tokenizer.tokenize(line[0].strip())
	bil_sentences.append(LabeledSentence(words=bil_tokens, tags=['bil_' + str(idx)]))


for size in [100, 200, 300, 400] :
	for window in [1, 3, 5, 7] :
		print('creating model_bil_s' + str(size) + "_w" + str(window) + "_v" + str(sys.argv[1])  + "...")
		model_bil = Doc2Vec(bil_sentences, size=size, window=window, min_count=5, workers=4)
		model_bil.save('model/model_bil_s' + str(size) + "_w" + str(window) + "_v" + str(sys.argv[1]) + ".doc2vec")