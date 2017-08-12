# -*- coding: utf8 -*-

import os
import re
import collections
import locale
import sys
from lexicon_handler import *
from lp_language_processor import *
from lexicon_clematide_dictionary import *

def main():
	reload(sys)
	sys.setdefaultencoding('utf8')

	bawl = Bawl()
	#bawl.createSentimentDictFileBawlLemmas("treetagger")
	bawl.readAndInitBawlAndLemmas("treetagger")
	#bawl.createExtendedOutputDTA()
	#bawl.readAndInitBawlAndLemmasDTA("treetagger")

	LP = Language_Processor("treetagger")
	lp = LP._processor
	lp.initStopWords()
	stopWordsInLexicon = [word for word in bawl._sentimentDict \
	 if (word in lp._stopwords)]
	print (len(lp._stopwords))
	print stopWordsInLexicon
	for word in stopWordsInLexicon:
		print word

	print(len(bawl._sentimentDict))
	print(len(bawl._sentimentDictLemmas))

class Bawl:

	def __init__(self):
		self._sentimentDict = {}
		self._sentimentDictLemmas = {}

	def readAndInitBawlAndLemmas(self, processor):
		dta = DTA_Handler()
		self.initBawl()
		sentDictText = open("../SentimentAnalysis/TransformedLexicons/" + processor + "-Lemmas/Bawl-Lemmas.txt")
		self._sentimentDictLemmas = self.getSentimentDictBawl(sentDictText)

	def readAndInitBawlAndLemmasDTA(self, processor):
		self.initBawl()
		self.extendLexiconBawlDTA()
		sentDictText = open("../SentimentAnalysis/TransformedLexicons/" + processor + "-Lemmas/Bawl-Lemmas-DTAExtended.txt")
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

	def lemmatizeDictBawl(self, processor):
		lp = Language_Processor(processor)
		newSentimentDict = {}
		print("start Lemmatisation")
		
		for word,value in self._sentimentDict.iteritems():
			lemma = lp._processor.getLemma(word)		
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

	def createExtendedOutputDTA(self):
		self.initBawl()
		print("###")
		print(len(self._sentimentDict))
		self.extendLexiconBawlDTA()
		print("###")
		print(len(self._sentimentDict))
		self.createOutputBawl(self._sentimentDict, "../SentimentAnalysis/TransformedLexicons/Bawl-Token-DTAExtended")
		self.lemmatizeDictBawl("treetagger")
		print("###")
		print(len(self._sentimentDictLemmas))
		self.createOutputBawl(self._sentimentDictLemmas, "../SentimentAnalysis/TransformedLexicons/treetagger-Lemmas/Bawl-Lemmas-DTAExtended")
		self.lemmatizeDictBawl("textblob")
		print(len(self._sentimentDictLemmas))
		self.createOutputBawl(self._sentimentDictLemmas, "../SentimentAnalysis/TransformedLexicons/textblob-Lemmas/Bawl-Lemmas-DTAExtended")

	def extendLexiconBawlDTA(self):
		dta = DTA_Handler()
		self._sentimentDict = dta.extendSentimentDictDTA(self._sentimentDict)

	def createSentimentDictFileBawlToken(self):
		self.initBawl()
		self.createOutputBawl(self._sentimentDict, "../SentimentAnalysis/TransformedLexicons/Bawl-Token")


	def createSentimentDictFileBawlLemmas(self, processor):
		self.initBawl()
		self.lemmatizeDictBawl(processor)
		self.createOutputBawl(self._sentimentDictLemmas, "../SentimentAnalysis/TransformedLexicons/" + processor + "-Lemmas/Bawl-Lemmas")

if __name__ == "__main__":
    main()