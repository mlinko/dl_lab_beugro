#!/usr/bin/python

from random import randint

def getWords(files):
	words = []
	for f in files:
		with open(f, 'r') as fi:

			for line in fi:
				for word in line.strip().split(' '):
					words.append( word )
	words = filter(None, words)
	words = filter( lambda x: not x.isupper() or x in ['A', 'I'] , words) #do not want to filter the A and I words
	
	#for word in words:
	#	if word.isupper() and word not in ['A', 'I'] : print word
	
	return words

def findNextWord( lastWord, words):
	foundWords = []
	if lastWord[-1] in ['.','?','!']:
		for i, word in enumerate(words[-1]):
			if lastWord[-1] in ['.','?','!']:
				foundWords.append( words[ i+1])
	elif lastWord.endswith(','):
		for i, word in enumerate(words[:-1]):
			if lastWord.endswith('.'):
				foundWords.append( words[ i+1])
	else:
		for i, word in enumerate(words[:-1]):
			if lastWord.lower() == word.lower():
				foundWords.append( words[ i+1])
	if foundWords:
		return foundWords[ randint(0, len(foundWords) -1) ]
	else:
		return words[ randint(0, len(words)-1) ]
		
def isEnough( text, wantedSize):
	if len(text) >= wantedSize :
		return False
	return True


if __name__ == '__main__':
	words = getWords( [ 'hg1.txt', 'hg2.txt', 'hg3_1.txt', 'hg3_2.txt'] )
	print len(words)
	
	lastWord = 'He' #str( raw_input('First word of the generated text: '))
	wantedSize = 500 #int( raw_input('Wanted size of the text :'))
	text = lastWord 
	needMore = True

	while needMore:
		nextWord = findNextWord( lastWord, words)
		text += ' ' +  nextWord
		lastWord = nextWord[:]

		if text[-1] in ['.','?','!']:
			needMore = isEnough( text, 500)
	print "-------------------------------------------------------------------------------------"
	print text
	print "-------------------------------------------------------------------------------------"
