#!/usr/bin/python3

import sys, argparse
from tensorflow.examples.tutorials.mnist import input_data
import tensorflow as tf

'''
Firstly I have started to solve the problem with openCV, since
I had no clue about the furthermore steps, I have decided to give 
a try to the tensorflow module.
It has turned out learning on the MNIST database is the 'Hello World'
of deeplearning, and there are many tutorials. I have tried to 
follow one, and to understand what is exactly going on here.
'''

def main(_):
	dataset = input_data.read_data_sets("MNIST_data/",one_hot=True)
	
	print("Dataset ok\n")

	x = tf.placeholder(tf.float32, [None, 784])
	W = tf.Variable(tf.zeros([784, 10]))
	b = tf.Variable(tf.zeros([10]))
	y = tf.matmul(x, W) + b
	
	y_ = tf.placeholder(tf.float32, [None, 10])
	cross_entropy = tf.reduce_mean( tf.nn.softmax_cross_entropy_with_logits( labels=y_, logits=y))
	train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)
	
	sess = tf.InteractiveSession()
	tf.global_variables_initializer().run()
	
	print("Started trainingi\n")
	for i in range(1000):
		batch_xs, batch_ys = dataset.train.next_batch(100)
		sess.run(train_step, feed_dict={x: batch_xs, y_: batch_ys})
	
	correct_prediction = tf.equal(tf.argmax(y,1), tf.argmax(y_,1))
	accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
	print(sess.run(accuracy, feed_dict={x: dataset.test.images, y_: dataset.test.labels}))

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--data_dir', type=str, default='/tmp/tensorflow/mnist/input_data', help='Dir to store input data')

	FLAGS, unparsed = parser.parse_known_args()
	tf.app.run(main=main, argv=[sys.argv[0]] + unparsed)
