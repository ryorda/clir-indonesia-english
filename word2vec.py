from gensim.models import Word2Vec
from nltk.tokenize import WhitespaceTokenizer

tokenizer = WhitespaceTokenizer()

en_doc = open('../dataset/GV-en_tokenized.txt', 'r')
id_doc = open('../dataset/GV-id_tokenized.txt', 'r')

en_sentences = []
id_sentences = []

for line in en_doc :
	en_sentences.append(tokenizer.tokenize(line.strip()))

for line in id_doc :
	id_sentences.append(tokenizer.tokenize(line.strip()))

for size in [100, 200, 300, 400] :
	print('creating model_en_' + str(size) + "...")
	model_en = Word2Vec(en_sentences, size=size, window=5, min_count=5, workers=4)
	model_en.save('model/model_en_' + str(size) + ".word2vec")
	print('creating model_id_' + str(size) + "...")
	model_id = Word2Vec(id_sentences, size=size, window=5, min_count=5, workers=4)
	model_id.save('model/model_id_' + str(size) + ".word2vec")

