#coding: utf8

import os
import re
import collections
import locale
import sys
from sa_models import *
import pprint
import treetaggerwrapper

def main():
	reload(sys)
	sys.setdefaultencoding('utf8')

	text = "Das ist ein schöner Tag. Das ist ein großer, aber schwerer Erfolg"
	tt = Tree_Tagger()
	tt.processTextFully(text)


class Tree_Tagger:

	def __init__(self):

		self._plainText = ""
		self._filteredText = ""

		self._tagger = None

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

	def processText(self, plainText):
		self._plainText = plainText
		self._filteredText = self.filterText(plainText)
		self._tagger = treetaggerwrapper.TreeTagger(TAGLANG='de')
		print("Tagger ready...")
		self.tagText()
		print("Tokens ready...")
		print("Tags ready...")
		print("Lemmas ready...")
		print("Lemmas With LanguageInfo ready...")

	def processTextFully(self, plainText):
		self._plainText = plainText
		self._filteredText = self.filterText(plainText)
		self._tagger = treetaggerwrapper.TreeTagger(TAGLANG='de')
		print("Tagger ready...")
		self.tagText()
		print("Tokens ready...")
		print("Tags ready...")
		print("Lemmas ready...")
		print("Lemmas With LanguageInfo ready...")
		self.createLemmaAndPOSDict()
		print(self._lemmaAndPOSDict)
		print("LemmasANDPOSDict ready...")
		self.combineLemmasPOSTokens()
		print("LemmasAndPOSAndTokensDict ready...")	
	
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

	#TODO getLemma, getLemmas
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

	def tagText(self):
		tagsTabSeperated = self._tagger.tag_text(self._filteredText)
		tags = self.removeTabSeperation(tagsTabSeperated)
		tags = self.filterPunctuationMarks(tags)
		for tag in tags:
			token = tag[0]
			pos = tag[1]
			lemma = tag[2]
			lemmaWithLanguageInfo = (lemma, (token, pos))
			self._tokens.append(token)
			self._lemmas.append(lemma)
			self._tokensAndPOS.append((token, pos))
			self._lemmasAndPOS.append((lemma, pos))
			self._lemmasWithLanguageInfo.append(lemmaWithLanguageInfo)

	def removeTabSeperation(self, tagsTabSeperated):
		newTags = []
		for tag in tagsTabSeperated:
			tags = tag.split("\t")
			newTags.append(tags)
		return newTags

	def filterPunctuationMarks(self, tags):
		print "Start Punctuation Filter"
		newTags = []
		for tag in tags:
			if(not tag[1].startswith("$") or tag[1] == "SEN"):
				newTags.append(tag)
		
		return newTags
	
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

	def initStopWords(self):
		stopwords_text = open("stopwords_german.txt")
		for line in stopwords_text:
			stopword = unicode(line.strip())
			self._stopwords.append(stopword)
			tagsTabSeperated = self._tagger.tag_text(stopword)
			tags = tagsTabSeperated[0].split("\t")
			stopword_lemmatized = tags[2]

			print(stopword_lemmatized)
			self._stopwords_lemmatized.append(stopword_lemmatized)

	def removeStopWordsFromLemmas(self):
		self.initStopWords()
		lemmasCopy = list(self._lemmas)
		self._lemmasWithoutStopwords = self.removeStopwordsFromList(lemmasCopy)
	
	def removeStopwordsFromTokens(self):
		self.initStopWords()
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


if __name__ == "__main__":
    main()