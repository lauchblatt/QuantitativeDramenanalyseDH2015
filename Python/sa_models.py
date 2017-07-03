#coding: utf8

import os
import re
import collections
import locale
import sys
from sa_models import *

def main():
	reload(sys)
	sys.setdefaultencoding('utf8')

class Sentiment_Metrics:
	#List of SentimentBearingWord-Objects
	def __init__(self):
		self._metricsTotal = {}
		self._metricsNormalised = {}
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

		#Language Data
		self._token = ""
		self._lemma = ""
		self._POS = ""

	def printAllInformation(self):
		info = "(" + self._token + ", " + self._lemma + ", " + self._POS + "):"
		sentiments = ", ".join(str(x) for x in [self._polaritySentiWS,self._positiveNrc,self._negativeNrc,
		self._anger,self._anticipation,self._disgust,self._fear,self._joy,self._sadness,self._surprise,self._trust])

		info = info + " " + sentiments
		print info

if __name__ == "__main__":
    main()