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

	lexiconHandler.initCD()
	

class Lexicon_Handler:

	def __init__(self):
		self._sentimentDict = {}
		self._sentimentDictLemmas = {}

	def initSingleDict (self, lexicon):
		if (lexicon == "SentiWS"):
			self.readAndInitSentiWSAndLemmas()
		elif (lexicon == "NRC"):
			self.readAndInitNRCAndLemmas()
		elif (lexicon == "Bawl"):
			self.readAndInitBawlAndLemmas()
		else:
			return("Kein korrekter Lexikonname wurde übergeben")

	def initNRC(self):
		sentDictText = open("../SentimentAnalysis/NRCEmotionLexicon/NRC.txt")
		self._sentimentDict = self.getSentimentDictNRC(sentDictText, False)

		#self._sentimentDict = self.removePhrasesFromNRC(self._sentimentDict)
		self._sentimentDict = self.removeTotalZerosFromNRC(self._sentimentDict)
	
	def readAndInitSentiWSAndLemmas(self):
		self.initSentiWS()
		sentimentDictText = open("../SentimentAnalysis/TransformedLexicons/Pattern-Lemmas/SentiWS-Lemmas.txt")
		sentimentDict = {}

		for line in sentimentDictText:
			wordAndValue = line.split("\t")
			word = wordAndValue[0]
			value = float(wordAndValue[1].rstrip())
			sentimentDict[unicode(word)] = value

		self._sentimentDictLemmas = sentimentDict

	def readAndInitNRCAndLemmas(self):
		sentDictText = open("../SentimentAnalysis/TransformedLexicons/Pattern-Lemmas/NRC-Lemmas.txt")
		self.initNRC()
		self._sentimentDictLemmas = self.getSentimentDictNRC(sentDictText, True)

	def readAndInitBawlAndLemmas(self):
		sentDictText = open("../SentimentAnalysis/TransformedLexicons/Pattern-Lemmas/Bawl-Lemmas.txt")
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
			print lemma
			
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
				#could be a method
				newAbsolute = abs(value["emotion"]) + abs(value["arousel"])
				oldAbsolute = abs(newSentimentDict[lemma]["emotion"]) + abs(newSentimentDict[lemma]["arousel"])
				if(newAbsolute > oldAbsolute):
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
	
	def initCD(self):
		sentDictText = open("../SentimentAnalysis/CD/cd.txt")
		sentimentDict = self.getSentimentDictCD(sentDictText)

	def getSentimentDictCD(self, sentimentDictText):
		lines = sentimentDictText.readlines()
		sentimentDict = {}
		i = 0
		for line in lines:
			info = line.split(" ")
			word = info[0]
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
				sentiments = self.getHigherSentimentValuesCD(infoPerWord, sentimentDict[unicode(word)])
				print("\n")
				print word
				print ("Alte Sentiments:")
				print(sentimentDict[unicode(word)])
				print("Neue Sentiments:")
				print(infoPerWord)
				print("Gewählte Sentiments:")
				print(sentiments)
				infoPerWord = sentiments
			
			sentimentDict[unicode(word)] = infoPerWord

		print(len(sentimentDict))

	def getHigherSentimentValuesCD(self, newSentiments, oldSentiments):
		sentiments = {}
		sentiments["positive"] = self.getHigherSentimentValue(newSentiments["positive"], oldSentiments["positive"])
		sentiments["negative"] = self.getHigherSentimentValue(newSentiments["negative"], oldSentiments["negative"])
		sentiments["neutral"] = self.getHigherSentimentValue(newSentiments["neutral"], oldSentiments["neutral"])
		return sentiments

	def getSentimentCD(self, sentiments):
		if(sentiments["positive"] != 0):
			return "POS"
		if(sentiments["negative"] != 0):
			return "NEG"
		if(sentiments["neutral"] != 0):
			return "NEU"

	def initBawl(self):
		sentDictText = open("../SentimentAnalysis/Bawl-R/bawl-r.txt")
		sentimentDict = self.getSentimentDictBawl(sentDictText)
		self._sentimentDict = sentimentDict

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

	def createSentimentDictFileSentiWSToken(self):
		self.initSentiWS()
		self.createOutput(self._sentimentDict, "../SentimentAnalysis/TransformedLexicons/SentiWS-Token")
		
	
	def createSentimentDictFileSentiWSLemmas(self):
		self.initSentiWS()
		self.lemmatizeDict()
		self.createOutput(self._sentimentDictLemmas, "../SentimentAnalysis/TransformedLexicons/Pattern-Lemmas/SentiWS-Lemmas")

	def createSentimentDictFileNRCToken(self):
		self.initNRC()
		self.createOutputNRC(self._sentimentDict, "../SentimentAnalysis/TransformedLexicons/NRC-Token")

	def createSentimentDictFileNRCLemmas(self):
		self.initNRC()
		self.lemmatizeDictNrc()
		self.createOutputNRC(self._sentimentDictLemmas, "../SentimentAnalysis/TransformedLexicons/Pattern-Lemmas/NRC-Lemmas")
	
	def createSentimentDictFileBawlToken(self):
		self.initBawl()
		self.createOutputBawl(self._sentimentDict, "../SentimentAnalysis/TransformedLexicons/Bawl-Token")

	def createSentimentDictFileBawlLemmas(self):
		self.initBawl()
		self.lemmatizeDictBawl()
		self.createOutputBawl(self._sentimentDictLemmas, "../SentimentAnalysis/TransformedLexicons/Pattern-Lemmas/Bawl-Lemmas")

if __name__ == "__main__":
    main()