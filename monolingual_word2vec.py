from gensim.models import Word2Vec
from nltk.tokenize import WhitespaceTokenizer

tokenizer = WhitespaceTokenizer()

en_doc = open('dataset/GV-en_tokenized%s.txt' % sys.argv[1], 'r')
id_doc = open('dataset/GV-id_tokenized%s.txt' % sys.argv[1], 'r')

en_sentences = []
id_sentences = []

idx = 0
for line in zip(en_doc, id_doc) :
	en_tokens = tokenizer.tokenize(line[0].strip())
	id_tokens = tokenizer.tokenize(line[1].strip())

	en_sentences.append(en_tokens)
	id_sentences.append(id_tokens)

for size in [100, 200, 300, 400] :
	for window in [1, 3, 5, 7] :
		print('creating model_en_s' + str(size) + "_w" + str(window) + "_v%s" % sys.argv[1]  + "...")
		model_en = Word2Vec(en_sentences, size=size, window=window, min_count=5, workers=4)
		model_en.save('model/model_en_s' + str(size) + "_w" + str(window) + "_v%s" % sys.argv[1] + ".word2vec")

		print('creating model_id_s' + str(size) + "_w" + str(window) + "_v%s" % sys.argv[1]  + "...")
		model_id = Word2Vec(id_sentences, size=size, window=window, min_count=5, workers=4)
		model_id.save('model/model_id_s' + str(size) + "_w" + str(window) + "_v%s" % sys.argv[1] + ".word2vec")