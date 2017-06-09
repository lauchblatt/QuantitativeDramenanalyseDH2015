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

	text = "Ich gehe gerne in die Stadt zum Essen."
	lp.processText(text)
	
	"""
	lp.processSingleDrama("../Lessing-Dramen/less-Philotas_t.xml")
	
	
	lp.generateWordFrequenciesOutputLemmas("../Word-Frequencies/Lemmas/Minna_von_Barnhelm-Lemmas")
	
	lp.processEntireCorpusAndGenereateOutputLemmas("../Lessing-Dramen/")
	"""
	

class LanguageProcessor:

	def __init__(self):
		
		self._plainText = ""
		self._filteredText = ""
		self._textBlob = None
		self._tokens = []
		self._tokensAndPOS = []
		self._lemmas = []
		self._lemmasWithoutStopwords = []
		self._lemmasAndPOS = []
		self._lemmaAndPOSDict = None

		self._lemmasWithLanguageInfo = []

		self._lemmasAndPOSAndTokens = []
		self._lemmasAndPOSAndTokensDict = None

		self._wordFrequencies = []
		self._stopwords = []
		self._stopwords_lemmatized = []
		self.initStopWords()

	def processText(self, plainText):
		self._plainText = plainText
		self._filteredText = self.filterText(plainText)
		self._textBlob = TextBlobDE(self._filteredText)
		print("TextBlob ready...")
		self._tokens = self._textBlob.words
		print("Tokens ready...")
		self._tokensAndPOS = self._textBlob.tags
		print("Tags ready...")
		self.lemmatize()
		print("Lemmas ready...")

		print("LemmasANDPOSDict ready...")

		self.combineLemmasPOSTokens()
		print("LemmaAndPOSAndTokens ready...")
		
		self._lemmasAndPOSAndTokensDict = dict(self._lemmasAndPOSAndTokens)
		
		print("LemmasAndPOSAndTokensDict ready...")
		self.removeStopWordsFromLemmas()
		print("StopWords removed...")
		self.calcWordFrequencies()
		print("Frequencies calculated...")

	def filterText(self, text):
		newText = ""
		newText = unicode(text.replace("–", ""))
		newText = unicode(text.replace("'", ""))

		return newText

	def processSingleDrama(self, path):
		parser = DramaParser()
		dramaModel = parser.parse_xml(path)
		print("dramaModel ready...")
		text = ""
		#"""
		for act in dramaModel._acts:
			for conf in act._configurations:
				for speech in conf._speeches:
					text = text + speech._text
		#"""

		"""
		for i in range(3, 4):
			for conf in dramaModel._acts[i]._configurations:
				for speech in conf._speeches:
					newText = str(speech._text.replace("–", ""))
					text = text + newText
		"""
		
		"""
		for speech in dramaModel._acts[3]._configurations[1]._speeches:
				newText = unicode(str(speech._text.replace("–", "")))
				text = text + newText
		"""

		print("Text ready...")
		self.processText(text)

	def lemmatize(self):
		self._lemmas = self._textBlob.words.lemmatize()
		
		for i in range(0, len(self._lemmas)):
			lemmaAndPOS = (self._lemmas[i], self._tokensAndPOS[i][1])
			self._lemmasAndPOS.append(lemmaAndPOS)

			lemmaAndTokenPOS = (self._lemmas[i], (self._tokensAndPOS[i][0], self._tokensAndPOS[i][1]))
			self._lemmasWithLanguageInfo.append(lemmaAndTokenPOS)

	def combineLemmasPOSTokens(self):
		for lemma, POS in self._lemmaAndPOSDict.iteritems():
			tokensOfLemma = []
			for languageInfo in self._lemmasWithLanguageInfo:
				if(lemma == languageInfo[0]):
					token = languageInfo[1][0]
					if not self.isTokenOfLemma(tokensOfLemma, token):
						tokensOfLemma.append(token)
			lemmaAndPOSAndTokens = (lemma, POS, (tokensOfLemma))
			self._lemmasAndPOSAndTokens.append(lemmaAndPOSAndTokens)

	def isTokenOfLemma(self, tokensOfLemma, token):
		for alreadyToken in tokensOfLemma:
			if(alreadyToken == token):
				return True
		return False
	
	def initStopWords(self):
		stopwords_text = open("stopwords_german.txt")
		for line in stopwords_text:
			self._stopwords.append(unicode(line.strip()))
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

	def calcWordFrequencies(self):
		fdist = FreqDist(self._lemmasWithoutStopwords)
		frequencies = fdist.most_common()
		self._wordFrequencies = frequencies

	def generateWordFrequenciesOutputLemmas(self, dataName):
		outputFile = open(dataName + ".txt", "w")

		outputFile.write("Number of total lemmas " + str(len(self._lemmasWithoutStopwords)) + "\n")
		outputFile.write("Nummber of different lemmas " + str(len(self._wordFrequencies)) + "\n\n")

		for frequ in self._wordFrequencies:
			pos = self._lemmaAndPOSDict[frequ[0]]
			outputFile.write(str(frequ[0]) + "\t" + str(pos) + "\t" + str(frequ[1]) + "\n")
		outputFile.close()
		print("Output ready...")

	def processMultipleDramasAndGenerateOutputLemmas(self, originpath, resultpath):
		parser = DramaParser()

		for filename in os.listdir(originpath):
			print(filename + " processing starts...")
			dramaModel = parser.parse_xml(originpath + filename)
			print("DramaModel ready...")
			title = dramaModel._title
			self.processSingleDrama(originpath + filename)
			self.generateWordFrequenciesOutputLemmas(resultpath + title)

	def processEntireCorpusAndGenereateOutputLemmas(self, originpath):
		parser = DramaParser()
		totalText = "";
		for filename in os.listdir(originpath):
			print(filename + " processing starts...")
			dramaModel = parser.parse_xml(originpath + filename)
			
			for act in dramaModel._acts:
				for conf in act._configurations:
					for speech in conf._speeches:
						newText = unicode(speech._text.replace("–", ""))
						totalText = totalText + newText
		self.processText(totalText)
		self.generateWordFrequenciesOutputLemmas("../Word-Frequencies/EntireCorpus")



if __name__ == "__main__":
    main()