#coding: utf8

import os
from textblob_de import *
from textblob_de.lemmatizers import PatternParserLemmatizer
import sys
import nltk
from nltk import *
from drama_parser import *
from drama_output import *

def main():
	reload(sys)
	sys.setdefaultencoding('utf8')
	text = "Anschließend ging ein anderer weg."

	lp = LanguageProcessor()
	print(lp._stopwords_lemmatized)
	lp.processText(text)
	print(lp._lemmas)

class LanguageProcessor:

	def __init__(self):
		
		self._plainText = ""
		self._textBlob = None
		self._tokens = []
		self._tokensAndPOS = []
		self._lemmas = []
		self._lemmasAndPOS = []
		self._lemmaAndPOSDict = None
		self._wordFrequencies = []
		self._stopwords = []
		self._stopwords_lemmatized = []
		self.initStopWords()

	def processText(self, plainText):
		self._plainText = plainText
		self._textBlob = TextBlobDE(self._plainText)
		self._tokens = self._textBlob.words
		self._tokensAndPOS = self._textBlob.tags
		self.lemmatize()
		self.calcWordFrequencies()
		self._lemmaAndPOSDict = dict(self._lemmasAndPOS)
		removeStopWords()

	def processSingleDrama(self, path):
		parser = DramaParser()
		dramaModel = parser.parse_xml(path)
		text = ""
		for act in dramaModel._acts:
			for conf in act._configurations:
				for speech in conf._speeches:
					text = text + str(speech._text)
		self.processText(text)

	def lemmatize(self):
		self._lemmas = self._textBlob.words.lemmatize()
		
		for i in range(0, len(self._lemmas)):
			lemmaAndPOS = (self._lemmas[i], self._tokensAndPOS[i][1])
			self._lemmasAndPOS.append(lemmaAndPOS)

	def initStopWords(self):
		stopwords_text = open("stopwords_german.txt")
		for line in stopwords_text:
			self._stopwords.append(line.strip())
			stopword_lemmatized = TextBlobDE(line.strip()).words.lemmatize()[0]
			self._stopwords_lemmatized.append(stopword_lemmatized)

	def removeStopWords(self):
		for lemma in self._lemmas:
			for stopword in self_stopwords_lemmatized:

	def calcWordFrequencies(self):
		fdist = FreqDist(self._lemmas)
		frequencies = fdist.most_common()
		self._wordFrequencies = frequencies

	def generateWordFrequenciesOutput(self, dataName):
		outputFile = open(dataName + ".txt", "w")

		for frequ in self._wordFrequencies:
			pos = self._lemmaAndPOSDict[frequ[0]]
			outputFile.write(str(frequ[0]) + "\t" + str(pos) + "\t" + str(frequ[1]) + "\n")
		outputFile.close()

if __name__ == "__main__":
    main()