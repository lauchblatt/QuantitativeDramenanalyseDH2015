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

	lexiconHandler = Lexicon_Handler()
	#lexiconHandler.createSentimentDictFileNRCRaw()
	#lexiconHandler.createSentimentDictFileNRCLemmas()
	lexiconHandler.initSingleDict("NRC-Lemmas")

class Lexicon_Handler:

	def __init__(self):
		self._sentimentDict = {}
		self._sentimentDictLemmas = {}

	def initSingleDict (self, lexicon):
		if (lexicon == "SentiWS-Original"):
			self.initSentiWS()
		elif (lexicon == "SentiWS-Lemmas"):
			self.readAndInitSentiWSLemmas()
		elif (lexicon == "NRC-Original"):
			self.initNRC()
		elif (lexicon == "NRC-Lemmas"):
			self.readAndInitNRCLemmas()
		else:
			return("Kein korrekter Lexikonname wurde übergeben")

	def initNRC(self):
		sentDictText = open("../SentimentAnalysis/NRCEmotionLexicon/NRC.txt")
		sentimentDict = self.getSentimentDictNRC(sentDictText, False)
		self._sentimentDict = self.removeTotalZerosFromNRC(sentimentDict)
	
	def readAndInitNRCLemmas(self):
		sentDictText = open("../SentimentAnalysis/TransformedLexicons/NRC-Lemmas.txt")
		self.initNRC()
		sentimentDictLemmas = self.getSentimentDictNRC(sentDictText, True)
		self._sentimentDictLemmas = self.removeTotalZerosFromNRC(sentimentDictLemmas)

	def removeTotalZerosFromNRC(self, nrcSentimentDict):
		totalZeros = self.getTotalZerosNRC(nrcSentimentDict)

		for zeroWord in totalZeros:
			del nrcSentimentDict[zeroWord]
		return nrcSentimentDict

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

				nrcSentimentDict[unicode(word)] = sentimentsPerWord
		
		return nrcSentimentDict
				
	def lemmatizeDict(self):
		lp = Language_Processor()
		newSentimentDict = {}
		print("start Lemmatisation")
		
		for word,value in self._sentimentDict.iteritems():
			lemma = lp.getLemma(word)
			"""
			if lemma in newSentimentDict:
				print("###########")
				print("Altes Wort: " + newSentimentDict[lemma][0])
				print("Altes Lemma: " + lemma + " Wert: " + str(newSentimentDict[lemma][1]))
				print("Neues Wort: " + (word))
				print("Neues Lemma: " + (lemma) + " Wert: " + str(value))
			"""
			newSentimentDict[lemma] = value
		
		print("Lemmatisation finished")	
		self._sentimentDictLemmas = newSentimentDict

	def createOutput(self, sentimentDict, dataName):
		outputFile = open(dataName + ".txt", "w")

		for word in sentimentDict:
			outputFile.write(word + "\t" + str(sentimentDict[word]) +"\n")

		outputFile.close()

	def createOutputNRC(self, sentimentDict, dataName):
		outputFile = open(dataName + ".txt", "w")
		sentiments = ["positive", "negative", "anger", "anticipation", "disgust", "fear", "joy", "sadness", "surprise", "trust"]
		firstLine = "word\tpositive\tnegative\tanger\tanticipation\tdisgust\tfear\tjoy\tsadness\tsurprise\ttrust\n"
		outputFile.write(firstLine)
		
		for word in sentimentDict:
			line = word + "\t"
			sentimentsPerWord = sentimentDict[word]
			for sentiment in sentiments:
				line = line + sentimentsPerWord[sentiment] + "\t"
			line = line.rstrip("\t")
			line = line + "\n"
			outputFile.write(line)
		outputFile.close()


	def getWordsAsTextFromDict(self):
		text = ""
		for word in self._sentimentDict:
			text = text + " " + word

		return text

	def readAndInitSentiWSLemmas(self):
		self.initSentiWS()
		sentimentDictText = open("../SentimentAnalysis/TransformedLexicons/SentiWS-Lemmas.txt")
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

		for line in sentimentDictText:
			firstWord = line.split("|")[0]

			tabSplit = line.split("\t")
			number = tabSplit[1].rstrip()

			sentimentDict[unicode(firstWord)] = number
			
			if 0 <= 2 < len(tabSplit):
				flexions = tabSplit[2]
				seperatedFlexions = flexions.split(",")

				for flex in seperatedFlexions:
					flex = flex.rstrip()
					sentimentDict[unicode(flex)] = number
			

		return sentimentDict

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
		print(len(words))
		print(len(doubles))
		for word in doubles:
			print(word)

	def createSentimentDictFileSentiWSRaw(self):
		self.initSingleDict("SentiWS-Original")
		self.createOutput(self._sentimentDict, "../SentimentAnalysis/TransformedLexicons/SentiWS-Raw")
		
	
	def createSentimentDictFileSentiWSLemmas(self):
		self.initSingleDict("SentiWS-Original")
		self.lemmatizeDict()
		self.createOutput(self._sentimentDictLemmas, "../SentimentAnalysis/TransformedLexicons/SentiWS-Lemmas")

	def createSentimentDictFileNRCRaw(self):
		self.initSingleDict("NRC-Original")
		self.createOutputNRC(self._sentimentDict, "../SentimentAnalysis/TransformedLexicons/NRC-Raw")

	def createSentimentDictFileNRCLemmas(self):
		self.initSingleDict("NRC-Original")
		self.lemmatizeDict()
		self.createOutputNRC(self._sentimentDictLemmas, "../SentimentAnalysis/TransformedLexicons/NRC-Lemmas")

if __name__ == "__main__":
    main()