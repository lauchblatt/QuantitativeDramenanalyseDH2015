# -*- coding: utf8 -*-

import os
import re
import collections
import locale
import sys
from sentiWS import *
from nrc import *
from bawl import *
from clematide_dictionary import *
from german_polarity_clues import *
import pickle

def main():
	reload(sys)
	sys.setdefaultencoding('utf8')

	lexiconHandler = Lexicon_Handler()
	#lexiconHandler.combineSentimentLexiconsKeysAndDump("treetagger")
	#lexiconHandler.combineSentimentLexiconsKeysAndDump()

	lexiconHandler.combineSentimentLexica("treetagger")

class Lexicon_Handler:

	def __init__(self):
		self._sentimentDict = {}
		self._sentimentDictLemmas = {}
		self._sentimentDicts = ["SentiWS", "NRC", "Bawl", "CD", "GPC"]

	def initSingleDict (self, lexicon, processor):
		if (lexicon == "SentiWS"):
			self.initSentiWS(processor)
		elif (lexicon == "NRC"):
			self.initNrc(processor)
		elif (lexicon == "Bawl"):
			self.initBawl(processor)
		elif (lexicon == "CD"):
			self.initCD(processor)
		elif (lexicon == "GPC"):
			self.initGPC(processor)
		else:
			return("Kein korrekter Lexikonname wurde übergeben")
	
	def initSentiWS(self, processor):
		sentiWS = Senti_WS()
		sentiWS.readAndInitSentiWSAndLemmas(processor)
		self._sentimentDict = sentiWS._sentimentDict
		self._sentimentDictLemmas = sentiWS._sentimentDictLemmas

	def initNrc(self, processor):
		nrc = NRC()
		nrc.readAndInitNRCAndLemmas(processor)
		self._sentimentDict = nrc._sentimentDict
		self._sentimentDictLemmas = nrc._sentimentDictLemmas

	def initBawl(self, processor):
		bawl = Bawl()
		bawl.readAndInitBawlAndLemmas(processor)
		self._sentimentDict = bawl._sentimentDict
		self._sentimentDictLemmas = bawl._sentimentDictLemmas

	def initCD(self, processor):
		cd = CD()
		cd.readAndInitCDAndLemmas(processor)
		self._sentimentDict = cd._sentimentDict
		self._sentimentDictLemmas = cd._sentimentDictLemmas

	def initGPC(self, processor):
		gpc = German_Polarity_Clues()
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
		print(len(self._sentimentDict))
		print(len(self._sentimentDictLemmas))

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

if __name__ == "__main__":
    main()