from gensim.models import Word2Vec
from nltk.tokenize import WhitespaceTokenizer

tokenizer = WhitespaceTokenizer()

en_doc = open('../dataset/GV-en_tokenized.txt', 'r')
id_doc = open('../dataset/GV-id_tokenized.txt', 'r')

en_sentences = []
id_sentences = []

bilingual_sentences = []

idx = 0
for line in zip(en_doc, id_doc) :
	en_tokens = tokenizer.tokenize(line[0].strip())
	id_tokens = tokenizer.tokenize(line[1].strip())

	new_tokens = []
	maxlength = max(len(en_tokens), len(id_tokens))
	for i in range(maxlength) :
		try:
			new_tokens.append(en_tokens[i])
		except IndexError :
			pass

		try:
			new_tokens.append(id_tokens[i])
		except IndexError :
			pass

	bilingual_sentences.append(new_tokens)

print(len(bilingual_sentences))

for size in [100, 200, 300, 400] :
	for window in [3, 5, 7, 9] :
		print('creating model_bilingual_' + str(size) + "_" + str(window) + "...")
		model_en = Word2Vec(bilingual_sentences, size=size, window=window, min_count=5, workers=4)
		model_en.save('model/model_bilingual_' + str(size) + "_" + str(window) + ".word2vec")