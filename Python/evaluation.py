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

	evaluation = Evaluation_LexiconVsVocabulary()
	evaluation.init("../Word-Frequencies/Tokens/EntireCorpus.txt", "NRC")
	
	#evaluation.evaluateLexiconTokensAndLemmasVsMultipleVocabularies("../Word-Frequencies/Lemmas", "NRC")
	result = evaluation.evaluateLexiconLemmasVsVocabulary()

	evaluation.writeResultOutput("../Evaluation/NRC/LemmaTokenEntireCorpus.txt", result)

class Evaluation_LexiconVsVocabulary:

	def __init__(self):
		self._placeholder = ""
		self._vocabulary = None

		self._lexiconName = ""
		self._lexicon = {}
		self._lexiconLemmas = {}

		self._vocabulary = None
	
	def init(self, vocPath, lexiconName):
		self._vocabulary = self.readVocabulary(vocPath)
		self.setLexicon(lexiconName)

	def setLexicon(self, lexiconName):
		lexiconHandler = Lexicon_Handler()
		lexiconHandler.initSingleDict(lexiconName)

		self._lexiconName = unicode(lexiconName)
		self._lexicon = lexiconHandler._sentimentDict
		self._lexiconLemmas = lexiconHandler._sentimentDictLemmas

	def evaluateLexiconTokensAndLemmasVsMultipleVocabularies(self, vocFolder, lexiconName):
		for filename in os.listdir(vocFolder):
			vocPath = vocFolder + "/" + filename
			self.init(vocPath, lexiconName)
			results = self.evaluateLexiconTokensAndLemmasVsVocabulary()
			print(results[0]._recognizedPercentage)
			print(results[1]._recognizedPercentage)
			outputPath = "../Evaluation/" + lexiconName + "/"
			crossFolder1 = "TokensLexiconVS" + self._vocabulary._type + "Vocabulary/"
			crossFolder2 = "LemmasLexiconVS" + self._vocabulary._type + "Vocabulary/"
			name1 = lexiconName + "-TokensVS-" + self._vocabulary._name + "-" + self._vocabulary._type
			name2 = lexiconName + "-LemmasVS-" + self._vocabulary._name + "-" + self._vocabulary._type

			outputPathTokens = outputPath + crossFolder1 + name1 + ".txt"
			outputPathLemmas = outputPath + crossFolder2 + name2 + ".txt"
			
			self.writeResultOutput(outputPathTokens, results[0])
			self.writeResultOutput(outputPathLemmas, results[1])


	def evaluateLexiconTokensAndLemmasVsVocabulary(self):
		results = []
		results.append(self.evaluateLexiconTokensVsVocabulary())
		results.append(self.evaluateLexiconLemmasVsVocabulary())
		return results

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

	def test(self, sentimentDict):

		caseDoubleWords = []

		for word in sentimentDict:
			upperWord = word[:1].upper() + word[1:]
			lowerWord = word.lower()
			if(upperWord in sentimentDict and lowerWord in sentimentDict):
				caseDoubleWords.append(word)

class Vocabulary:

	def __init__(self, path):
		self._name = ""
		self._type = ""

		self._wordsWithInformationDict = {}
		self._words = []

		self.init(path)

	def init(self, path):
		vocabularyFile = open(path, 'r')
		pathParts = path.split("/")
		lines = vocabularyFile.readlines()[5:]

		self._name = unicode(path.split("/")[-1].replace(".txt", "").decode("cp1252"))
		self._type = path.split("/")[-2]

		for line in lines:
			wordsWithInformation = line.split("\t")
			word = unicode(wordsWithInformation[0])
			information = wordsWithInformation.pop(0)

			self._wordsWithInformationDict[word] = information
			self._words.append(word)

class Evaluation_Result_Vocabulary:

	def __init__(self):
		self._nameOfLexicon = ""
		self._lexicon = {}

		self._recognizedWords = None
		self._recognizedPercentage = 0.0

if __name__ == "__main__":
    main()