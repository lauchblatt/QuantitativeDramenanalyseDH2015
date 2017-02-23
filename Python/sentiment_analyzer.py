#coding: utf8

import os
import re
import collections
import locale

def main():
	sa = Sentiment_Analyzer()
	sa.initDict()
	"""
	si = sa.calcSentimentScorePerText("Anf\xe4lligkeit".decode('cp1252').encode('utf8'))
	print(si.sentimentBearingWords)
	"""
	print (sa.sentimentDict)

class Sentiment_Analyzer:

	sentimentDict = {}

	def initDict (self):

		sentDictTextNegative = open("../SentimentAnalysis/SentiWS_v1.8c_Negative.txt")
		sentDictTextPositive = open("../SentimentAnalysis/SentiWS_v1.8c_Positive.txt")

		sentimentDictNegative = self.getSentimentDict(sentDictTextNegative)
		sentimentDictPositiv = self.getSentimentDict(sentDictTextPositive)

		sentimentDictNegative.update(sentimentDictPositiv)
		self.sentimentDict = sentimentDictNegative

	def calcSentimentScorePerText (self, text):

		text = text.strip()
		words = text.split(" ")

		sentimentScore = 0
		sentimentInformation = Sentiment_Information()
		sentimentInformation.sentimentBearingWords = []

		for word in words:
			word = word.strip(".,:?!();-'\"")
			"""
			word = word.replace("\xe4", "\xc3\xa4")
			"""
			"""
			word = str(word.decode('iso-8859-1').encode('utf8'))
			"""
			sentimentScorePerWord = self.getSentimentScorePerWord(word)
			sentimentScore = sentimentScore + sentimentScorePerWord

			if(sentimentScorePerWord != 0):
				#OrderedDictionary necessary
				pair = (word, sentimentScorePerWord)
				sentimentInformation.sentimentBearingWords.append(pair)

		sentimentInformation.sentimentScore = sentimentScore

		return sentimentInformation

	
	def getSentimentScorePerWord (self, word):
		scoreString = self.sentimentDict.get(word)
		
		if (scoreString is None):
			return 0

		scoreFloat = float(scoreString)
		return scoreFloat

	def getSentimentDict (self, sentimentDictText):
		
		sentimentDict = {}

		for line in sentimentDictText:
			firstWord = line.split("|")[0]

			tabSplit = line.split("\t")
			number = tabSplit[1].rstrip()

			sentimentDict[firstWord.decode('utf-8').encode('iso-8859-1')] = number

			if 0 <= 2 < len(tabSplit):
				flexions = tabSplit[2]
				seperatedFlexions = flexions.split(",")

				for flex in seperatedFlexions:
					flex = flex.rstrip()
					sentimentDict[flex.decode('utf-8').encode('iso-8859-1')] = number

		return sentimentDict

class Sentiment_Information:

	sentimentScore = 0
	sentimentBearingWords = []


if __name__ == "__main__":
    main()
