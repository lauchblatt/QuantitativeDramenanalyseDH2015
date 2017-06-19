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

	def __init__(self):
		self._polaritySentiWSTotal = 0

		self._positiveNrcTotal = 0
		self._negativeNrcTotal = 0
		self._angerTotal = 0
		self._anticipationTotal = 0
		self._disgustTotal = 0
		self._fearTotal = 0
		self._joyTotal = 0
		self._sadnessTotal = 0
		self._surpriseTotal = 0
		self._trustTotal = 0

		self._sentimentBearingWords = []

	def init(self, sentimentBearingWords):
			self._sentimentBearingWords = sentimentBearingWords
			self.calcTotalMetrics()

	def calcTotalMetrics(self):
		polaritySentiWSTotal = 0
		positiveNrcTotal = 0
		negativeNrcTotal = 0
		angerTotal = 0
		anticipationTotal = 0
		disgustTotal = 0
		fearTotal = 0
		joyTotal = 0
		sadnessTotal = 0
		surpriseTotal = 0
		trustTotal = 0

		for word in self._sentimentBearingWords:
			polaritySentiWSTotal = polaritySentiWSTotal + word._polaritySentiWS
			positiveNrcTotal = positiveNrcTotal + word._positiveNrc
			negativeNrcTotal = negativeNrcTotal + word._negativeNrc
			angerTotal = angerTotal + word._anger
			anticipationTotal = anticipationTotal + word._anticipation
			disgustTotal = disgustTotal + word._disgust
			fearTotal = fearTotal + word._fear
			joyTotal = joyTotal + word._joy
			sadnessTotal = sadnessTotal + word._sadness
			surpriseTotal = surpriseTotal + word._surprise
			trustTotal = trustTotal + word._trust

		self._polaritySentiWSTotal = polaritySentiWSTotal
		self._positiveNrcTotal = positiveNrcTotal
		self._negativeNrcTotal = negativeNrcTotal
		self._angerTotal = angerTotal
		self._anticipationTotal = anticipationTotal
		self._disgustTotal = disgustTotal
		self._fearTotal = fearTotal
		self._joyTotal = joyTotal
		self._sadnessTotal = sadnessTotal
		self._surpriseTotal = surpriseTotal
		self._trustTotal = trustTotal

	def printAllInformation(self):
		sentiments = ", ".join(str(x) for x in [self._polaritySentiWSTotal,self._positiveNrcTotal,self._negativeNrcTotal,
		self._angerTotal,self._anticipationTotal,self._disgustTotal,self._fearTotal,
		self._joyTotal,self._sadnessTotal,self._surpriseTotal,self._trustTotal])
		info = "All Values: " + sentiments
		print sentiments


if __name__ == "__main__":
    main()