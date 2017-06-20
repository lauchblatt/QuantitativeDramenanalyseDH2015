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

class Sentiment_Calculator:

	def __init__(self):

		self._sentimentBearingWords = []
		self._sentimentMetrics = Sentiment_Metrics()

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
			#print("### " + word._token)
			#print("Total: " + str(polaritySentiWSTotal) + " + " + str(word._polaritySentiWS))
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

		self._sentimentMetrics._polaritySentiWSTotal = polaritySentiWSTotal
		self._sentimentMetrics._positiveNrcTotal = positiveNrcTotal
		self._sentimentMetrics._negativeNrcTotal = negativeNrcTotal
		self._sentimentMetrics._angerTotal = angerTotal
		self._sentimentMetrics._anticipationTotal = anticipationTotal
		self._sentimentMetrics._disgustTotal = disgustTotal
		self._sentimentMetrics._fearTotal = fearTotal
		self._sentimentMetrics._joyTotal = joyTotal
		self._sentimentMetrics._sadnessTotal = sadnessTotal
		self._sentimentMetrics._surpriseTotal = surpriseTotal
		self._sentimentMetrics._trustTotal = trustTotal


if __name__ == "__main__":
    main()