from multiprocessing import Pool

file = open('test.txt', 'w')
def test(n) :
	for _ in range(n) :
		file.write('x\n')
		file.flush()

pool = Pool(3)
it = [100, 200, 300, 400]

pool.map(test, it)
