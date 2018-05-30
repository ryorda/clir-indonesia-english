import tensorflow as tf


class SentenceEmbedding():
	def __init__(self, vocab, dim=100, window=1, hidden_size=1, epoch=10) :
		self.vocab = {el: 0 for el in vocab}
		self.vocab_size = len(self.vocab)
		self.hidden_size = hidden_size
		self.dim = dim
		self.context_size = 2*window
		self.epoch = epoch

		__construct_model()


	def __construct_model(self): 
		input_target = tf.placeholder(tf.float32, [None, self.vocab_size])
		actual_context = tf.placeholder(tf.float32, [None, self.context_size, self.vocab_size])

		hidden_state = tf.contrib.layers.fully_connected(
			inputs=input_target, 
			num_outputs=self.dim,
			activation_fn=tf.nn.relu
			)

		for _ in range(self.hidden_size - 1) :
			hidden_state = tf.contrib.layers.fully_connected(
				hidden_state,
				num_outputs=self.dim,
				activation_fn=tf.nn.relu
				)

		hidden_state = tf.contrib.layers.fully_connected(
			hidden_state,
			num_outputs=self.dim,
			activation_fn=tf.nn.relu
		)

		W = tf.Variable(tf.random_normal([self.dim, self.context_size, vocab_size]))
		b = tf.Variable(tf.random_normal([self.context_size, vocab_size]))

		self.out = tf.add(tf.matmul(hidden_state, W), b)

		loss = tf.reduce_mean(tf.abs(tf.subtract(self.out, actual_context)))

		self.train_op = tf.train.GradientDescentOptimizer(0.1).minimize(loss)

		self.sess = tf.InteractiveSession()
		self.sess.run(tf.global_variables_initializer())


	def __train(self, target, context) :
		self.sess.run([ self.train_op], feed_dict={ input_target: target, actual_context: context} )

	
	# vectorize sentence by vocabularies
	def __get_term_frequency(self, words) :
		voc = self.vocab.copy()

		for w in words :
			voc[w] = voc[w]+1

		return voc

	# array of array of words
	def train(self, sentences) :
		vectors = []
		for s in sentences :
			vectors.append(self.__get_term_frequency(s))

		for i in range(len(sentences) - self.context_size) :
			target = vectors[i + self.context_size/2]
			context = vectors[i:i+self.context_size/2] + vectors[i+self.context_size/2+1:self.context_size+1] 
			self.__train(target, context)

	def vectorize_sentence(self, words):
		freq = self.__get_term_frequency(words)
		vec = self.sess.run([self.out], feed_dict={input_target : words, actual_context : None})
		return vec


