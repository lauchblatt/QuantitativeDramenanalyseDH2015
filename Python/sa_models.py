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
		self._metricsNormalised = OrderedDict([])
		self._sentimentRatio = 0

	def initMetrics(self):
		self._metricsTotal["polaritySentiWS"] = 0

		self._metricsTotal["positiveNrc"] = 0
		self._metricsTotal["negativeNrc"] = 0
		self._metricsTotal["polarityNrc"] = 0

		self._metricsTotal["anger"] = 0
		self._metricsTotal["anticipation"] = 0
		self._metricsTotal["disgust"] = 0
		self._metricsTotal["fear"] = 0
		self._metricsTotal["joy"] = 0
		self._metricsTotal["sadness"] = 0
		self._metricsTotal["surprise"] = 0
		self._metricsTotal["trust"] = 0

		self._metricsTotal["emotion"] = 0
		self._metricsTotal["arousel"] = 0


	def printAllInfo(self, lengthInWords):
		print("Total Values: ")
		for metric,value in self._metricsTotal.items():
			item = metric + ": " + str(value)
			print item,
		print("\n")

		print("Normalised Values: ")
		print("Length in Words: " + str(lengthInWords))
		for metric,value in self._metricsNormalised.items():
			item = metric + ": " + str(value)
			print item,
		print("\n")

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

		#NRCData
		self._positiveNrc = 0
		self._negativeNrc = 0
		self._anger = 0
		self._anticipation = 0
		self._disgust = 0
		self._fear = 0
		self._joy = 0
		self._sadness = 0
		self._surprise = 0
		self._trust = 0

		#Bawl
		self._emotion = 0.0
		self._arousel = 0.0

		#CD
		self._positiveCd = 0
		self._negativeCd = 0
		self._neutralCd = 0

		#GPC
		self._positiveGpc = 0
		self._negativeGpc = 0
		self._neutralGpc = 0

		#Language Data
		self._token = ""
		self._lemma = ""
		self._POS = ""

	def setAllSentiments(self, sentiments):
		if("sentiWS" in sentiments):
			self._polaritySentiWS = sentiments["sentiWS"]
		
		if("nrc" in sentiments):
			self._positiveNrc = sentiments["nrc"]["positive"]
			self._negativeNrc = sentiments["nrc"]["negative"]
			self._anger = sentiments["nrc"]["anger"]
			self._anticipation = sentiments["nrc"]["anticipation"]
			self._disgust = sentiments["nrc"]["disgust"]
			self._fear = sentiments["nrc"]["fear"]
			self._joy = sentiments["nrc"]["joy"]
			self._sadness = sentiments["nrc"]["sadness"]
			self._surprise = sentiments["nrc"]["surprise"]
			self._trust = sentiments["nrc"]["trust"]
		
		if("bawl" in sentiments):
			self._emotion = sentiments["bawl"]["emotion"]
			self._arousel = sentiments["bawl"]["arousel"]

		if("cd" in sentiments):
			self._positiveCd = sentiments["cd"]["positive"]
			self._negativeCd = sentiments["cd"]["negative"]
			self._neutralCd = sentiments["cd"]["neutral"]

		if("gpc" in sentiments):
			self._positiveGpc = sentiments["gpc"]["positive"]
			self._negativeGpc = sentiments["gpc"]["negative"]
			self._neutralGpc = sentiments["gpc"]["neutral"]


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
		sentiments = ", ".join(str(x) for x in [self._polaritySentiWS,self._positiveNrc,self._negativeNrc,
		self._anger,self._anticipation,self._disgust,self._fear,self._joy,self._sadness,self._surprise,self._trust])
		bawl = ",".join([str(self._emotion), str(self._arousel)])
		info = info + " " + sentiments + " " + bawl
		return info

if __name__ == "__main__":
    main()