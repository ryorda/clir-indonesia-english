from gensim.models import Doc2Vec
from gensim.models.doc2vec import LabeledSentence
from nltk.tokenize import WhitespaceTokenizer
import sys

tokenizer = WhitespaceTokenizer()

en_doc = open('dataset/GV-en_tokenized%s.txt' % sys.argv[1], 'r')
id_doc = open('dataset/GV-id_tokenized%s.txt' % sys.argv[1], 'r')

en_sentences = []
id_sentences = []

bilingual_sentences = []

idx = 0
docs = []
for line in zip(en_doc, id_doc) :
	en_tokens = tokenizer.tokenize(line[0].strip())
	id_tokens = tokenizer.tokenize(line[1].strip())

	new_tokens = []
	new_tokens2 = []
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

		try:
			new_tokens2.append(id_tokens[i])
		except IndexError :
			pass
		try:
			new_tokens2.append(en_tokens[i])
		except IndexError :
			pass


	bilingual_sentences.append(LabeledSentence(words=new_tokens, tags=['en_id_bilingual_' + str(idx)]))
	bilingual_sentences.append(LabeledSentence(words=new_tokens2, tags=['id_en_bilingual_' + str(idx)]))
	bilingual_sentences.append(LabeledSentence(words=en_tokens, tags=['en_' + str(idx)]))
	bilingual_sentences.append(LabeledSentence(words=id_tokens, tags=['id_' + str(idx)]))
	
	idx += 1

for size in [100, 200, 300, 400] :
	for window in [3, 5, 7, 9] :
		print('creating model_bilingual_mono_' + str(size) + "_" + str(window) + "...")
		model_en = Doc2Vec(bilingual_sentences, dm=0, dbow_words=1, size=size, window=window, min_count=5, workers=4)
		model_en.save('model/model_bilingual_mono_' + str(size) + "_" + str(window) + ".doc2vec")