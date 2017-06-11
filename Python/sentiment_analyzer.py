# -*- coding: utf8 -*-

import os
import re
import collections
import locale
import sys
from language_processor import *

def main():
	reload(sys)
	sys.setdefaultencoding('utf8')

	lexiconReader = Lexicon_Reader()
	lexiconReader.initSingleDict("SentiWS")

	#print(lexiconReader._sentimentDict)
	lexiconReader.lemmmatizeDict()

class Lexicon_Reader:

	def __init__(self):
		self._sentimentDict = {}

	def initSingleDict (self, lexicon):
		if (lexicon == "SentiWS"):
			self.initSentiWS()
		else:
			return("Kein korrekter Lexikonname wurde übergeben")

	def lemmmatizeDict(self):
		lp = Language_Processor()
		newSentimentDict = {}

		for word,value in self._sentimentDict.iteritems():
			#print word
			"""
			lp.processText(word)
			languageInfo = lp._lemmasWithLanguageInfo[0]
			newSentimentDict[word] = (languageInfo, value)
			"""
			#lp.processText(word)
			lemma = lp.getLemma(word)
			#print lemma
			lemmaList = [unicode(lemma)]

			
			if lemma in newSentimentDict:
				print("###########")
				print("Originalwort: " + (word))
				print("Lemma: " + (lemma))
				print(lemmaList)
			

			newSentimentDict[lemma] = value
			
			#print (lemma + " " + str(value))
		print(len(self._sentimentDict))
		print(len(newSentimentDict))
		"""
		for word in self._sentimentDict:
			print word
		for key in newSentimentDict:
			print key
		"""


	
	def initSentiWS (self):
		print("initSentiWS")
		sentDictTextNegative = open("../SentimentAnalysis/SentiWS_v1.8c_Negative.txt")
		sentDictTextPositive = open("../SentimentAnalysis/SentiWS_v1.8c_Positive.txt")

		sentimentDictNegative = self.getSentimentDictSentiWS(sentDictTextNegative)
		sentimentDictPositiv = self.getSentimentDictSentiWS(sentDictTextPositive)

		sentimentDictNegative.update(sentimentDictPositiv)
		self._sentimentDict = sentimentDictNegative

	def getSentimentDictSentiWS (self, sentimentDictText):
		print("getSentimentDictSentiWS")
		sentimentDict = {}

		for line in sentimentDictText:
			firstWord = line.split("|")[0]

			tabSplit = line.split("\t")
			number = tabSplit[1].rstrip()

			sentimentDict[unicode(firstWord)] = number
			"""
			if 0 <= 2 < len(tabSplit):
				flexions = tabSplit[2]
				seperatedFlexions = flexions.split(",")

				for flex in seperatedFlexions:
					flex = flex.rstrip()
					sentimentDict[unicode(flex)] = number
			"""

		return sentimentDict

if __name__ == "__main__":
    main()