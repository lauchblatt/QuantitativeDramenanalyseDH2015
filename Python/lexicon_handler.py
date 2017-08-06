# -*- coding: utf8 -*-

import os
import re
import collections
import locale
import sys
import pickle
from lexicon_bawl import *
from lexicon_german_polarity_clues import *
from lexicon_clematide_dictionary import *
from lexicon_nrc import *
from lexicon_sentiWS import *


def main():
	reload(sys)
	sys.setdefaultencoding('utf8')

	lexiconHandler = Lexicon_Handler()
	lexiconHandler.initSingleDict("SentiWS-DTAExtended", "treetagger")
	#lexiconHandler.initSingleDict("Bawl-DTAExtended", "treetagger")
	for key in lexiconHandler._sentimentDictLemmas:
		print key
	if(u"Heirat" in lexiconHandler._sentimentDictLemmas):
		print lexiconHandler._sentimentDictLemmas[u"Heirat"]
	print(len(lexiconHandler._sentimentDict))
	print(len(lexiconHandler._sentimentDictLemmas))
	#bawl.readAndInitBawlAndLemmasDTA("treetagger")
	#lexiconHandler.initSingleDict("Bawl-DTAExtended", "treetagger")
	#lexiconHandler.combineSentimentLexiconsKeysAndDump("treetagger")
	#lexiconHandler.combineSentimentLexiconsKeysAndDump("textblob")
	#lexiconHandler.resetAllFiles()
	#lexiconHandler.createSimpleOutputCombinedLexicon()
	#print(len(lexiconHandler._sentimentDict))
	#print(len(lexiconHandler._sentimentDictLemmas))
	#lexiconHandler.combineSentimentLexica("textblob")

