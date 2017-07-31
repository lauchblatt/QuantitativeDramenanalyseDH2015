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

	bawl = Bawl()
	#bawl.createSentimentDictFileBawlLemmas()
	#bawl.readAndInitBawlAndLemmas()

class Bawl:
	def __init__(self):
		self._sentimentDict = {}
		self._sentimentDictLemmas = {}

	def readAndInitBawlAndLemmas(self):
		self.initBawl()
		sentDictText = open("../SentimentAnalysis/TransformedLexicons/Pattern-Lemmas/Bawl-Lemmas.txt")
		self._sentimentDictLemmas = self.getSentimentDictBawl(sentDictText)

	def initBawl(self):
		sentDictText = open("../SentimentAnalysis/Bawl-R/bawl-r-wc.txt")
		sentimentDict = self.getSentimentDictBawl(sentDictText)
		self._sentimentDict = sentimentDict

	def getSentimentDictBawl(self, sentimentDictText):
		lines = sentimentDictText.readlines()[1:]
		sentimentDict = {}

		for line in lines:
			info = line.split("\t")
			word = info[0]
			#For first Read
			if(len(info) > 3):
				wordClass = info[3].rstrip()
				# Uppercase Word if noun
				if(wordClass == "N"):
					upperWord = word[:1].upper() + word[1:]
					word = upperWord
			infoPerWord = {}
			infoPerWord["emotion"] = float(info[1].replace(",", "."))
			infoPerWord["arousel"] = float(info[2].replace(",", "."))
			sentimentDict[unicode(word)] = infoPerWord
		return sentimentDict

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

	def createOutputBawl(self, sentimentDict, dataName):
		outputFile = open(dataName + ".txt", "w")
		firstLine = "word\temotion\tarousel"
		outputFile.write(firstLine)

		for word in sentimentDict:
			info = sentimentDict[word]
			line = "\n" + word + "\t" + str(info["emotion"]) + "\t" + str(info["arousel"])
			outputFile.write(line)
		outputFile.close()

	def createSentimentDictFileBawlToken(self):
		self.initBawl()
		self.createOutputBawl(self._sentimentDict, "../SentimentAnalysis/TransformedLexicons/Bawl-Token")

	def createSentimentDictFileBawlLemmas(self):
		self.initBawl()
		self.lemmatizeDictBawl()
		self.createOutputBawl(self._sentimentDictLemmas, "../SentimentAnalysis/TransformedLexicons/Pattern-Lemmas/Bawl-Lemmas")

if __name__ == "__main__":
    main()