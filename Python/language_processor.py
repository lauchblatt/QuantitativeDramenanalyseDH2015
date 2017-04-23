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
		self._lemmasWithoutStopwords = []
		self._lemmasAndPOS = []
		self._lemmaAndPOSDict = None
		self._wordFrequencies = []
		self._stopwords = []
		self._stopwords_lemmatized = []
		self.initStopWords()

	def processText(self, plainText):
		self._plainText = plainText
		self._textBlob = TextBlobDE(self._plainText)
		print("TextBlob ready...")
		self._tokens = self._textBlob.words
		print("Tokens ready...")
		self._tokensAndPOS = self._textBlob.tags
		print("Tags ready...")
		self.lemmatize()
		print("Lemmas ready...")
		self._lemmaAndPOSDict = dict(self._lemmasAndPOS)
		self.removeStopWordsFromLemmas()
		print("StopWords removed...")
		self.calcWordFrequencies()
		print("Frequencies calculated...")

	def processSingleDrama(self, path):
		parser = DramaParser()
		dramaModel = parser.parse_xml(path)
		print("dramaModel ready...")
		text = ""
		
		for act in dramaModel._acts:
			for conf in act._configurations:
				for speech in conf._speeches:
					newText = str(speech._text.replace("–", ""))
					text = text + newText

		"""
		for i in range(0, 1):
			for conf in dramaModel._acts[i]._configurations:
				for speech in conf._speeches:
					newText = str(speech._text.replace("–", ""))
					text = text + newText
		print("Text ready...")
		self.processText(text)
		"""

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

	def removeStopWordsFromLemmas(self):
		lemmasCopy = list(self._lemmas)
		for stopword in self._stopwords_lemmatized:
			while stopword.lower() in lemmasCopy:
				lemmasCopy.remove(stopword.lower())
			while stopword.title() in lemmasCopy:
				lemmasCopy.remove(stopword.title())

		for stopword in self._stopwords:
			while stopword.lower() in lemmasCopy:
				lemmasCopy.remove(stopword.lower())
			while stopword.title() in lemmasCopy:
				lemmasCopy.remove(stopword.title())

		self._lemmasWithoutStopwords = lemmasCopy
		print(self._lemmasWithoutStopwords)

	def calcWordFrequencies(self):
		fdist = FreqDist(self._lemmasWithoutStopwords)
		frequencies = fdist.most_common()
		self._wordFrequencies = frequencies

	def generateWordFrequenciesOutput(self, dataName):
		outputFile = open(dataName + ".txt", "w")

		for frequ in self._wordFrequencies:
			pos = self._lemmaAndPOSDict[frequ[0]]
			outputFile.write(str(frequ[0]) + "\t" + str(pos) + "\t" + str(frequ[1]) + "\n")
		outputFile.close()
		print("Output ready...")

if __name__ == "__main__":
    main()