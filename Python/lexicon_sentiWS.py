# -*- coding: utf8 -*-

import os
import re
import collections
import locale
import sys
from lp_language_processor import *

def main():
	reload(sys)
	sys.setdefaultencoding('utf8')

	sentiWs = Senti_WS()
	sentiWs.createSentimentDictFileSentiWSLemmas("treetagger")

class Senti_WS:

	def __init__(self):
		self._sentimentDict = {}
		self._sentimentDictLemmas = {}


	def readAndInitSentiWSAndLemmas(self, processor):
		self.initSentiWS()
		sentimentDictText = open("../SentimentAnalysis/TransformedLexicons/" + processor + "-Lemmas/SentiWS-Lemmas.txt")
		sentimentDict = {}

		for line in sentimentDictText:
			wordAndValue = line.split("\t")
			word = wordAndValue[0]
			value = float(wordAndValue[1].rstrip())
			sentimentDict[unicode(word)] = value

		self._sentimentDictLemmas = sentimentDict

	def initSentiWS (self):
		sentDictTextNegative = open("../SentimentAnalysis/SentiWS/SentiWS_v1.8c_Negative.txt")
		sentDictTextPositive = open("../SentimentAnalysis/SentiWS/SentiWS_v1.8c_Positive.txt")

		sentimentDictNegative = self.getSentimentDictSentiWS(sentDictTextNegative)

		sentimentDictPositiv = self.getSentimentDictSentiWS(sentDictTextPositive)

		sentimentDictNegative.update(sentimentDictPositiv)
		self._sentimentDict = sentimentDictNegative

	def getSentimentDictSentiWS (self, sentimentDictText):
		sentimentDict = {}
		sentimentList = []

		for line in sentimentDictText:
			firstWord = line.split("|")[0]

			tabSplit = line.split("\t")
			number = float(tabSplit[1].rstrip())

			if(unicode(firstWord) in sentimentDict):
				higherSentiment = self.getHigherSentimentValue(number, sentimentDict[unicode(firstWord)])
				sentimentDict[unicode(firstWord)] = higherSentiment
			else:
				sentimentDict[unicode(firstWord)] = number
			
			if 0 <= 2 < len(tabSplit):
				flexions = tabSplit[2]
				seperatedFlexions = flexions.split(",")

				for flex in seperatedFlexions:
					flex = flex.rstrip()

					if(unicode(flex) in sentimentDict):
						higherSentiment = self.getHigherSentimentValue(number, sentimentDict[unicode(flex)])
						sentimentDict[unicode(flex)] = higherSentiment
					else:
						sentimentDict[unicode(flex)] = number

		return sentimentDict

	def lemmatizeDict(self, processor):
		lp = Language_Processor(processor)
		newSentimentDict = {}
		print("start Lemmatisation")
		lemmaTokenPairs = {}
		
		for word,value in self._sentimentDict.iteritems():
			lemma = lp._processor.getLemma(word)
			
			if lemma in newSentimentDict:
				newScore = value
				oldScore = newSentimentDict[lemma]
				higherScore = self.getHigherSentimentValue(newScore, oldScore)
				oldToken = lemmaTokenPairs[lemma]
				newSentimentDict[lemma] = higherScore
			else:
				newSentimentDict[lemma] = value
				lemmaTokenPairs[lemma] = word
		
		print("Lemmatisation finished")
		self._sentimentDictLemmas = newSentimentDict

	def createOutput(self, sentimentDict, dataName):
		outputFile = open(dataName + ".txt", "w")

		for word in sentimentDict:
			outputFile.write(word + "\t" + str(sentimentDict[word]) +"\n")

		outputFile.close()

	def getHigherSentimentValue(self, newScore, oldScore):
		if(abs(newScore) > abs(oldScore)):
			return newScore
		else:
			return oldScore

	def createSentimentDictFileSentiWSToken(self):
		self.initSentiWS()
		self.createOutput(self._sentimentDict, "../SentimentAnalysis/TransformedLexicons/SentiWS-TokenTest")
		
	
	def createSentimentDictFileSentiWSLemmas(self, processor):
		self.initSentiWS()
		self.lemmatizeDict(processor)
		self.createOutput(self._sentimentDictLemmas, "../SentimentAnalysis/TransformedLexicons/" + processor + "-Lemmas/SentiWS-Lemmas")

if __name__ == "__main__":
    main()