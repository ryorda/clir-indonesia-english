import sys
import os
from multiprocessing import Pool

folder = sys.argv[3]

def sorting(d) :
	f = open(os.path.abspath('result/{0}/{1}'.format(folder, d)), 'r', encoding='utf-8')

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


	res = open('proc_result/{0}/proc_{1}'.format(folder, d), 'w', encoding='utf-8')
	for (k, v) in list(docs.items()):
		for idx in range(min(int(sys.argv[1]), len(v))) :
			res.write('%s Q0 %s %d %f NH-BM25\n' % (k, v[idx][1], idx, float(v[idx][0])))

	print('processing ' + d + ' [done]')

pool = Pool(int(sys.argv[2]))

pool.map(sorting, os.listdir('result/{0}/'.format(folder)))
	
