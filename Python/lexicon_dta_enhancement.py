# -*- coding: utf8 -*-

import os
import re
import collections
import locale
import sys
from lexicon_handler import *

def main():
	reload(sys)
	sys.setdefaultencoding('utf8')

	dta = DTA_Handler()
	dta.extendCombinedLexiconTokens()

class DTA_Handler:
	
	def __init__(self):
		
		self._wordSynonymsDict = {}

	def extendCombinedLexiconTokens(self):
		lexiconHandler = Lexicon_Handler()
		lexiconHandler.combineSentimentLexica("treetagger")
		lexiconHandler.sentimmentDict = self.extendSentimentDictDTA(lexiconHandler._sentimentDict)

	def extendSentimentDictDTA(self, sentimentDict):
		self.setWordSynonymsFromDTA()
		for word in sentimentDict.keys():
			if(word in self._wordSynonymsDict):
				sentiments = sentimentDict[word]
				synonyms = self._wordSynonymsDict[word]
				for synonym in synonyms:
					sentimentDict[synonym] = sentiments
		return sentimentDict


	def setWordSynonymsFromDTA(self):
		currentWord = ""
		synonyms = []
		wordSynonymsDict = {}
		
		for filename in os.listdir("../SentimentAnalysis/DTA-Output/"):
			outputFile = open("../SentimentAnalysis/DTA-Output/" + filename) 
		 	for line in outputFile:
		 		if (not line.startswith("\t")):
		 			word = line.strip()
		 			if(word != ""):
		 				if(currentWord != ""):
		 					wordSynonymsDict[unicode(currentWord)] = synonyms
		 				currentWord = word
		 				synonyms = []
		 		else:
		 			if(line.startswith("\t+[eqpho]") or line.startswith("\t+[eqrw]") or line.startswith("\t+[eqlemma]")):
		 				line = line.strip("\t+[eqpho]")
		 				line = line.strip("\t+[eqrw]")
		 				line = line.strip("\t+[eqlemma]")
		 				line = line.lstrip()
		 				line = line.split(" ")[0]
		 				synonym = line.strip()
		 				synonyms.append(unicode(synonym))

		self._wordSynonymsDict = wordSynonymsDict

if __name__ == "__main__":
    main()