#coding: utf8

from textblob_de import *
from textblob_de.lemmatizers import PatternParserLemmatizer
import sys
import nltk
from nltk import *

def main():
	reload(sys)
	sys.setdefaultencoding('utf8')

	lp = LanguageProcessor("Heute ist ein schöner Tag. Gestern war ein schlechter Tag")
	lp.processText()

class LanguageProcessor:

	def __init__(self, plainText):
		self._plainText = plainText
		self._textBlob = None
		self._tokens = []
		self._tokensAndPOS = []
		self._lemmas = []
		self._lemmasAndPOS = []
		self._lemmaAndPOSDict = None
		self._wordFrequencies = []

	def processText(self):
		self._textBlob = TextBlobDE(self._plainText)
		self._tokens = self._textBlob.words
		self._tokensAndPOS = self._textBlob.tags
		self.lemmatize()
		self.calcWordFrequencies()
		self._lemmaAndPOSDict = dict(self._lemmasAndPOS)

	def lemmatize(self):
		self._lemmas = self._textBlob.words.lemmatize()
		
		for i in range(0, len(self._lemmas)):
			lemmaAndPOS = (self._lemmas[i], self._tokensAndPOS[i][1])
			self._lemmasAndPOS.append(lemmaAndPOS)

	def calcWordFrequencies(self):
		fdist = FreqDist(self._lemmas)
		frequencies = fdist.most_common()
		self._wordFrequencies = frequencies

	def generateWordFrequenciesOutput(self):
		


if __name__ == "__main__":
    main()