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
		self._sentimentMetrics.initMetrics()

	def calcNormalisedMetrics(self, lengthInWords):
		if lengthInWords is 0:
			for metric in self._sentimentMetrics._metricsTotal:
				self._sentimentMetrics._metricsNormalised[metric] = 0
		else:
			for metric in self._sentimentMetrics._metricsTotal:
				metricTotal = self._sentimentMetrics._metricsTotal[metric]
				self._sentimentMetrics._metricsNormalised[metric] = float(metricTotal)/lengthInWords

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
		if self._sentimentBearingWords is not None:
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

		self._sentimentMetrics._metricsTotal["polaritySentiWS"] = polaritySentiWSTotal
		
		self._sentimentMetrics._metricsTotal["positiveNrc"] = positiveNrcTotal
		self._sentimentMetrics._metricsTotal["negativeNrc"]  = negativeNrcTotal
		self._sentimentMetrics._metricsTotal["polarityNrc"] = positiveNrcTotal - negativeNrcTotal

		self._sentimentMetrics._metricsTotal["anger"] = angerTotal
		self._sentimentMetrics._metricsTotal["anticipation"] = anticipationTotal
		self._sentimentMetrics._metricsTotal["disgust"] = disgustTotal
		self._sentimentMetrics._metricsTotal["fear"] = fearTotal
		self._sentimentMetrics._metricsTotal["joy"] = joyTotal
		self._sentimentMetrics._metricsTotal["sadness"] = sadnessTotal
		self._sentimentMetrics._metricsTotal["surprise"] = surpriseTotal
		self._sentimentMetrics._metricsTotal["trust"] = trustTotal


if __name__ == "__main__":
    main()