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
	cd = CD()
	cd.resetAllFiles()


class CD:
	def __init__(self):
		self._sentimentDict = {}
		self._sentimentDictLemmas = {}

	def readAndInitCDAndLemmas(self, processor):
		self.initCD()
		sentDictText = open("../SentimentAnalysis/TransformedLexicons/" + processor + "-Lemmas/CD-Lemmas.txt")
		sentimentDict = {}
		lines = sentDictText.readlines()[1:]
		for line in lines:
			wordAndValues = line.split("\t")
			sentiments = {}
			sentiments["positive"] = float(wordAndValues[1])
			sentiments["negative"] = float(wordAndValues[2])
			sentiments["neutral"] = float(wordAndValues[3])
			sentimentDict[unicode((wordAndValues)[0])] = sentiments
		self._sentimentDictLemmas = sentimentDict

	def readAndInitCDAndLemmasDTA(self, processor):
		self.initCD()
		self.extendLexiconCDDTA()
		sentDictText = open("../SentimentAnalysis/TransformedLexicons/" + processor + "-Lemmas/CD-Lemmas-DTAExtended.txt")
		sentimentDict = {}
		lines = sentDictText.readlines()[1:]
		for line in lines:
			wordAndValues = line.split("\t")
			sentiments = {}
			sentiments["positive"] = float(wordAndValues[1])
			sentiments["negative"] = float(wordAndValues[2])
			sentiments["neutral"] = float(wordAndValues[3])
			sentimentDict[unicode((wordAndValues)[0])] = sentiments
		self._sentimentDictLemmas = sentimentDict

	def initCD(self):
		sentDictText = open("../SentimentAnalysis/CD/cd.txt")
		sentimentDict = self.getSentimentDictCD(sentDictText)
		self._sentimentDict = sentimentDict
		self.removePhrasesFromSentimentDict()
		self._sentimentDict = self.removeNeutralWordsFromCD(self._sentimentDict)
		
	def removePhrasesFromSentimentDict(self):
		for word,sentiments in self._sentimentDict.items():
			if(len(word.split(" ")) > 1):
				del self._sentimentDict[word]

	def getSentimentDictCD(self, sentimentDictText):
		lines = sentimentDictText.readlines()
		sentimentDict = {}
		i = 0
		for line in lines:
			info = line.split(" ")
			word = info[0]
			# catch Phrases
			word = word.replace("_", " ")
			sentiment = info[1]
			sentimentInfo = sentiment.split("=")
			infoPerWord = {}
			
			
			if(sentimentInfo[0] == "POS"):
				infoPerWord["positive"] = float(sentimentInfo[1])
			else:
				infoPerWord["positive"] = 0
			if(sentimentInfo[0] == "NEG"):
				infoPerWord["negative"] = float(sentimentInfo[1])
			else:
				infoPerWord["negative"] = 0
			if(sentimentInfo[0] == "NEU"):
				infoPerWord["neutral"] = float(sentimentInfo[1])
			else:
				infoPerWord["neutral"] = 0

			
			if(unicode(word) in sentimentDict):
				sentiments = self.getBetterSentimentValuesCD(infoPerWord, sentimentDict[unicode(word)], word)
				infoPerWord = sentiments
			
			sentimentDict[unicode(word)] = infoPerWord

		return sentimentDict

	def lemmatizeDictCD(self, processor):
		lp = Language_Processor(processor)
		newSentimentDict = {}
		print("start Lemmatisation")
		for word,value in self._sentimentDict.iteritems():
			lemma = lp._processor.getLemma(word)
			if lemma in newSentimentDict:			
				sentiments = self.getBetterSentimentValuesCD(value, newSentimentDict[lemma], lemma)
				newSentimentDict[lemma] = sentiments
			else:
				newSentimentDict[lemma] = value

		print ("Lemmatisation finished")
		self._sentimentDictLemmas = newSentimentDict

	def createOutputCD(self, sentimentDict, dataName):
		outputFile = open(dataName + ".txt", "w")
		firstLine = "word\tpositive\tnegative\tneutral"
		outputFile.write(firstLine)

		for word in sentimentDict:
			info = sentimentDict[word]
			line = "\n" + word + "\t" + str(info["positive"]) + "\t" + str(info["negative"]) + "\t" + str(info["neutral"])
			outputFile.write(line)
		outputFile.close()

	def removeNeutralWordsFromCD(self, cdDict):
		wordsToDel = []
		for word in cdDict:
			sentiments = cdDict[word]
			if(sentiments["positive"] == 0 and sentiments["negative"] == 0):
				wordsToDel.append(word)
		
		for word in wordsToDel:
			del cdDict[word]
		return cdDict

	def getHigherSentimentValuesCD(self, newSentiments, oldSentiments):
		sentiments = {}
		sentiments["positive"] = self.getHigherSentimentValue(newSentiments["positive"], oldSentiments["positive"])
		sentiments["negative"] = self.getHigherSentimentValue(newSentiments["negative"], oldSentiments["negative"])
		sentiments["neutral"] = self.getHigherSentimentValue(newSentiments["neutral"], oldSentiments["neutral"])
		return sentiments

	def getBetterSentimentValuesCD(self, newSentiments, oldSentiments, word):
		# if somethin is neutral take the other
		highestSentimentValues = self.getHigherSentimentValuesCD(newSentiments, oldSentiments)

		polarityChange = (highestSentimentValues["positive"] != 0 and highestSentimentValues["negative"] != 0)
		neutralityChange = (highestSentimentValues["neutral"] != 0 \
			and (highestSentimentValues["positive"] != 0 or highestSentimentValues["negative"] != 0))
		if(highestSentimentValues["positive"] != 0 or highestSentimentValues["negative"] != 0):
			if(highestSentimentValues["positive"] >= highestSentimentValues["negative"]):
				highestSentimentValues["negative"] = 0
				highestSentimentValues["neutral"] = 0
				return highestSentimentValues
			else:
				highestSentimentValues["positive"] = 0
				highestSentimentValues["neutral"] = 0
				return highestSentimentValues
		else:
			return highestSentimentValues

	def getSentimentCD(self, sentiments):
		if(sentiments["positive"] != 0):
			return "POS"
		if(sentiments["negative"] != 0):
			return "NEG"
		if(sentiments["neutral"] != 0):
			return "NEU"

	def getHigherSentimentValue(self, newScore, oldScore):
		if(abs(newScore) > abs(oldScore)):
			return newScore
		else:
			return oldScore
	
	def createExtendedOutputDTA(self):
		self.initCD()
		print("###")
		print(len(self._sentimentDict))
		self.extendLexiconCDDTA()
		print("###")
		print(len(self._sentimentDict))
		self.createOutputCD(self._sentimentDict, "../SentimentAnalysis/TransformedLexicons/CD-Token-DTAExtended")
		self.lemmatizeDictCD("treetagger")
		print("###")
		print(len(self._sentimentDictLemmas))
		self.createOutputCD(self._sentimentDictLemmas, "../SentimentAnalysis/TransformedLexicons/treetagger-Lemmas/CD-Lemmas-DTAExtended")
		self.lemmatizeDictCD("textblob")
		print(len(self._sentimentDictLemmas))
		self.createOutputCD(self._sentimentDictLemmas, "../SentimentAnalysis/TransformedLexicons/textblob-Lemmas/CD-Lemmas-DTAExtended")

	def extendLexiconCDDTA(self):
		dta = DTA_Handler()
		self._sentimentDict = dta.extendSentimentDictDTA(self._sentimentDict)

	def resetAllFiles(self):
		self.createSentimentDictFileCDToken()
		self.createSentimentDictFileCDLemmas("treetagger")
		self.createSentimentDictFileCDLemmas("textblob")

	def createSentimentDictFileCDToken(self):
		self.initCD()
		self.createOutputCD(self._sentimentDict, "../SentimentAnalysis/TransformedLexicons/CD-Token")

	def createSentimentDictFileCDLemmas(self, processor):
		self.initCD()
		self.lemmatizeDictCD(processor)
		self.createOutputCD(self._sentimentDictLemmas, "../SentimentAnalysis/TransformedLexicons/" + processor + "-Lemmas/CD-Lemmas")

if __name__ == "__main__":
    main()