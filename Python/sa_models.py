#coding: utf8

import os
import re
import collections
import locale
import sys

def main():
	reload(sys)
	sys.setdefaultencoding('utf8')

class Sentiment_Information:
	#List of SentimentBearingWord-Objects
	def __init__(self):
		self._sentimentBearingWords = []

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