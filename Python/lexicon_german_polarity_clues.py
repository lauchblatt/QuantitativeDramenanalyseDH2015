# -*- coding: utf8 -*-

import os
import re
import collections
import locale
import sys
from lp_language_processor import *
from lexicon_dta_enhancement import *

def main():
	reload(sys)
	sys.setdefaultencoding('utf8')

	gpc = German_Polarity_Clues()
	gpc.initGPC()

class German_Polarity_Clues:
	def __init__(self):
		self._sentimentDict = {}
		self._sentimentDictLemmas = {}

	def readAndInitGPCAndLemmas(self, processor):
		self.initGPC()
		sentDictText = open("../SentimentAnalysis/TransformedLexicons/" + processor + "-Lemmas/GPC-Lemmas.txt")
		sentimentDict = {}
		lines = sentDictText.readlines()[1:]
		for line in lines:
			wordAndValues = line.split("\t")
			sentiments = {}
			sentiments["positive"] = int(wordAndValues[1])
			sentiments["negative"] = int(wordAndValues[2])
			sentiments["neutral"] = int(wordAndValues[3])
			sentimentDict[unicode((wordAndValues)[0])] = sentiments
		self._sentimentDictLemmas = sentimentDict

	def readAndInitGPCAndLemmasDTA(self, processor):
		self.initGPC()
		self.extendLexiconGPCDTA()
		sentDictText = open("../SentimentAnalysis/TransformedLexicons/" + processor + "-Lemmas/GPC-Lemmas-DTAExtended.txt")
		sentDictText = open("../SentimentAnalysis/TransformedLexicons/" + processor + "-Lemmas/GPC-Lemmas.txt")
		sentimentDict = {}
		lines = sentDictText.readlines()[1:]
		for line in lines:
			wordAndValues = line.split("\t")
			sentiments = {}
			sentiments["positive"] = int(wordAndValues[1])
			sentiments["negative"] = int(wordAndValues[2])
			sentiments["neutral"] = int(wordAndValues[3])
			sentimentDict[unicode((wordAndValues)[0])] = sentiments
		self._sentimentDictLemmas = sentimentDict

	def initGPC(self):

		sentDictTextNegative = open("../SentimentAnalysis/GermanPolarityClues/GermanPolarityClues-Negative-220311.tsv")
		sentDictTextNeutral = open("../SentimentAnalysis/GermanPolarityClues/GermanPolarityClues-Neutral-220311.tsv")
		sentDictTextPositive = open("../SentimentAnalysis/GermanPolarityClues/GermanPolarityClues-Positive-220311.tsv")

		sentimentDict = self.getSentimentDictGPC(sentDictTextNegative, sentDictTextNeutral, sentDictTextPositive)
		self._sentimentDict = sentimentDict
		self.removeNeutralWordsFromGPC()
		self.handleSpecialCases()
		self.removePhrasesFromSentimentDict()

	def removePhrasesFromSentimentDict(self):
		for word, sentiments in self._sentimentDict.items():
			if(len(word.split(" ")) > 1):
				del self._sentimentDict[word]

	def handleSpecialCases(self):
		for word, sentiments in self._sentimentDict.items():
			if(word.endswith(":")):
				del self._sentimentDict[word]
				self._sentimentDict[unicode(word.rstrip(":"))] = sentiments
			if(word.endswith("-")):
				del self._sentimentDict[word]
			if("/" in word):
				del self._sentimentDict[word]
				specialWords = word.split("/")
				for specialWord in specialWords:
					self._sentimentDict[unicode(specialWord)] = sentiments

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
			print unicode(info[0])
			print unicode(info[1])
		
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

		print(sentimentDictNeutral["der"])
		print(sentimentDictNegative["der"])
		sentimentDictNegative = self.removePositiveDoubles(sentimentDictNegative, sentimentDictPositive)
		sentimentDictNeutral = self.removeNeutralDoubles(sentimentDictNeutral, sentimentDictPositive, sentimentDictNegative)
		sentimentDict = {}
		sentimentDict.update(sentimentDictNegative)
		sentimentDict.update(sentimentDictPositive)
		sentimentDict.update(sentimentDictNeutral)
		print(sentimentDict["der"])

		return sentimentDict

	def removeNeutralWordsFromGPC(self):
		toDel = []
		for word in self._sentimentDict:
			if(self._sentimentDict[word]["neutral"] is 1):
				toDel.append(word)

		for wordToDel in toDel:
			del self._sentimentDict[wordToDel]
	
	def lemmatizeDictGPC(self, processor):
		lp = Language_Processor(processor)
		newSentimentDict = {}
		i = 0

		print("start Lemmatisation")
		for word,value in self._sentimentDict.iteritems():
			lemma = lp._processor.getLemma(word)
			if lemma in newSentimentDict:
				if(self.getPolarityChange(value, newSentimentDict[lemma])):
					i = i + 1
					"""
					print("Lemma:")
					print(lemma)
					print("Alte Werte:")
					print(newSentimentDict[lemma])
					print("Neue Werte:")
					print(value)
					print("Gewählter Wert:")
					print(self.getChosenValues(value, newSentimentDict[lemma]))
					"""
					chosenValues = self.getChosenValues(value, newSentimentDict[lemma], lemma)
					newSentimentDict[lemma] = chosenValues
			else:
				newSentimentDict[lemma] = value
		print ("Lemmatisation finished")
		self._sentimentDictLemmas = newSentimentDict

	def getChosenValues(self, newValues, oldValues, word):
		if(newValues["neutral"] > oldValues["neutral"]):
			return oldValues
		else:
			if(newValues["positive"] > oldValues["positive"]):
				return newValues
			else:
				return oldValues

	def getPolarityChange(self, newValues, oldValues):
		positive = (oldValues["positive"] is newValues["positive"])
		negative = (oldValues["negative"] is newValues["negative"])
		neutral = (oldValues["neutral"] is newValues["neutral"])
		if(positive and negative and neutral):
			return False
		else:
			return True
	
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

	def createOutputGPC(self, sentimentDict, dataName):
		outputFile = open(dataName + ".txt", "w")
		firstLine = "word\tpositive\tnegative\tneutral"
		outputFile.write(firstLine)

		for word in sentimentDict:
			info = sentimentDict[word]
			line = "\n" + word + "\t" + str(info["positive"]) + "\t" + str(info["negative"]) + "\t" + str(info["neutral"])
			outputFile.write(line)
		outputFile.close()

	def createExtendedOutputDTA(self):
		self.initGPC()
		print("###")
		print(len(self._sentimentDict))
		self.extendLexiconGPCDTA()
		print("###")
		print(len(self._sentimentDict))
		self.createOutputGPC(self._sentimentDict, "../SentimentAnalysis/TransformedLexicons/GPC-Token-DTAExtended")
		self.lemmatizeDictGPC("treetagger")
		print("###")
		print(len(self._sentimentDictLemmas))
		self.createOutputGPC(self._sentimentDictLemmas, "../SentimentAnalysis/TransformedLexicons/treetagger-Lemmas/GPC-Lemmas-DTAExtended")
		self.lemmatizeDictGPC("textblob")
		print(len(self._sentimentDictLemmas))
		self.createOutputGPC(self._sentimentDictLemmas, "../SentimentAnalysis/TransformedLexicons/textblob-Lemmas/GPC-Lemmas-DTAExtended")

	def extendLexiconGPCDTA(self):
		dta = DTA_Handler()
		self._sentimentDict = dta.extendSentimentDictDTA(self._sentimentDict, "GPC")

	def resetAllFiles(self):
		self.createSentimentDictFileGPCToken()
		self.createSentimentDictFileGPCLemmas("treetagger")
		self.createSentimentDictFileGPCLemmas("textblob")

	def createSentimentDictFileGPCToken(self):
		self.initGPC()
		self.createOutputGPC(self._sentimentDict, "../SentimentAnalysis/TransformedLexicons/GPC-Token")

	def createSentimentDictFileGPCLemmas(self, processor):
		self.initGPC()
		self.lemmatizeDictGPC(processor)
		self.createOutputGPC(self._sentimentDictLemmas, "../SentimentAnalysis/TransformedLexicons/" + processor + "-Lemmas/GPC-Lemmas")

if __name__ == "__main__":
    main()