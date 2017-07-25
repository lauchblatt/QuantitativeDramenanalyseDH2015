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

	gpc = German_Polarity_Clues()
	gpc.initGPC()
	gpc.lemmatizeDictGPC()
	print(len(gpc._sentimentDict))
	print(len(gpc._sentimentDictLemmas))

class German_Polarity_Clues:
	def __init__(self):
		self._sentimentDict = {}
		self._sentimentDictLemmas = {}

	def initGPC(self):

		sentDictTextNegative = open("../SentimentAnalysis/GermanPolarityClues/GermanPolarityClues-Negative-220311.tsv")
		sentDictTextNeutral = open("../SentimentAnalysis/GermanPolarityClues/GermanPolarityClues-Neutral-220311.tsv")
		sentDictTextPositive = open("../SentimentAnalysis/GermanPolarityClues/GermanPolarityClues-Positive-220311.tsv")

		sentimentDict = self.getSentimentDictGPC(sentDictTextNegative, sentDictTextNeutral, sentDictTextPositive)
		self._sentimentDict = sentimentDict
		self.removeNeutralWordsFromGPC()

	def getSentimentDictGPC(self, textNegative, textNeutral, textPositive):
		linesNegative = textNegative.readlines()
		linesPositive = textPositive.readlines()
		linesNeutral = textNeutral.readlines()

		sentimentDictNegative = {}
		sentimentDictPositive = {}
		sentimentDictNeutral = {}

		i = 0

		for line in linesNegative:
			info = line.split("\t")
			infoPerWord = {}
			infoPerWord["negative"] = 1
			infoPerWord["positive"] = 0
			infoPerWord["neutral"] = 0
			sentimentDictNegative[unicode(info[0])] = infoPerWord
			sentimentDictNegative[unicode(info[1])] = infoPerWord
		
		for line in linesPositive:
			info = line.split("\t")
			infoPerWord = {}
			infoPerWord["negative"] = 0
			infoPerWord["positive"] = 1
			infoPerWord["neutral"] = 0
			sentimentDictPositive[unicode(info[0])] = infoPerWord
			sentimentDictPositive[unicode(info[1])] = infoPerWord
		
		for line in linesNeutral[19:]:
			info = line.split("\t")
			infoPerWord = {}
			infoPerWord["negative"] = 0
			infoPerWord["positive"] = 0
			infoPerWord["neutral"] = 1
			sentimentDictNeutral[unicode(info[0])] = infoPerWord
			sentimentDictNeutral[unicode(info[1])] = infoPerWord

		sentimentDictNegative = self.removePositiveDoubles(sentimentDictNegative, sentimentDictPositive)
		sentimentDictNeutral = self.removeNeutralDoubles(sentimentDictNeutral, sentimentDictPositive, sentimentDictNegative)
		sentimentDict = {}
		sentimentDict.update(sentimentDictNegative)
		sentimentDict.update(sentimentDictPositive)
		sentimentDict.update(sentimentDictNeutral)

		return sentimentDict

	def removeNeutralWordsFromGPC(self):
		toDel = []
		for word in self._sentimentDict:
			if(self._sentimentDict[word]["neutral"] is 1):
				toDel.append(word)

		for wordToDel in toDel:
			del self._sentimentDict[wordToDel]
	
	def lemmatizeDictGPC(self):
		lp = Language_Processor()
		newSentimentDict = {}
		i = 0
		print("start Lemmatisation")
		for word,value in self._sentimentDict.iteritems():
			lemma = lp.getLemma(word)
			if lemma in newSentimentDict:
				i = i + 1
			else:
				newSentimentDict[lemma] = value

		print ("Lemmatisation finished")
		print i
		self._sentimentDictLemmas = newSentimentDict

	def removePositiveDoubles(self, sentimentDictNegative, sentimentDictPositive):
		toDel = []
		for word in sentimentDictNegative:
			if(word in sentimentDictPositive):
				toDel.append(word)
		
		for wordToDel in toDel:
			del sentimentDictNegative[wordToDel]
		return sentimentDictNegative

	def removeNeutralDoubles(self, sentimentDictNeutral, sentimentDictPositive, sentimentDictNegative):
		toDel = []

		for word in sentimentDictNeutral:
			if(word in sentimentDictPositive or word in sentimentDictNegative):
				toDel.append(word)

		for wordToDel in toDel:
			del sentimentDictNeutral[wordToDel]
		return sentimentDictNeutral

if __name__ == "__main__":
    main()