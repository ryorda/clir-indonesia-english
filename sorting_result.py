import sys
import os

for d in os.listdir('result/') :
	f = open(os.path.abspath('result/' + d), 'r')

	print('processing ' + d + '...')
	docs = {}

	for line in f :
		params = line.strip().split()
		query = int(params[0])
		docno = params[1]
		similarity = params[2]

		if query not in docs.keys() :
			docs[query] = []

		docs[query].append((similarity, docno))

	for k in docs.keys() : 	
		docs[k] = sorted(docs[k], key=lambda x: x[0], reverse=True)


	res = open(os.path.abspath('proc_result/proc_' + d), 'w')
	for k, v in docs.items() : 	
		for idx in range(min(int(sys.argv[1]), len(v))) :
			res.write('%s Q0 %s %d %f NH-BM25\n' % (k, v[idx][1], idx, float(v[idx][0])))

	print('processing ' + d + ' [done]')
