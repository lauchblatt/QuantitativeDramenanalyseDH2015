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

	evaluation = Evaluation_LexiconVSVocabulary("../Word-Frequencies/test.txt", "CD")
	

	result = evaluation.evaluateLexiconTokensVsVocabulary()

	evaluation.writeResultOutput("../Evaluation/CD-Lemmas-Vocabulary-Lemmas.txt", result)
	print(result._recognized)
	print(result._recognizedPercentage)

class Evaluation_LexiconVSVocabulary:

	def __init__(self, vocPath, lexiconName):
		self._placeholder = ""
		self._vocabulary = None

		self._lexiconName = ""
		self._lexicon = {}
		self._lexiconLemmas = {}

		self._vocabulary = self.readVocabulary(vocPath)
		
		self.setLexicon(lexiconName)
	
	def setLexicon(self, lexiconName):
		lexiconHandler = Lexicon_Handler()
		lexiconHandler.initSingleDict(lexiconName)

		self._lexiconName = lexiconName
		self._lexicon = lexiconHandler._sentimentDict
		self._lexiconLemmas = lexiconHandler._sentimentDictLemmas

	def evaluateLexiconLemmasVsVocabulary(self):
		result = self.evaluateLexiconVsVocabulary(self._lexiconLemmas)
		return result

	def evaluateLexiconTokensVsVocabulary(self):
		result = self.evaluateLexiconVsVocabulary(self._lexicon)
		return result
	
	def evaluateLexiconVsVocabulary(self, lexicon):
		recognized = self.getRecognizedWordsOfVocabulary(lexicon)
		recognizedPercentage = self.getRecognizedPercentage(recognized, self._vocabulary._words)

		result = Evaluation_Result_Vocabulary()
		result._nameOfLexicon = self._lexiconName
		result._lexicon = lexicon
		result._recognized = recognized
		result._recognizedPercentage = recognizedPercentage

		return result

	def getRecognizedWordsOfVocabulary(self, lexicon):
		words = self._vocabulary._words
		recognized = self.getRecognizedWords(lexicon, self._vocabulary._words)

		return recognized

	def getRecognizedWords(self, lexicon, vocabularyList):
		recognized = []
		for word in vocabularyList:
			if(word in lexicon):
				recognized.append(word)
			else:
				upperWord = word[:1].upper() + word[1:]
				lowerWord = word.lower()
				if(upperWord in lexicon or lowerWord in lexicon):
					recognized.append(word)

		return recognized

	def getRecognizedPercentage(self, recognized, vocabularyList):

		return (float(float(len(recognized))/float(len(vocabularyList))))

	def getWordDifferencesOfRecognizedLexiconWords(self, recognized1, recognized2):
		in1MissingIn2 = []
		in2MissingIn1 = []


	def readVocabulary(self, path):
		vocabulary = Vocabulary(path)

		return vocabulary

	
	def writeResultOutput(self, path, result):
		outputFile = open(path, 'w')

		outputFile.write(result._nameOfLexicon + " IN " + self._vocabulary._name)
		outputFile.write("\n\n")
		outputFile.write("Length of Lexicon: " + str(len(result._lexicon)))
		outputFile.write("\nLength of Vocabulary: " + str(len(self._vocabulary._words)))
		outputFile.write("\nRecognized Words: " + str(len(result._recognized)))
		outputFile.write("\nRecognized Percentage: " + str(result._recognizedPercentage))

		outputFile.write("\n\nRecognized Words:\n\n")
		for word in result._recognized:
			outputFile.write(word + "\n")

		outputFile.close

		print(self._vocabulary._name)
		print(result._nameOfLexicon)


	def test(self, sentimentDict):

		caseDoubleWords = []

		for word in sentimentDict:
			upperWord = word[:1].upper() + word[1:]
			lowerWord = word.lower()
			if(upperWord in sentimentDict and lowerWord in sentimentDict):
				caseDoubleWords.append(word)
				print word

		print(len(caseDoubleWords))

class Vocabulary:

	def __init__(self, path):
		self._name = ""

		self._wordsWithInformationDict = {}
		self._words = []

		self.init(path)

	def init(self, path):
		vocabularyFile = open(path, 'r')
		lines = vocabularyFile.readlines()[4:]

		self._name = path.split("/")[-1]

		for line in lines:
			wordsWithInformation = line.split("\t")
			word = unicode(wordsWithInformation[0])
			information = wordsWithInformation.pop(0)

			self._wordsWithInformationDict[word] = information
			self._words.append(word)

class Evaluation_Result_Vocabulary:

	def __init__(self):
		self._nameOfLexicon = ""
		self._lexicon = []

		self._recognizedWords = None
		self._recognizedPercentage = 0.0

if __name__ == "__main__":
    main()