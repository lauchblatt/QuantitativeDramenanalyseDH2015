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

	lp = LanguageProcessor()
	lp.processSingleDrama("../Lessing-Dramen/-Der_junge_Gelehrte.xml")
	lp.generateWordFrequenciesOutput("test")

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

	def processText(self, plainText):
		self._plainText = plainText
		self._textBlob = TextBlobDE(self._plainText)
		self._tokens = self._textBlob.words
		self._tokensAndPOS = self._textBlob.tags
		self.lemmatize()
		self.calcWordFrequencies()
		self._lemmaAndPOSDict = dict(self._lemmasAndPOS)

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