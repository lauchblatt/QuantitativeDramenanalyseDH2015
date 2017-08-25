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
	la = Lexicon_Handler()
	la.initSingleDict("NRC", "treetagger")
	sentimentDict = la._sentimentDict
	print (len(sentimentDict))
	sentimentDict = dta.extendSentimentDictDTA(sentimentDict)
	print(len(sentimentDict))

class DTA_Handler:
	
	def __init__(self):
		
		self._wordSynonymsDict = {}

	def extendSentimentDictDTA(self, sentimentDict):
		self.setWordSynonymsFromDTA()
		for word in sentimentDict.keys():
			if(word in self._wordSynonymsDict):
				sentiments = sentimentDict[word]
				synonyms = self._wordSynonymsDict[word]
				for synonym in synonyms:
						sentimentDict[synonym] = sentiments

		return sentimentDict

	def getBetterValues(self, lexicon, newValues, oldValues):
		["SentiWS", "NRC", "Bawl", "CD", "GPC"]
		if(lexicon == "SentiWS"):
			return self.getBetterValueSentiWS(newValues, oldValues)
		elif("NRC"):
			return self.getBetterValuesNRC(newValues, oldValues)
		elif(lexicon == "Bawl"):
			return self.geBetterValuesBawl(newValues, oldValues)
		elif(lexicon == "CD"):
			return self.getBetterValuesCD(newValues, oldValues)
		elif(lexicon == "GPC"):
			return self.getBetterValuesGPC(newValues, oldValues)

	def getBetterValueSentiWS(self, newValue, oldValue):
		if(abs(newValue) > abs(oldValue)):
			return newValue
		else:
			return oldValue

	def getBetterValuesNRC(self, newSentiments, oldSentiments):
		newSentimentsScore = 0
		oldSentimentsScore = 0
		doublePolarityNew = (newSentiments["positive"] == 1 and newSentiments["negative"] == 1)
		doublePolarityOld = (oldSentiments["positive"] == 1 and oldSentiments["negative"] == 1)
		isNeutralNew = all(value == 0 for value in newSentiments.values())
		isNeutralOld = all(value == 0 for value in oldSentiments.values())
		if(doublePolarityNew == True and doublePolarityOld == False and isNeutralOld == False):
			return oldSentiments
		if(doublePolarityOld == True and doublePolarityNew == False and isNeutralNew == False):
			return newSentiments

		for sentiment in newSentiments:
			newSentimentsScore = newSentimentsScore + newSentiments[sentiment]
		for sentiment in oldSentiments:
			oldSentimentsScore = oldSentimentsScore + oldSentiments[sentiment]

		if(newSentimentsScore > oldSentimentsScore):
			return newSentiments
		else:
			return oldSentiments

	def getBetterValuesBawl(self, newValues, oldValues):
		newEmotion = abs(newValues["emotion"])
		newArousel = newValues["arousel"]
		oldEmotion = abs(oldValues["emotion"])
		oldArousel = oldValues["arousel"]
		if(newEmotion > oldEmotion):
			return newValues
		elif(newArousel > oldArousel):
			return newValues
		return oldValues

	def getBetterValuesCD(self, newValues, oldValues):
		# if somethin is neutral take the other
		highestSentimentValues = self.getHigherSentimentValuesCD(newSentiments, oldSentiments)
		if(highestSentimentValues["positive"] != 0):
			highestSentimentValues["neutral"] = 0
			highestSentimentValues["negative"] = 0
			return highestSentimentValues
		else:
			if(highestSentimentValues["negative"] != 0):
				highestSentimentValues["neutral"] = 0
				return highestSentimentValues
			else:
				return highestSentimentValues

	def getBetterValuesGPC(self, newValues, oldValues):
		if(newValues["neutral"] > oldValues["neutral"]):
			return oldValues
		else:
			if(newValues["positive"] > oldValues["positive"]):
				return newValues
			else:
				return oldValues

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