#coding: utf8

import os
import re
import collections
import locale
import sys
from sa_models import *
from collections import OrderedDict

def main():
	reload(sys)
	sys.setdefaultencoding('utf8')

	sm = Sentiment_Metrics()
	sm.initMetrics()

class Sentiment_Relation:

	def __init__(self, originSpeaker, targetSpeaker, speeches):
		self._originSpeaker = originSpeaker
		self._targetSpeaker = targetSpeaker
		self._speeches = speeches

		self._sentimentBearingWords = []
		self._sentimentMetrics = None
		self._lengthInWords = 0

		self.setSentimentBearingWords()

	def setSentimentBearingWords(self):
		lengthInWords = 0
		for speech in self._speeches:
			self._sentimentBearingWords.extend(speech._sentimentBearingWords)
			lengthInWords = lengthInWords + speech._lengthInWords
		self._lengthInWords = lengthInWords


class Sentiment_Metrics:
	
	def __init__(self):
		self._metricsTotal = OrderedDict([])
		self._metricsNormalisedLengthInWords = OrderedDict([])
		self._metricsNormalisedSBWs = OrderedDict([])
		
		self._names = OrderedDict([])
		self._sentimentRatio = 0

	def initMetrics(self):
		self._metricsTotal["polaritySentiWS"] = 0
		self._metricsTotal["positiveSentiWS"] = 0
		self._metricsTotal["negativeSentiWS"] = 0
		self._metricsTotal["positiveSentiWSDichotom"] = 0
		self._metricsTotal["negativeSentiWSDichotom"] = 0
		self._metricsTotal["polaritySentiWSDichotom"] = 0
		self._names["sentiWS"] = ["polaritySentiWS", "positiveSentiWS", "negativeSentiWS", "positiveSentiWSDichotom",\
		"negativeSentiWSDichotom", "polaritySentiWSDichotom"]

		self._metricsTotal["positiveNrc"] = 0
		self._metricsTotal["negativeNrc"] = 0
		self._metricsTotal["polarityNrc"] = 0
		self._names["nrcPolarity"] = ["positiveNrc", "negativeNrc", "polarityNrc"]

		self._metricsTotal["anger"] = 0
		self._metricsTotal["anticipation"] = 0
		self._metricsTotal["disgust"] = 0
		self._metricsTotal["fear"] = 0
		self._metricsTotal["joy"] = 0
		self._metricsTotal["sadness"] = 0
		self._metricsTotal["surprise"] = 0
		self._metricsTotal["trust"] = 0
		self._names["nrcEmotion"] = ["anger", "anticipation", "disgust", "fear", "joy", "sadness",\
		"surprise", "trust"]

		self._metricsTotal["emotion"] = 0
		self._metricsTotal["arousel"] = 0
		self._metricsTotal["positiveBawl"] = 0
		self._metricsTotal["negativeBawl"] = 0
		
		
		self._metricsTotal["positiveBawlDichotom"] = 0
		self._metricsTotal["negativeBawlDichotom"] = 0
		self._metricsTotal["polarityBawlDichotom"] = 0
		self._names["bawl"] = ["emotion", "arousel", "positiveBawl", "negativeBawl", "positiveBawlDichotom",\
		"negativeBawlDichotom", "polarityBawlDichotom"]


		#CD
		self._metricsTotal["positiveCd"] = 0
		self._metricsTotal["negativeCd"] = 0
		self._metricsTotal["neutralCd"] = 0
		self._metricsTotal["polarityCd"] = 0

		self._metricsTotal["positiveCDDichotom"] = 0
		self._metricsTotal["negativeCDDichotom"] = 0
		self._metricsTotal["polarityCDDichotom"] = 0
		self._names["Cd"] = ["positiveCd", "negativeCd","neutralCd", "polarityCd", "positiveCDDichotom",\
		"negativeCDDichotom", "polarityCDDichotom"]

		#GPC
		self._metricsTotal["positiveGpc"] = 0
		self._metricsTotal["negativeGpc"] = 0
		self._metricsTotal["neutralGpc"] = 0
		self._metricsTotal["polarityGpc"] = 0
		self._names["Gpc"] = ["positiveGpc", "negativeGpc","neutralGpc", "polarityGpc"]

		self._metricsTotal["positiveCombined"] = 0
		self._metricsTotal["negativeCombined"] = 0
		self._metricsTotal["polarityCombined"] = 0
		self._names["Combined"] = ["positiveCombined", "negativeCombined", "polarityCombined"]

	def returnAllBasicMetricsLists(self):
		basicMetrics = OrderedDict([])
		basicMetrics["metricsTotal"] = self._metricsTotal
		basicMetrics["metricsNormalisedLengthInWords"] = self._metricsNormalisedLengthInWords
		basicMetrics["metricsNormalisedSBWs"] = self._metricsNormalisedSBWs

		return basicMetrics

	def printAllInfo(self, lengthInWords):
		print("Total Values: ")
		for metric,value in self._metricsTotal.items():
			item = metric + ": " + str(value)
			print item,

		print("Normalised Values: ")
		print("Length in Words: " + str(lengthInWords))
		for metric,value in self._metricsNormalisedLengthInWords.items():
			item = metric + ": " + str(value)
			print item,

		print("Sentiment Ratio: " + str(self._sentimentRatio))

		"""
		sentiments = ", ".join(str(x) for x in [self._polaritySentiWSTotal,self._positiveNrcTotal,self._negativeNrcTotal,
		self._polarityNrcTotal, self._angerTotal,self._anticipationTotal,self._disgustTotal,self._fearTotal,
		self._joyTotal,self._sadnessTotal,self._surpriseTotal,self._trustTotal])
		info = "All Values: " + sentiments
		print sentiments
		"""