class Lexicon_Handler:

	def __init__(self):
		self._sentimentDict = {}
		self._sentimentDictLemmas = {}
		self._sentimentDicts = ["SentiWS", "NRC", "Bawl", "CD", "GPC"]
		self._sentimentDictsDTAExtended = ["SentiWS-DTAExtended", "NRC-DTAExtended", "Bawl-DTAExtended", "CD-DTAExtended", "GPC-DTAExtended"]

	def initSingleDict (self, lexicon, processor):
		if (lexicon == "SentiWS"):
			self.initSentiWS(processor, False)
		elif (lexicon == "NRC"):
			self.initNrc(processor, False)
		elif (lexicon == "Bawl"):
			self.initBawl(processor, False)
		elif (lexicon == "CD"):
			self.initCD(processor, False)
		elif (lexicon == "GPC"):
			self.initGPC(processor, False)
		elif (lexicon == "SentiWS-DTAExtended"):
			self.initSentiWS(processor, True)
		elif (lexicon == "NRC-DTAExtended"):
			self.initNrc(processor, True)
		elif (lexicon == "Bawl-DTAExtended"):
			self.initBawl(processor, True)
		elif (lexicon == "CD-DTAExtended"):
			self.initCD(processor, True)
		elif (lexicon == "GPC-DTAExtended"):
			self.initGPC(processor, True)
		elif (lexicon == "CombinedLexicon"):
			self.combineSentimentLexica(processor)
		else:
			return("Kein korrekter Lexikonname wurde übergeben")
	
	def initSentiWS(self, processor, DTAExtended):
		sentiWS = Senti_WS()
		if(DTAExtended):
			sentiWS.readAndInitSentiWSAndLemmasDTA(processor)
		else:
			sentiWS.readAndInitSentiWSAndLemmas(processor)
		self._sentimentDict = sentiWS._sentimentDict
		self._sentimentDictLemmas = sentiWS._sentimentDictLemmas

	def initNrc(self, processor, DTAExtended):
		nrc = NRC()
		if(DTAExtended):
			nrc.readAndInitNRCAndLemmasDTA(processor)
		else:
			nrc.readAndInitNRCAndLemmas(processor)
		self._sentimentDict = nrc._sentimentDict
		self._sentimentDictLemmas = nrc._sentimentDictLemmas

	def initBawl(self, processor, DTAExtended):
		bawl = Bawl()
		if(DTAExtended):
			bawl.readAndInitBawlAndLemmasDTA(processor)
		else:
			bawl.readAndInitBawlAndLemmas(processor)
		self._sentimentDict = bawl._sentimentDict
		self._sentimentDictLemmas = bawl._sentimentDictLemmas

	def initCD(self, processor, DTAExtended):
		cd = CD()
		if(DTAExtended):
			cd.readAndInitCDAndLemmasDTA(processor)
		else:
			cd.readAndInitCDAndLemmas(processor)
		self._sentimentDict = cd._sentimentDict
		self._sentimentDictLemmas = cd._sentimentDictLemmas

	def initGPC(self, processor, DTAExtended):
		gpc = German_Polarity_Clues()
		if(DTAExtended):
			gpc.readAndInitGPCAndLemmasDTA(processor)
		else:
			gpc.readAndInitGPCAndLemmas(processor)
		self._sentimentDict = gpc._sentimentDict
		self._sentimentDictLemmas = gpc._sentimentDictLemmas

	def combineSentimentLexica(self, processor):
		keys = self.readAndReturnLexiconKeyDumps(processor)
		lexiconKeysTokens = keys[0]
		lexiconKeysLemma = keys[1]
		
		sentiWS = Senti_WS()
		sentiWS.readAndInitSentiWSAndLemmas(processor)

		nrc = NRC()
		nrc.readAndInitNRCAndLemmas(processor)

		bawl = Bawl()
		bawl.readAndInitBawlAndLemmas(processor)

		cd = CD()
		cd.readAndInitCDAndLemmas(processor)

		gpc = German_Polarity_Clues()
		gpc.readAndInitGPCAndLemmas(processor)

		combinedLexiconTokens = {}
		combinedLexiconLemmas = {}
		for key in lexiconKeysTokens:
			sentiments = {}
			if (key in sentiWS._sentimentDict): sentiments["sentiWS"] = sentiWS._sentimentDict[key]
			if (key in nrc._sentimentDict): sentiments["nrc"] = nrc._sentimentDict[key]
			if (key in bawl._sentimentDict): sentiments["bawl"] = bawl._sentimentDict[key]
			if (key in cd._sentimentDict): sentiments["cd"] = cd._sentimentDict[key]
			if (key in gpc._sentimentDict): sentiments["gpc"] = gpc._sentimentDict[key]
			combinedLexiconTokens[key] = sentiments

		for key in lexiconKeysLemma:
			sentiments = {}
			if (key in sentiWS._sentimentDictLemmas): sentiments["sentiWS"] = sentiWS._sentimentDictLemmas[key]
			if (key in nrc._sentimentDictLemmas): sentiments["nrc"] = nrc._sentimentDictLemmas[key]
			if (key in bawl._sentimentDictLemmas): sentiments["bawl"] = bawl._sentimentDictLemmas[key]
			if (key in cd._sentimentDictLemmas): sentiments["cd"] = cd._sentimentDictLemmas[key]
			if (key in gpc._sentimentDictLemmas): sentiments["gpc"] = gpc._sentimentDictLemmas[key]
			combinedLexiconLemmas[key] = sentiments

		self._sentimentDict = combinedLexiconTokens
		self._sentimentDictLemmas = combinedLexiconLemmas

	def readAndReturnLexiconKeyDumps(self, processor):
		lexiconKeysTokens = pickle.load(open("Dumps/LexiconKeys/" + processor + "/combinedLexiconKeysTokens.p", "rb"))
		lexiconKeysLemmas = pickle.load(open("Dumps/LexiconKeys/" + processor + "/combinedLexiconKeysLemmas.p", "rb"))
		return (lexiconKeysTokens, lexiconKeysLemmas)

	def combineSentimentLexiconsKeysAndDump(self, processor):
		newLexiconKeysTokens = self.getCombinedLexiconKeysTokens(processor)
		newLexiconKeysLemmas = self.getCombinedLexiconKeysLemmas(processor)
		pickle.dump(newLexiconKeysTokens, open("Dumps/LexiconKeys/" + processor + "/combinedLexiconKeysTokens.p", "wb" ))
		pickle.dump(newLexiconKeysLemmas, open("Dumps/LexiconKeys/" + processor + "/combinedLexiconKeysLemmas.p", "wb" ))

	def getCombinedLexiconKeysTokens(self, processor):
		newLexiconKeysTokens = []
		for dictString in self._sentimentDicts:
			self.initSingleDict(dictString, processor)
			
			for key in self._sentimentDict:
				if(not(key in newLexiconKeysTokens)):
					newLexiconKeysTokens.append(key)

		return newLexiconKeysTokens

	def getCombinedLexiconKeysLemmas(self, processor):
		newLexiconKeysLemmas = []
		for dictString in self._sentimentDicts:
			self.initSingleDict(dictString, processor)
			for key in self._sentimentDictLemmas:
				if(not(key in newLexiconKeysLemmas)):
					newLexiconKeysLemmas.append(key)

		return newLexiconKeysLemmas

	
	def resetAllFiles(self):
		self.combineSentimentLexiconsKeysAndDump("treetagger")
		print("dump treetagger keys")
		self.combineSentimentLexiconsKeysAndDump("textblob")
		print("dump textblob keys")
		self.createAllFilesCombinedLexicon()
		print("combinedlexicon Files")

	def createAllFilesCombinedLexicon(self):
		self.createSentimentDictFileCombinedLexiconTokens("treetagger")
		self.createSentimentDictFileCombinedLexiconLemmas("treetagger")
		self.createSentimentDictFileCombinedLexiconLemmas("textblob")

	def createSentimentDictFileCombinedLexiconTokens(self, processor):
		self.combineSentimentLexica(processor)
		self.createOutputCombinedLexicon(self._sentimentDict, processor, "Tokens")

	def createSentimentDictFileCombinedLexiconLemmas(self, processor):
		self.combineSentimentLexica(processor)
		self.createOutputCombinedLexicon(self._sentimentDictLemmas, processor, "Lemmas")

	def createOutputCombinedLexicon(self, sentimentDict, processor, tokensOrLemmas):
		if(tokensOrLemmas == "Tokens"):
			outputFile = open("../SentimentAnalysis/TransformedLexicons/CombinedLexicon-Token.txt", "w")
		elif(tokensOrLemmas == "Lemmas"):
			outputFile = open("../SentimentAnalysis/TransformedLexicons/" + processor + "-Lemmas/CombinedLexicon.txt", "w")
		
		sentiments = ["sentiWS", "nrcPositive", "nrcNegative", "anger", "anticipation",\
		"disgust", "fear", "joy", "sadness", "surprise", "trust", "emotion", "arousel",\
		 "cdPositive", "cdNegative", "cdNeutral", "gpcPositive", "gpcNegative", "gpcNeutral"]
		firstLine = "\t".join(sentiments)
		outputFile.write(firstLine + "\n")

		for word in sentimentDict:
			sentimentGroups = sentimentDict[word]
			values = self.getValuesOfCombinedLexiconByWord(sentimentGroups)
			valueString = "\t".join(str(x) for x in values)
			lineString = word + "\t" + valueString + "\n"
			outputFile.write(lineString)
		outputFile.close()
	
	def createSimpleOutputCombinedLexicon(self):
		outputFile11 = open("../SentimentAnalysis/TransformedLexicons/CombinedLexiconGroups/CombinedLexicon-SimpleTokens1-1.txt", "w")
		outputFile12 = open("../SentimentAnalysis/TransformedLexicons/CombinedLexiconGroups/CombinedLexicon-SimpleTokens1-2.txt", "w")
		outputFile21 = open("../SentimentAnalysis/TransformedLexicons/CombinedLexiconGroups/CombinedLexicon-SimpleTokens2-1.txt", "w")
		outputFile22 = open("../SentimentAnalysis/TransformedLexicons/CombinedLexiconGroups/CombinedLexicon-SimpleTokens2-2.txt", "w")
		
		# Doesnt matter which processor to choose
		self.combineSentimentLexica("treetagger")
		keyList = list(self._sentimentDict.keys())
		partOne = keyList[:len(keyList)/2]
		partTwo = keyList[len(keyList)/2:]

		partOneOne = partOne[:len(partOne)/2]
		partOneTwo = partOne[len(partOne)/2:]

		partTwoOne = partTwo[:len(partTwo)/2]
		partTwoTwo = partTwo[len(partTwo)/2:]
		
		for word in partOneOne:
			lineString = word + "\n"
			outputFile11.write(lineString)
		outputFile11.close()
		
		for word in partOneTwo:
			lineString = word + "\n"
			outputFile12.write(lineString)
		outputFile12.close()

		for word in partTwoOne:
			lineString = word + "\n"
			outputFile21.write(lineString)
		outputFile21.close()

		for word in partTwoTwo:
			lineString = word + "\n"
			outputFile22.write(lineString)
		outputFile22.close()

	def getValuesOfCombinedLexiconByWord(self, sentimentGroups):
		values = []
		if("sentiWS" in sentimentGroups): 
			values.append(sentimentGroups["sentiWS"])
		else:
			values.append(0)

		if("nrc" in sentimentGroups):
			values.append(sentimentGroups["nrc"]["positive"])
			values.append(sentimentGroups["nrc"]["negative"])
			values.append(sentimentGroups["nrc"]["anger"])
			values.append(sentimentGroups["nrc"]["anticipation"])
			values.append(sentimentGroups["nrc"]["disgust"])
			values.append(sentimentGroups["nrc"]["fear"])
			values.append(sentimentGroups["nrc"]["joy"])
			values.append(sentimentGroups["nrc"]["sadness"])
			values.append(sentimentGroups["nrc"]["surprise"])
			values.append(sentimentGroups["nrc"]["trust"])
		else:
			values += 10 * [0]

		if("bawl" in sentimentGroups):
			values.append(sentimentGroups["bawl"]["emotion"])
			values.append(sentimentGroups["bawl"]["arousel"])
		else:
			values += 2 * [0]

		if("cd" in sentimentGroups):
			values.append(sentimentGroups["cd"]["positive"])
			values.append(sentimentGroups["cd"]["negative"])
			values.append(sentimentGroups["cd"]["neutral"])
		else:
			values += 3 * [0]

		if("gpc" in sentimentGroups):
			values.append(sentimentGroups["gpc"]["positive"])
			values.append(sentimentGroups["gpc"]["negative"])
			values.append(sentimentGroups["gpc"]["neutral"])
		else:
			values += 3 * [0]

		return values

if __name__ == "__main__":
    main()