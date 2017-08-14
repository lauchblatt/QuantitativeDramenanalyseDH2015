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

	nrc = NRC()
	#nrc.resetAllFiles()
	#nrc.createSentimentDictFileNRCLemmas("treetagger")
	#nrc.createExtendedOutputDTA()
	nrc.readAndInitNRCAndLemmas("treetagger")
	print(len(nrc._sentimentDict))

class NRC:

	def __init__(self):
		self._sentimentDict = {}
		self._sentimentDictLemmas = {}

	def readAndInitNRCAndLemmas(self, processor):
		self.initNRC()
		sentDictText = open("../SentimentAnalysis/TransformedLexicons/" + processor + "-Lemmas/NRC-Lemmas.txt")
		self._sentimentDictLemmas = self.getSentimentDictNRC(sentDictText, True)

	def readAndInitNRCAndLemmasDTA(self, processor):
		self.initNRC()
		self.extendLexiconNRCDTA()
		sentDictText = open("../SentimentAnalysis/TransformedLexicons/" + processor + "-Lemmas/NRC-Lemmas-DTAExtended.txt")
		self._sentimentDictLemmas = self.getSentimentDictNRC(sentDictText, True)

	def initNRC(self):
		sentDictText = open("../SentimentAnalysis/NRCEmotionLexicon/NRC.txt")
		self._sentimentDict = self.getSentimentDictNRC(sentDictText, False)

		self._sentimentDict = self.removePhrasesFromNRC(self._sentimentDict)
		self.handleSpecialCases()
		self._sentimentDict = self.removeTotalZerosFromNRC(self._sentimentDict)
		self.replaceRemainingDoublePolarities()

	def replaceRemainingDoublePolarities(self):
		for word in self._sentimentDict:
			sentiments = self._sentimentDict[word]
			if(sentiments["positive"] == 1 and sentiments["negative"] == 1):
				self._sentimentDict[word]["negative"] = 0

	def handleSpecialCases(self):
		for word in self._sentimentDict.keys():
			if(word.endswith("-")):
				del self._sentimentDict[word]
			# wegen leugnen,
			if(word.endswith(",")):
				self._sentimentDict[word.rstrip(",")] = self._sentimentDict[word]
				del self._sentimentDict[word]
				

	def getSentimentDictNRC(self, sentimentDictText, isLemmas):
		columnSub = 0
		if(isLemmas):
			columnSub = 1

		nrcSentimentDict = {}
		lines = sentimentDictText.readlines()[1:]
		for line in lines:
			wordsAndValues = line.split("\t")
			word = wordsAndValues[1-columnSub]
			
			# skip missing german translations
			if(not(word == "")):
				sentimentsPerWord = {}

				sentimentsPerWord["positive"] = int(wordsAndValues[2-columnSub])
				sentimentsPerWord["negative"] = int(wordsAndValues[3-columnSub])
				sentimentsPerWord["anger"] = int(wordsAndValues[4-columnSub])
				sentimentsPerWord["anticipation"] = int(wordsAndValues[5-columnSub])
				sentimentsPerWord["disgust"] = int(wordsAndValues[6-columnSub])
				sentimentsPerWord["fear"] = int(wordsAndValues[7-columnSub])
				sentimentsPerWord["joy"] = int(wordsAndValues[8-columnSub])
				sentimentsPerWord["sadness"] = int(wordsAndValues[9-columnSub])
				sentimentsPerWord["surprise"] = int(wordsAndValues[10-columnSub])
				sentimentsPerWord["trust"] = int(wordsAndValues[11-columnSub].rstrip())

				alreadyInLexicon = False
				if(unicode(word) in nrcSentimentDict):
					higherSentiments = self.getHigherSentimentsValueNrc(sentimentsPerWord, nrcSentimentDict[unicode(word)])
					alreadyInLexicon = True
					nrcSentimentDict[unicode(word)] = higherSentiments
				
				if(not alreadyInLexicon):
					nrcSentimentDict[unicode(word)] = sentimentsPerWord
		
		return nrcSentimentDict

	def lemmatizeDictNRC(self, processor):
		lp = Language_Processor(processor)
		newSentimentDict = {}
		print("start Lemmatisation")
		
		for word,value in self._sentimentDict.iteritems():
			lemma = lp._processor.getLemma(word)
			
			if lemma in newSentimentDict:
				newSentiments = value
				oldSentiments = newSentimentDict[lemma]
				sentiments = self.getHigherSentimentsValueNrc(newSentiments, oldSentiments)
				newSentimentDict[lemma] = sentiments
			else:
				newSentimentDict[lemma] = value
		
		print("Lemmatisation finished")
		self._sentimentDictLemmas = newSentimentDict

	def getHigherSentimentsValueNrc(self, newSentiments, oldSentiments):
		newSentimentsScore = 0
		oldSentimentsScore = 0
		doublePolarityNew = (newSentiments["positive"] == 1 and newSentiments["negative"] == 1)
		doublePolarityOld = (oldSentiments["positive"] == 1 and oldSentiments["negative"] == 1)
		isNeutralNew = all(value == 0 for value in newSentiments.values())
		isNeutralOld = all(value == 0 for value in oldSentiments.values())
		if(doublePolarityNew == True and doublePolarityOld == False and isNeutralOld == False):
			return oldSentiments
		if(doublePolarityOld == True and doublePolarityNew == False and isNeutralNew == False):
			return newSentiments

		for sentiment in newSentiments:
			newSentimentsScore = newSentimentsScore + newSentiments[sentiment]
		for sentiment in oldSentiments:
			oldSentimentsScore = oldSentimentsScore + oldSentiments[sentiment]

		if(newSentimentsScore > oldSentimentsScore):
			return newSentiments
		else:
			return oldSentiments

	def removePhrasesFromNRC(self, nrcSentimentDict):
		phrases = []
		for word in nrcSentimentDict:
			words = word.split()
			if(len(words) > 1):
				phrases.append(word)
		for phrase in phrases:
			del nrcSentimentDict[phrase]
		return nrcSentimentDict

	def removeTotalZerosFromNRC(self, nrcSentimentDict):
		totalZeros = self.getTotalZerosNRC(nrcSentimentDict)

		for zeroWord in totalZeros:
			del nrcSentimentDict[zeroWord]
		return nrcSentimentDict

	def createOutputNRC(self, sentimentDict, dataName):
		outputFile = open(dataName + ".txt", "w")
		sentiments = ["positive", "negative", "anger", "anticipation", "disgust", "fear", "joy", "sadness", "surprise", "trust"]
		firstLine = "word\tpositive\tnegative\tanger\tanticipation\tdisgust\tfear\tjoy\tsadness\tsurprise\ttrust\n"
		outputFile.write(firstLine)
		
		for word in sentimentDict:
			line = word + "\t"
			sentimentsPerWord = sentimentDict[word]
			for sentiment in sentiments:
				line = line + str(sentimentsPerWord[sentiment]) + "\t"
			line = line.rstrip("\t")
			line = line + "\n"
			outputFile.write(line)
		outputFile.close()

	def getTotalZerosNRC(self, nrcSentimentDict):
		totalZeros = {}
		
		for word in nrcSentimentDict:
			sentiments = nrcSentimentDict[word]
			if(all(value == 0 for value in sentiments.values())):
				totalZeros[word] = sentiments
		return totalZeros

	def getDoublesInGermanNRC(self):
		sentDictText = open("../SentimentAnalysis/NRCEmotionLexicon/NRC.txt")
		lines = sentDictText.readlines()[1:]
		words = []
		doubles = []

		for line in lines:
			wordsAndValues = line.split("\t")
			word = wordsAndValues[1]

			if(not(word == "")):
				if(word in words):
					doubles.append(word)
				else:
					words.append(word)
		for word in doubles:
			print(word)

	def createExtendedOutputDTA(self):
		self.initNRC()
		print("###")
		print(len(self._sentimentDict))
		self.extendLexiconNRCDTA()
		print("###")
		print(len(self._sentimentDict))
		self.createOutputNRC(self._sentimentDict, "../SentimentAnalysis/TransformedLexicons/NRC-Token-DTAExtended")
		self.lemmatizeDictNRC("treetagger")
		print("###")
		print(len(self._sentimentDictLemmas))
		self.createOutputNRC(self._sentimentDictLemmas, "../SentimentAnalysis/TransformedLexicons/treetagger-Lemmas/NRC-Lemmas-DTAExtended")
		self.lemmatizeDictNRC("textblob")
		print(len(self._sentimentDictLemmas))
		self.createOutputNRC(self._sentimentDictLemmas, "../SentimentAnalysis/TransformedLexicons/textblob-Lemmas/NRC-Lemmas-DTAExtended")

	def extendLexiconNRCDTA(self):
		dta = DTA_Handler()
		self._sentimentDict = dta.extendSentimentDictDTA(self._sentimentDict)

	def resetAllFiles(self):
		self.createSentimentDictFileNRCToken()
		self.createSentimentDictFileNRCLemmas("treetagger")
		self.createSentimentDictFileNRCLemmas("textblob")

	def createSentimentDictFileNRCToken(self):
		self.initNRC()
		self.createOutputNRC(self._sentimentDict, "../SentimentAnalysis/TransformedLexicons/NRC-Token")

	def createSentimentDictFileNRCLemmas(self, processor):
		self.initNRC()
		self.lemmatizeDictNRC(processor)
		self.createOutputNRC(self._sentimentDictLemmas, "../SentimentAnalysis/TransformedLexicons/" + processor + "-Lemmas/NRC-Lemmas")

if __name__ == "__main__":
    main()