class Sentiment_Bearing_Word:

	def __init__(self):
		#SentiWSData
		self._polaritySentiWS = 0
		self._positiveSentiWSDichotom = 0
		self._negativeSentiWSDichotom = 0

		self._sentiWSOccurence = 0

		#NRCData
		self._positiveNrc = 0
		self._negativeNrc = 0
		
		self._nrcPolarityOccurence = 0

		self._anger = 0
		self._anticipation = 0
		self._disgust = 0
		self._fear = 0
		self._joy = 0
		self._sadness = 0
		self._surprise = 0
		self._trust = 0
		
		self._nrcEmotionOccurence = 0
		self._nrcOccurence = 0

		#Bawl
		self._emotion = 0.0
		self._arousel = 0.0
		self._positiveBawlDichotom = 0
		self._negativeBawlDichotom = 0
		
		self._bawlOccurence = 0
		self._bawlEmotionOccurence = 0
		self._bawlArouselOccurence = 0

		#CD
		self._positiveCd = 0
		self._negativeCd = 0
		self._neutralCd = 0
		self._positiveCDDichotom = 0
		self._negativeCDDichotom = 0

		self._cdOccurence = 0

		#GPC
		self._positiveGpc = 0
		self._negativeGpc = 0
		self._neutralGpc = 0

		self._gpcOccurence = 0

		self._positiveCombined = 0
		self._negativeCombined = 0

		#Language Data
		self._token = ""
		self._lemma = ""
		self._POS = ""

	def setAllSentiments(self, sentiments):
		if("sentiWS" in sentiments):
			self._sentiWSOccurence = 1
			self._polaritySentiWS = sentiments["sentiWS"]
			if(self._polaritySentiWS > 0): self._positiveSentiWSDichotom = 1
			if(self._polaritySentiWS < 0): self._negativeSentiWSDichotom = 1
		
		if("nrc" in sentiments):
			self._nrcOccurence = 1
			self._positiveNrc = sentiments["nrc"]["positive"]
			self._negativeNrc = sentiments["nrc"]["negative"]
			if(self._positiveNrc != 0 or self._negativeNrc != 0):
				self._nrcPolarityOccurence = 1

			self._anger = sentiments["nrc"]["anger"]
			self._anticipation = sentiments["nrc"]["anticipation"]
			self._disgust = sentiments["nrc"]["disgust"]
			self._fear = sentiments["nrc"]["fear"]
			self._joy = sentiments["nrc"]["joy"]
			self._sadness = sentiments["nrc"]["sadness"]
			self._surprise = sentiments["nrc"]["surprise"]
			self._trust = sentiments["nrc"]["trust"]
			if((self._anger + self._anticipation + self._disgust + self._fear + self._joy \
				+ self._sadness + self._surprise + self._trust) != 0):
				self._nrcEmotionOccurence = 1
		
		if("bawl" in sentiments):
			self._bawlOccurence = 1
			self._emotion = sentiments["bawl"]["emotion"]
			self._arousel = sentiments["bawl"]["arousel"]

			if(self._emotion > 0): 
				self._positiveBawlDichotom = 1
				self._bawlEmotionOccurence = 1
			if(self._emotion < 0): 
				self._negativeBawlDichotom = 1
				self._bawlEmotionOccurence = 1
			if(self._arousel != 0):
				self._bawlArouselOccurence = 1

		if("cd" in sentiments):
			# need to change with inclusion of neutral words
			self._cdOccurence = 1
			self._positiveCd = sentiments["cd"]["positive"]
			self._negativeCd = sentiments["cd"]["negative"]
			self._neutralCd = sentiments["cd"]["neutral"]

			if(self._positiveCd > 0): self._positiveCDDichotom = 1
			if(self._negativeCd > 0): self._negativeCDDichotom = 1

		if("gpc" in sentiments):
			# need to change with inclusion of neutral words
			self._gpcOccurence = 1
			self._positiveGpc = sentiments["gpc"]["positive"]
			self._negativeGpc = sentiments["gpc"]["negative"]
			self._neutralGpc = sentiments["gpc"]["neutral"]

		self.setCombinedPosNeg()


	def setCombinedPosNeg(self):
		positivities = [self._positiveSentiWSDichotom, self._positiveNrc, self._positiveBawlDichotom,\
		self._positiveCDDichotom, self._positiveGpc]
		zerosPos = [x for x in positivities if x == 0]
		onesPos = [x for x in positivities if x == 1]

		if(len(onesPos) > len(zerosPos)):
			self._positiveCombined = 1
		
		negativities = [self._negativeSentiWSDichotom, self._negativeNrc, self._negativeBawlDichotom,\
		self._negativeCDDichotom, self._negativeGpc]
		zerosNeg = [x for x in negativities if x == 0]
		onesNeg =[x for x in negativities if x == 1]
		
		if(len(onesNeg) > len(zerosNeg)):
			self._negativeCombined = 1

	def printAllInformation(self):
		info = "(" + self._token + ", " + self._lemma + ", " + self._POS + "):"
		sentiments = ", ".join(str(x) for x in [self._polaritySentiWS,self._positiveNrc,self._negativeNrc,
		self._anger,self._anticipation,self._disgust,self._fear,self._joy,self._sadness,self._surprise,self._trust])
		bawl = ",".join([str(self._emotion), str(self._arousel)])
		cd = ",".join([str(self._positiveCd), str(self._negativeCd), str(self._neutralCd)])
		gpc = ",".join([str(self._positiveGpc), str(self._negativeGpc), str(self._neutralGpc)])
		info = info + " " + sentiments + " " + bawl
		print info

	def returnInfoAsString(self):
		info = "(" + self._token + ", " + self._lemma + ", " + self._POS + "):"
		sentiWs = str(self._polaritySentiWS)
		nrc = ", ".join(str(x) for x in [self._positiveNrc,self._negativeNrc,
		self._anger,self._anticipation,self._disgust,self._fear,self._joy,self._sadness,self._surprise,self._trust])
		bawl = ", ".join([str(self._emotion), str(self._arousel)])
		cd = ", ".join([str(self._positiveCd), str(self._negativeCd), str(self._neutralCd)])
		gpc = ", ".join([str(self._positiveGpc), str(self._negativeGpc), str(self._neutralGpc)])
		info = info + sentiWs + " | " + nrc + " | " + bawl + " | " + cd + " | " + gpc
		return info

if __name__ == "__main__":
    main()