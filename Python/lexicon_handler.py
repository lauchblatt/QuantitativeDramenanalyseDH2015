# -*- coding: utf8 -*-

import os
import re
import collections
import locale
import sys
from language_processor import *
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
	lexiconHandler.combineSentimentLexicons()
	#lexiconHandler.initSingleDict("GPC")
	#print(len(lexiconHandler._sentimentDict))
	#print(len(lexiconHandler._sentimentDictLemmas))

class Lexicon_Handler:

	def __init__(self):
		self._sentimentDict = {}
		self._sentimentDictLemmas = {}
		self._sentimentDicts = ["SentiWS", "NRC", "Bawl", "CD", "GPC"]

	def initSingleDict (self, lexicon):
		if (lexicon == "SentiWS"):
			self.initSentiWS()
		elif (lexicon == "NRC"):
			self.initNrc()
		elif (lexicon == "Bawl"):
			self.initBawl()
		elif (lexicon == "CD"):
			self.initCD()
		elif (lexicon == "GPC"):
			self.initGPC()
		else:
			return("Kein korrekter Lexikonname wurde übergeben")
	
	def initSentiWS(self):
		sentiWS = Senti_WS()
		sentiWS.readAndInitSentiWSAndLemmas()
		self._sentimentDict = sentiWS._sentimentDict
		self._sentimentDictLemmas = sentiWS._sentimentDictLemmas

	def initNrc(self):
		nrc = NRC()
		nrc.readAndInitNRCAndLemmas()
		self._sentimentDict = nrc._sentimentDict
		self._sentimentDictLemmas = nrc._sentimentDictLemmas

	def initBawl(self):
		bawl = Bawl()
		bawl.readAndInitBawlAndLemmas()
		self._sentimentDict = bawl._sentimentDict
		self._sentimentDictLemmas = bawl._sentimentDictLemmas

	def initCD(self):
		cd = CD()
		cd.readAndInitCDAndLemmas()
		self._sentimentDict = cd._sentimentDict
		self._sentimentDictLemmas = cd._sentimentDictLemmas

	def initGPC(self):
		gpc = German_Polarity_Clues()
		gpc.readAndInitGPCAndLemmas()
		self._sentimentDict = gpc._sentimentDict
		self._sentimentDictLemmas = gpc._sentimentDictLemmas

	def combineSentimentLexicons(self):
		keys = self.readAndReturnLexiconKeyDumps()
		lexiconKeysTokens = keys[0]
		lexiconKeysLemma = keys[1]
		
		sentiWS = Senti_WS()
		sentiWS.readAndInitSentiWSAndLemmas()

		nrc = NRC()
		nrc.readAndInitNRCAndLemmas()

		bawl = Bawl()
		bawl.readAndInitBawlAndLemmas()

		cd = CD()
		cd.readAndInitCDAndLemmas()

		gpc = German_Polarity_Clues()
		gpc.readAndInitGPCAndLemmas()

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

		for key in lexiconKeysLemmas:
			sentiments = {}
			if (key in sentiWS._sentimentDict): sentiments["sentiWS"] = sentiWS._sentimentDict[key]
			if (key in nrc._sentimentDict): sentiments["nrc"] = nrc._sentimentDict[key]
			if (key in bawl._sentimentDict): sentiments["bawl"] = bawl._sentimentDict[key]
			if (key in cd._sentimentDict): sentiments["cd"] = cd._sentimentDict[key]
			if (key in gpc._sentimentDict): sentiments["gpc"] = gpc._sentimentDict[key]
			combinedLexiconLemmas[key] = sentiments

		return (combinedLexiconTokens, combinedLexiconLemmas)

	def readAndReturnLexiconKeyDumps(self):
		lexiconKeysTokens = pickle.load(open("Dumps/combinedLexiconKeysTokens.p", "rb"))
		lexiconKeysLemmas = pickle.load(open("Dumps/combinedLexiconKeysLemmas.p", "rb"))
		return (lexiconKeysTokens, lexiconKeysLemmas)

	def combineSentimentLexiconsKeysAndDump(self):
		newLexiconKeysTokens = self.getCombinedLexiconKeysTokens()
		newLexiconKeysLemmas = self.getCombinedLexiconKeysLemmas()
		pickle.dump(newLexiconKeysTokens, open("Dumps/combinedLexiconKeysTokens.p", "wb" ))
		pickle.dump(newLexiconKeysLemmas, open("Dumps/combinedLexiconKeysLemmas.p", "wb" ))

	def getCombinedLexiconKeysTokens(self):
		newLexiconKeysTokens = []
		for dictString in self._sentimentDicts:
			self.initSingleDict(dictString)
			
			for key in self._sentimentDict:
				if(not(key in newLexiconKeysTokens)):
					newLexiconKeysTokens.append(key)

		return newLexiconKeysTokens

	def getCombinedLexiconKeysLemmas(self):
		newLexiconKeysLemmas = []
		for dictString in self._sentimentDicts:
			self.initSingleDict(dictString)
			for key in self._sentimentDictLemmas:
				if(not(key in newLexiconKeysLemmas)):
					newLexiconKeysLemmas.append(key)

		return newLexiconKeysLemmas

if __name__ == "__main__":
    main()