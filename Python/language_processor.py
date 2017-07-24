#coding: utf8

import os
from textblob_de import *
from textblob_de.lemmatizers import PatternParserLemmatizer
import sys
import nltk
from nltk import *
from drama_parser import *
from drama_output import *
from collections import defaultdict

def main():
	reload(sys)
	sys.setdefaultencoding('utf8')

	parser = DramaParser()
	dramaModel = parser.parse_xml("../Lessing-Dramen/less-Der_Freigeist_k.xml")

	"""
	for filename in os.listdir("../Lessing-Dramen/"):
		print(filename)
		parser = DramaParser()
		dramaModel = parser.parse_xml("../Lessing-Dramen/" + filename)

	"""

	for act in dramaModel._acts:
		for conf in act._configurations:
			for speech in conf._speeches:
				print ("SPEECH")
				print unicode(speech._text)

	#lp = Language_Processor()

	#lp.processMultipleDramasAndGenerateOutputLemmas("../Lessing-Dramen/", "../Word-Frequencies/Test/")
	

class Language_Processor:

	def __init__(self):
		
		self._plainText = ""
		self._filteredText = ""
		self._textBlob = None
		self._tokens = []
		self._tokensAndPOS = []
		self._lemmas = []
		self._lemmasWithoutStopwords = []
		self._lemmasAndPOS = []
		self._lemmaAndPOSDict = {}

		self._lemmasWithLanguageInfo = []

		self._lemmasAndPOSAndTokensDict = {}

		self._stopwords = []
		self._stopwords_lemmatized = []

		self._currentDramaName = ""
		self._tokensWithoutStopwords = []
		
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
		print("Lemmas With LanguageInfo ready...")

	def processTextTokens(self, plainText):
		self._plainText = plainText
		self._filteredText = self.filterText(plainText)
		self._textBlob = TextBlobDE(self._filteredText)
		print("TextBlob ready...")
		self._tokens = self._textBlob.words
		print("Tokens ready...")

	def processTextFully(self, plainText):
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
		print("Lemmas With LanguageInfo ready...")
		self.createLemmaAndPOSDict()
		print("LemmasANDPOSDict ready...")
		self.combineLemmasPOSTokens()
		print("LemmasAndPOSAndTokensDict ready...")

		"""
		print(len(self._lemmas))
		print(len(self._lemmasAndPOS))
		print(len(self._lemmasWithLanguageInfo))
		print(len(self._lemmaAndPOSDict))
		print(len(self._lemmasAndPOSAndTokensDict))

		print(self._lemmas)
		print(self._lemmasAndPOS)
		print(self._lemmasWithLanguageInfo)
		print(self._lemmaAndPOSDict)
		print(self._lemmasAndPOSAndTokensDict)
		"""
		
		self.removeStopWordsFromLemmas()
		#print("StopWords removed...")


	def getLemma(self, word):
		blob = TextBlobDE(unicode(word))
		lemmas = blob.words.lemmatize()
		if(len(lemmas) > 1):
			lemmasString = " ".join(lemmas)
			return lemmasString
		else: 
			return lemmas[0]

	def getLemmas(self, wordsAsString):
		blob = TextBlobDE(unicode(wordsAsString))
		lemmas = blob.words.lemmatize()
		return lemmas

	def filterText(self, text):
		newText = ""
		newText = unicode(text.replace("–", ""))
		newText = unicode(newText.replace("'", ""))
		newText = unicode(newText.replace("«", ""))
		newText = unicode(newText.replace("»", ""))
		newText = unicode(newText.replace("[", ""))
		newText = unicode(newText.replace("]", ""))
		newText = unicode(newText.replace("...", ""))
		newText = unicode(newText.replace("..", ""))

		return newText


	def processSingleDrama(self, path):
		parser = DramaParser()
		dramaModel = parser.parse_xml(path)
		self._currentDramaName = dramaModel._title
		print("dramaModel ready...")
		text = ""
		#"""
		for act in dramaModel._acts:
			for conf in act._configurations:
				for speech in conf._speeches:
					text = text + speech._text

		print("Text ready...")
		self.processTextFully(text)

	def processSingleDramaTokens(self, path):
		parser = DramaParser()
		dramaModel = parser.parse_xml(path)
		self._currentDramaName = dramaModel._title
		print("dramaModel ready...")
		text = ""
		#"""
		for act in dramaModel._acts:
			for conf in act._configurations:
				for speech in conf._speeches:
					text = text + speech._text

		print("Text ready...")
		self.processTextTokens(text)

	def lemmatize(self):
		self._lemmas = self._textBlob.words.lemmatize()
		self._lemmasAndPOS = []
		self._lemmasWithLanguageInfo = []
		
		for i in range(0, len(self._lemmas)):
			lemmaAndPOS = (self._lemmas[i], self._tokensAndPOS[i][1])
			self._lemmasAndPOS.append(lemmaAndPOS)

			lemmaAndTokenPOS = (self._lemmas[i], (self._tokensAndPOS[i][0], self._tokensAndPOS[i][1]))
			self._lemmasWithLanguageInfo.append(lemmaAndTokenPOS)

	# One Lemma can have multiple POS
	def createLemmaAndPOSDict(self):
		lemmasSet = set(self._lemmas)
		for lemma in lemmasSet:
			POSList = []
			for compareLemma in self._lemmasAndPOS:
				if(lemma == compareLemma[0]):
					if(compareLemma[1] not in POSList):
						POSList.append(compareLemma[1])
			self._lemmaAndPOSDict[lemma] = POSList
	
	def combineLemmasPOSTokens(self):
		for lemma, POS in self._lemmaAndPOSDict.iteritems():
			tokensOfLemma = []
			for languageInfo in self._lemmasWithLanguageInfo:
				if(lemma == languageInfo[0]):
					token = languageInfo[1][0]
					if not self.isTokenOfLemma(tokensOfLemma, token):
						tokensOfLemma.append(token)
			#lemmaAndPOSAndTokens = (lemma, POS, (tokensOfLemma))
			#self._lemmasAndPOSAndTokens.append(lemmaAndPOSAndTokens)
			self._lemmasAndPOSAndTokensDict[lemma] = (POS, tokensOfLemma)

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
		self._lemmasWithoutStopwords = self.removeStopwordsFromList(lemmasCopy)
	
	def removeStopwordsFromTokens(self):
		tokensCopy = list(self._tokens)
		self._tokensWithoutStopwords = self.removeStopwordsFromList(tokensCopy)

	def removeStopwordsFromList(self, wordList):
		for stopword in self._stopwords:
			while stopword.lower() in wordList:
				wordList.remove(stopword.lower())
			while stopword.title() in wordList:
				wordList.remove(stopword.title())

		for stopword in self._stopwords_lemmatized:
			while stopword.lower() in wordList:
				wordList.remove(stopword.lower())
			while stopword.title() in wordList:
				wordList.remove(stopword.title())
		return wordList

	"""
	def removeStopwordsFromWordFrequencies(self, wordFrequencies):
		for wordFrequ in wordFrequencies:
			word = wordFrequ[0]
			if (word.lower() in self._stopwords) or (word.title() in self._stopwords):
	"""

if __name__ == "__main__":
    main()