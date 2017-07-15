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
	#lexiconHandler.initSingleDict("NRC-Original")
	#lexiconHandler.initSentiWS()
	#print(len(lexiconHandler._sentimentDictLemmas))
	
	#lexiconHandler.createSentimentDictFileSentiWSRaw()
	#lexiconHandler.createSentimentDictFileSentiWSLemmas()

	#lexiconHandler.createSentimentDictFileBawlRaw()
	#lexiconHandler.createSentimentDFileBawlLemmas()
	lexiconHandler.readAndInitBawlLemmas()
	print(len(lexiconHandler._sentimentDictLemmas))

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
		elif (lexicon == "Bawl-Original"):
			self.initBawl()
		else:
			return("Kein korrekter Lexikonname wurde übergeben")

	def initNRC(self):
		sentDictText = open("../SentimentAnalysis/NRCEmotionLexicon/NRC.txt")
		self._sentimentDict = self.getSentimentDictNRC(sentDictText, False)

		self._sentimentDict = self.removePhrasesFromNRC(self._sentimentDict)
		self._sentimentDict = self.removeTotalZerosFromNRC(self._sentimentDict)
	
	def readAndInitNRCLemmas(self):
		sentDictText = open("../SentimentAnalysis/TransformedLexicons/NRC-Lemmas.txt")
		self.initNRC()
		self._sentimentDictLemmas = self.getSentimentDictNRC(sentDictText, True)

	def readAndInitBawlLemmas(self):
		sentDictText = open("../SentimentAnalysis/TransformedLexicons/Bawl-Lemmas.txt")
		self.initBawl()
		self._sentimentDictLemmas = self.getSentimentDictBawl(sentDictText)
	
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
				
	def getHigherSentimentsValueNrc(self, newSentiments, oldSentiments):
		newSentimentsScore = 0
		oldSentimentsScore = 0

		for sentiment in newSentiments:
			newSentimentsScore = newSentimentsScore + newSentiments[sentiment]
		for sentiment in oldSentiments:
			oldSentimentsScore = oldSentimentsScore + oldSentiments[sentiment]

		if(newSentimentsScore > oldSentimentsScore):
			return newSentiments
		else:
			return oldSentiments

	def lemmatizeDict(self):
		lp = Language_Processor()
		newSentimentDict = {}
		print("start Lemmatisation")
		lemmaTokenPairs = {}
		
		for word,value in self._sentimentDict.iteritems():
			lemma = lp.getLemma(word)
			
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

	def lemmatizeDictNrc(self):
		lp = Language_Processor()
		newSentimentDict = {}
		print("start Lemmatisation")
		
		for word,value in self._sentimentDict.iteritems():
			lemma = lp.getLemma(word)
			
			if lemma in newSentimentDict:
				newSentiments = value
				oldSentiments = newSentimentDict[lemma]
				sentiments = self.getHigherSentimentsValueNrc(newSentiments, oldSentiments)
				newSentimentDict[lemma] = sentiments
			else:
				newSentimentDict[lemma] = value
		
		print("Lemmatisation finished")
		self._sentimentDictLemmas = newSentimentDict

	def lemmatizeDictBawl(self):
		lp = Language_Processor()
		newSentimentDict = {}
		print("start Lemmatisation")
		
		for word,value in self._sentimentDict.iteritems():
			lemma = lp.getLemma(word)			
			if lemma in newSentimentDict:
				print lemma
				#info = self.getHigherSentimentValuesBawl(value)
				newSentimentDict[lemma] = value
			else:
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
				line = line + str(sentimentsPerWord[sentiment]) + "\t"
			line = line.rstrip("\t")
			line = line + "\n"
			outputFile.write(line)
		outputFile.close()

	def createOutputBawl(self, sentimentDict, dataName):
		outputFile = open(dataName + ".txt", "w")
		firstLine = "word\temotion\tarousel"
		outputFile.write(firstLine)

		for word in sentimentDict:
			info = sentimentDict[word]
			line = "\n" + word + "\t" + str(info["emotion"]) + "\t" + str(info["arousel"])
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

	
	def initBawl(self):
		sentDictText = open("../SentimentAnalysis/Bawl-R/bawl-r.txt")
		sentimentDict = self.getSentimentDictBawl(sentDictText)
		self._sentimentDict = sentimentDict
		print(len(self._sentimentDict))

	def getSentimentDictBawl(self, sentimentDictText):
		lines = sentimentDictText.readlines()[1:]
		sentimentDict = {}
		for line in lines:
			info = line.split("\t")
			word = info[0]
			infoPerWord = {}
			infoPerWord["emotion"] = float(info[1].replace(",", "."))
			infoPerWord["arousel"] = float(info[2].replace(",", "."))
			sentimentDict[unicode(word)] = infoPerWord
		return sentimentDict
	
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

	def getHigherSentimentValue(self, newScore, oldScore):
		if(abs(newScore) > abs(oldScore)):
			return newScore
		else:
			return oldScore
	
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

	def createSentimentDictFileSentiWSRaw(self):
		self.initSingleDict("SentiWS-Original")
		self.createOutput(self._sentimentDict, "../SentimentAnalysis/TransformedLexicons/SentiWS-Raw-New")
		
	
	def createSentimentDictFileSentiWSLemmas(self):
		self.initSingleDict("SentiWS-Original")
		self.lemmatizeDict()
		self.createOutput(self._sentimentDictLemmas, "../SentimentAnalysis/TransformedLexicons/SentiWS-Lemmas-New")

	def createSentimentDictFileNRCRaw(self):
		self.initSingleDict("NRC-Original")
		self.createOutputNRC(self._sentimentDict, "../SentimentAnalysis/TransformedLexicons/NRC-Raw-New")

	def createSentimentDictFileNRCLemmas(self):
		self.initSingleDict("NRC-Original")
		self.lemmatizeDictNrc()
		self.createOutputNRC(self._sentimentDictLemmas, "../SentimentAnalysis/TransformedLexicons/NRC-Lemmas")
	
	def createSentimentDictFileBawlRaw(self):
		self.initSingleDict("Bawl-Original")
		self.createOutputBawl(self._sentimentDict, "../SentimentAnalysis/TransformedLexicons/Bawl-Raw")

	def createSentimentDFileBawlLemmas(self):
		self.initSingleDict("Bawl-Original")
		self.lemmatizeDictBawl()
		self.createOutputBawl(self._sentimentDictLemmas, "../SentimentAnalysis/TransformedLexicons/Bawl-Lemmas")

if __name__ == "__main__":
    main()