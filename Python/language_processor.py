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

	lp = Language_Processor()

	lp.processSingleDrama("../Lessing-Dramen/less-Philotas_t.xml")
	
	lp.generateWordFrequenciesOutputLemmas("../Word-Frequencies/test")
	
	#lp.processEntireCorpusAndGenereateOutputLemmas("../Lessing-Dramen/")
	

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

		self._wordFrequencies = []
		self._stopwords = []
		self._stopwords_lemmatized = []
		self.initStopWords()

	def processText(self, plainText):
		self._plainText = plainText
		self._filteredText = self.filterText(plainText)
		self._textBlob = TextBlobDE(self._filteredText)
		#print("TextBlob ready...")
		self._tokens = self._textBlob.words
		#print("Tokens ready...")
		self._tokensAndPOS = self._textBlob.tags
		#print("Tags ready...")
		self.lemmatize()
		#print("Lemmas ready...")
		#print("Lemmas With LanguageInfo ready...")
		self.createLemmaAndPOSDict()
		#print("LemmasANDPOSDict ready...")
		self.combineLemmasPOSTokens()
		#print("LemmasAndPOSAndTokensDict ready...")

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
		self.calcWordFrequencies()
		#print("Frequencies calculated...")


	def getLemma(self, word):
		blob = TextBlobDE(unicode(word))
		lemma = blob.words.lemmatize()[0]
		return lemma

	def filterText(self, text):
		newText = ""
		newText = unicode(text.replace("–", ""))
		newText = unicode(newText.replace("'", ""))
		newText = unicode(newText.replace("«", ""))
		newText = unicode(newText.replace("»", ""))

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
					newText = text + speech._text
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

		outputFile.write("Number of all words " + str(len(self._lemmasWithoutStopwords)) + "\n")
		outputFile.write("Nummber of different lemmas " + str(len(self._wordFrequencies)) + "\n\n")

		outputFile.write("Lemma" + "\t" + "POS" + "\t" + "Frequency" + "\t" + "Tokens" +"\n")
		for frequ in self._wordFrequencies:
			lemma = frequ[0]
			POS = self._lemmasAndPOSAndTokensDict[lemma][0]
			tokens = self._lemmasAndPOSAndTokensDict[lemma][1]
			outputFile.write(str(lemma) + "\t" + ', '.join(POS) + "\t" + str(frequ[1]) + "\t" + ', '.join(tokens) + "\n")
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