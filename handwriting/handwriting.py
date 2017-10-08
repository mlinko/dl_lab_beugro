#!/usr/bin/python3
import os
import struct
import numpy as np
from random import randint
import json

PATH_TO_MNIST = '../MNIST_data/'
JSONFILE = './state.json'
BINARY_MAP = { 0 : [False, False, False, False],
               1 : [False, False, False,  True], 
               2 : [False, False,  True, False], 
               3 : [False, False,  True,  True], 
               4 : [False,  True, False, False], 
               5 : [False,  True, False,  True], 
               6 : [False,  True,  True, False], 
               7 : [False,  True,  True,  True], 
               8 : [ True, False, False, False], 
               9 : [ True, False, False,  True] }
class Perceptron:
	def __init__(self):
		self.number = None
		self.W = None
		self.bias = None
		self.x0 = None
		self.nu = None

	def fromScratch(self, number, inputSize):
		self.number = number
		self.W = np.random.rand(inputSize)
		self.bias = randint(1,255)
		self.x0 = -1
		self.nu = 3

	def fromState(self, state):
		self.number = state['number']
		self.W = np.array(state['W'])
		self.bias = state['bias']
		self.x0 = state['x0']
		self.nu = state['nu']
	
	def sgn(self, inputVector):
		summa = np.dot(self.W, inputVector)
		summa += (self.x0 * self.bias)
		if summa >= 0: return True
		else: return False
	
	def learn(self, inputVector, wantedResult):
		givenResult = self.sgn(inputVector)
		error = wantedResult - givenResult
		self.W = self.W + self.nu * error * inputVector
		self.bias = self.bias + self.nu * error * self.x0
	
	def getState(self):
		state = {}
		state['number'] = self.number
		state['W'] = self.W.tolist()
		state['bias'] = self.bias
		state['x0'] = self.x0
		state['nu'] = self.nu

		return state
		
	
			
class Network:
	def __init__(self):
		self.perceptrons = []
	
	def fromScratch(self, numberOfPerceptrons, inputSize):
		for i in range(numberOfPerceptrons):
			perceptron = Perceptron()
			perceptron.fromScratch(i, inputSize)
			self.perceptrons.append(perceptron)

	def fromJson(self, pathToState):
		with open(pathToState, 'r') as f:
			states = json.load(f)
		for state in states:
			perceptron = Perceptron()
			perceptron.fromState(state)
			self.perceptrons.append(perceptron)
			
	def training(self, inputs, labels, trainingRounds ):
		for roundNum in range(trainingRounds):
			print('Training round',roundNum)
			for xi, label in zip(inputs, labels):
				for i, perceptron in enumerate(self.perceptrons):
					perceptron.learn(xi, BINARY_MAP[label][ perceptron.number])
			self.save(JSONFILE)
	
	def testing(self, inputs, labels):
		numberOfHits = 0
		print('Testing...')
		for xi, label in zip(inputs, labels):
			numberOfHittedBinaryDigits = 0
			for i, perceptron in enumerate(self.perceptrons):
				if perceptron.sgn(xi) == BINARY_MAP[label][ perceptron.number]:
					numberOfHittedBinaryDigits += 1
			if numberOfHittedBinaryDigits == 4:
				numberOfHits += 1
		print('Accuracy: ', numberOfHits / len(inputs) *100, '%')

	def save(self, path):
		states = []
		for perceptron in self.perceptrons:
			states.append(perceptron.getState())
		with open(path, 'w+') as f:
			json.dump(states, f, indent=4, sort_keys=True)


def readInDataset(forTrain=True):
	if forTrain:
		img_file = os.path.join(PATH_TO_MNIST, 'train-images.idx3-ubyte')
		lab_file = os.path.join(PATH_TO_MNIST, 'train-labels.idx1-ubyte')
	else:
		img_file = os.path.join(PATH_TO_MNIST, 't10k-images.idx3-ubyte')
		lab_file = os.path.join(PATH_TO_MNIST, 't10k-labels.idx1-ubyte')

	with open(lab_file, 'rb') as f:
		magicNum, size  = struct.unpack('>II', f.read(8))
		labels = np.fromfile( f, dtype=np.uint8)
	#print(magicNum, size, labels, len(labels))
	with open(img_file, 'rb') as f:
		magicNum, size, rows, cols  = struct.unpack('>IIII', f.read(16))
		images = np.fromfile( f, dtype=np.uint8).reshape(len(labels), rows*cols)
	vectorSize = rows*cols
	#print(magicNum, size, rows, cols, images, len(images))
	#print(type(images), type(images[0]), type(images[0][0]))

	if forTrain: return images, labels, vectorSize
	else: return images, labels

if __name__ == '__main__':
	images, labels, vectorSize = readInDataset()
	network = Network()
	#network.fromScratch(4, vectorSize)
	network.fromJson(JSONFILE)
	network.training(images, labels, 200)
	images, labels = readInDataset(forTrain=False)
	network.testing(images, labels)
