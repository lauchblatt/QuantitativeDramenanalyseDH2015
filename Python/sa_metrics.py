#coding: utf8

import os
import re
import collections
import locale
import sys

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

if __name__ == "__main__":
    main()