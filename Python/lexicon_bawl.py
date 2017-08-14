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
	mat = bawl.test2()
	bawl.fleiss_kappa(mat)
	#bawl.createExtendedOutputDTA()
	#bawl.createSentimentDictFileBawlLemmas("treetagger")
	#bawl.resetAllFiles()
	#bawl.createExtendedOutputDTA()
	#bawl.readAndInitBawlAndLemmasDTA("treetagger")

class Bawl:

	def __init__(self):
		self._sentimentDict = {}
		self._sentimentDictLemmas = {}

	def fleiss_kappa(self, matrix):
		raters = 5
		N = len(matrix)
		categories = len(matrix[0])
		allRates = N*raters
		print allRates
		pjs = []
		i = 0
		while(i < categories):
			colSum = 0
			for line in matrix:
				colSum = colSum + line[i]
			pjs.append(float(float(colSum)/allRates))
			i = i + 1
		Pis = []
		for line in matrix:
			squares = [item * item for item in line]
			squaresSum = sum(squares)
			result = (float(squaresSum - raters))/float(raters * (raters - 1))
			Pis.append(result)
		sumPis = sum(Pis)
		P_ = float(sumPis)/N
		squaresPjs = [item * item for item in pjs]
		P_e = sum(squaresPjs)
		fleiss_kappa = (P_ - P_e)/(1 - P_e)
		return fleiss_kappa


	def test(self):
		datei = open("zahlen.txt")
		for line in datei:
			number = int(line.strip())

			if(number == 1 or number == 2):
				number = 1
			elif(number == 3):
				number = 2
			elif(number == 4):
				number = 3
			elif(number == 5 or number == 6):
				number = 4
			print number

	def test2(self):
		data = open("blub.txt")
		lines = []
		for line in data:
			numbers = line.split("\t")
			numbers = [number.strip() for number in numbers]
			a1 = 0
			a2 = 0
			a3 = 0
			a4 = 0
			a5 = 0
			a6 = 0
			for number in numbers:
				if(number == "1"):
					a1 += 1
				elif(number == "2"):
					a2 += 1
				elif(number == "3"):
					a3 += 1
				elif(number == "4"):
					a4 += 1
				elif(number == "5"):
					a5 += 1
				elif(number == "6"):
					a6 += 1
			output = "\t".join([str(a1), str(a2), str(a3), str(a4), str(a5), str(a6)])
			#print output
			line = [a1, a2, a3, a4, a5, a6]
			lines.append(line)
		return lines



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
		self.removeNeutralWords()

	def removeNeutralWords(self):
		wordsToDel = []
		for word in self._sentimentDict:
			if(self._sentimentDict[word]["emotion"] == 0):
				wordsToDel.append(word)

		for word in wordsToDel:
			del self._sentimentDict[word]

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
				#reduction to only emotion, because its most important
				newSentimentDict[lemma] = self.getBetterValues(value, newSentimentDict[lemma])
			else:
				newSentimentDict[lemma] = value
		
		print("Lemmatisation finished")
		self._sentimentDictLemmas = newSentimentDict

	def getBetterValues(self, newValues, oldValues):
		newEmotion = abs(newValues["emotion"])
		newArousel = newValues["arousel"]
		oldEmotion = abs(oldValues["emotion"])
		oldArousel = oldValues["arousel"]
		if(newEmotion > oldEmotion):
			return newValues
		elif(newArousel > oldArousel):
			return newValues
		return oldValues


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

	def resetAllFiles(self):
		self.createSentimentDictFileBawlToken()
		self.createSentimentDictFileBawlLemmas("treetagger")
		self.createSentimentDictFileBawlLemmas("textblob")

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