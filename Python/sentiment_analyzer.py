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
		self._sentimentDict = self.getSentimentDictNRC(sentDictText)
	
	def readAndinitNRCLemmas():
		sentDictText = open("../SentimentAnalysis/TransformedLexicons/NRC-Lemmas.txt")
		self._sentimentDict = self.getSentimentDictNRC(sentDictText)
		self._lemmatizeDict()

	def getSentimentDictNRC(self, sentimentDictText):
		nrcSentimentDict = {}
		lines = sentimentDictText.readlines()[1:]
		for line in lines:
			wordsAndValues = line.split("\t")
			word = wordsAndValues[1]
			
			# skip missing german translations
			if(not(word == "")):
				sentimentsPerWord = {}

				sentimentsPerWord["positive"] = wordsAndValues[2]
				sentimentsPerWord["negative"] = wordsAndValues[3]
				sentimentsPerWord["anger"] = wordsAndValues[4]
				sentimentsPerWord["anticipation"] = wordsAndValues[5]
				sentimentsPerWord["disgust"] = wordsAndValues[6]
				sentimentsPerWord["fear"] = wordsAndValues[7]
				sentimentsPerWord["joy"] = wordsAndValues[8]
				sentimentsPerWord["sadness"] = wordsAndValues[9]
				sentimentsPerWord["surprise"] = wordsAndValues[10]
				sentimentsPerWord["trust"] = wordsAndValues[11].rstrip()

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
		sentimentDictText = open("../SentimentAnalysis/TransformedLexicons/SentiWS-Lemmas.txt")
		sentimentDict = {}

		for line in sentimentDictText:
			wordAndValue = line.split("\t")
			word = wordAndValue[0]
			value = wordAndValue[1].rstrip()
			sentimentDict[unicode(word)] = value

		self._sentimentDictLemmas = sentimentDict

	
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
			
			if 0 <= 2 < len(tabSplit):
				flexions = tabSplit[2]
				seperatedFlexions = flexions.split(",")

				for flex in seperatedFlexions:
					flex = flex.rstrip()
					sentimentDict[unicode(flex)] = number
			

		return sentimentDict

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