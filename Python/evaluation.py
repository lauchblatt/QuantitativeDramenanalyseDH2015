#coding: utf8

import os
import re
import collections
import locale
import sys
from lexicon_handler import *

def main():
	reload(sys)
	sys.setdefaultencoding('utf8')

	lexiconHandlerSentiWS = Lexicon_Handler()
	lexiconHandlerSentiWS.initSingleDict("NRC-Lemmas")
	lexiconLemmasDict = lexiconHandlerSentiWS._sentimentDictLemmas
	lexiconDict = lexiconHandlerSentiWS._sentimentDict

	evaluation = Evaluation_LexiconVSVocabulary()
	vocabulary = evaluation.readVocabulary("../Word-Frequencies/test.txt")
	print("Tokens")
	print(len(lexiconDict))
	evaluation.compareLexiconAndDramaVocabulary(lexiconDict, vocabulary)
	print("Lemmas")
	print(len(lexiconLemmasDict))
	evaluation.compareLexiconAndDramaVocabulary(lexiconLemmasDict, vocabulary)

class Evaluation_LexiconVSVocabulary:

	def __init__(self):
		self._vocabulary = None

	def test(self, sentimentDict):

		caseDoubleWords = []

		for word in sentimentDict:
			upperWord = word[:1].upper() + word[1:]
			lowerWord = word.lower()
			if(upperWord in sentimentDict and lowerWord in sentimentDict):
				caseDoubleWords.append(word)
				print word

		print(len(caseDoubleWords))

	def compareLexiconAndDramaVocabulary(self, lexicon, vocabulary):
		recognized = []
		for word in vocabulary:
			if(word in lexicon):
				recognized.append(word)
			else:
				upperWord = word[:1].upper() + word[1:]
				lowerWord = word.lower()
				if(upperWord in lexicon or lowerWord in lexicon):
					recognized.append(word)

		for word in recognized:
			print word

		print len(recognized)
		print len(vocabulary)
		print (float(float(len(recognized))/float(len(vocabulary))))

		return recognized

	def readVocabulary(self, path):
		vocFile = open(path, 'r')
		lines = vocFile.readlines()[4:]
		vocabulary = []
		
		for line in lines:
			languageInformation = line.split("\t")
			word = languageInformation[0]
			vocabulary.append(unicode(word))

		return vocabulary

if __name__ == "__main__":
    main()