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
	#lexiconHandler.initSingleDict("SentiWS-Lemmas")
	lexiconHandler.initSingleDict("NRC")
	print(len(lexiconHandler._sentimentDict))
	lexiconHandler.lemmatizeDict()
	print(len(lexiconHandler._sentimentDictLemmas))
	print(lexiconHandler._sentimentDictLemmas)

class Lexicon_Handler:

	def __init__(self):
		self._sentimentDict = {}
		self._sentimentDictLemmas = {}

	def initSingleDict (self, lexicon):
		if (lexicon == "SentiWSOriginal"):
			self.initSentiWS()
		elif (lexicon == "SentiWS-Lemmas"):
			self.initSentiWSLemmas()
		elif (lexicon == "NRC"):
			self.initNRC()
		else:
			return("Kein korrekter Lexikonname wurde übergeben")

	def initNRC(self):
		sentDictText = open("../SentimentAnalysis/NRCEmotionLexicon/NRC.txt")
		self._sentimentDict = self.getSentimentDictNRC(sentDictText)
	
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
		for word in sentimentDict:
			line = word + "\t"
			sentimentsPerWord = sentimentDict[word]
			#line = line + 

	def getWordsAsTextFromDict(self):
		text = ""
		for word in self._sentimentDict:
			text = text + " " + word

		return text

	def initSentiWSLemmas(self):
		print("initSentiWSLemmas")
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

	def createSentimentDictSentiWSRaw(self):
		self.initSingleDict("SentiWSOriginal")
		lexiconHandler.createOutput(lexiconHandler._sentimentDict, "../SentimentAnalysis/TransformedLexicons/SentiWS-Raw")
		
	
	def createSentimentDictSentiWSLemmas(self):
		self.initSingleDict("SentiWSOriginal")
		lexiconHandler.lemmmatizeDict()
		lexiconHandler.createOutput(lexiconHandler._sentimentDictLemmas, "../SentimentAnalysis/TransformedLexicons/SentiWS-Lemmas")

if __name__ == "__main__":
    main()