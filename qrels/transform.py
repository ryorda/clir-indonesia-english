f = open('AH-BILI-X2EN-CLEF2006-qrels.txt')
w = open('qrels.txt', 'w')
w2 = open('unique_docs.txt', 'w')

unique_words = set()
for line in f :
	words = line.strip().split()
	words[0] =  str(int(words[0]) - 301)
	w.write("\t".join(words) + "\n")
	unique_words.add(words[2])

print(len(unique_words))

for w in unique_words :
	w2.write(w + '\n')
