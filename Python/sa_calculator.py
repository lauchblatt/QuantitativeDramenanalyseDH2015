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

	def __init__(self, sentimentBearingWords, normalisationFactorLength):

		self._sentimentBearingWords = sentimentBearingWords
		self._sentimentMetrics = Sentiment_Metrics()
		self._sentimentMetrics.initMetrics()

		self._normalisationFactorLength = normalisationFactorLength
	
	def calcMetrics(self):
		self.calcTotalMetrics()
		self.calcNormalisedMetrics()
		self.calcSentimentRatio()
	
	def calcSentimentRatio(self):
		if self._normalisationFactorLength is 0:
			sentimentRatio = 0
		else:
			sentimentRatio = float(len(self._sentimentBearingWords))/float(self._normalisationFactorLength)
			sentimentRatioPercent = sentimentRatio*100
			self._sentimentMetrics._sentimentRatio = sentimentRatioPercent

	def calcNormalisedMetrics(self):
		if self._normalisationFactorLength is 0:
			for metric in self._sentimentMetrics._metricsTotal:
				self._sentimentMetrics._metricsNormalised[metric] = 0
		else:
			for metric in self._sentimentMetrics._metricsTotal:
				metricTotal = self._sentimentMetrics._metricsTotal[metric]
				self._sentimentMetrics._metricsNormalised[metric] = float(metricTotal)/self._normalisationFactorLength

	def calcTotalMetrics(self):

		self._sentimentMetrics._metricsTotal["polaritySentiWS"] = sum(word._polaritySentiWS for word in self._sentimentBearingWords)
		self._sentimentMetrics._metricsTotal["positiveSentiWSDichotom"] = sum(word._positiveSentiWSDichotom for word in self._sentimentBearingWords)
		self._sentimentMetrics._metricsTotal["negativeSentiWSDichotom"] = sum(word._negativeSentiWSDichotom for word in self._sentimentBearingWords)
		self._sentimentMetrics._metricsTotal["polaritySentiWSDichotom"] = self._sentimentMetrics._metricsTotal["positiveSentiWSDichotom"] \
		- self._sentimentMetrics._metricsTotal["negativeSentiWSDichotom"]

		self._sentimentMetrics._metricsTotal["positiveNrc"] = sum(word._positiveNrc for word in self._sentimentBearingWords)
		self._sentimentMetrics._metricsTotal["negativeNrc"]  = sum(word._negativeNrc for word in self._sentimentBearingWords)
		self._sentimentMetrics._metricsTotal["polarityNrc"] = self._sentimentMetrics._metricsTotal["positiveNrc"] - self._sentimentMetrics._metricsTotal["negativeNrc"]

		self._sentimentMetrics._metricsTotal["anger"] = sum(word._anger for word in self._sentimentBearingWords)
		self._sentimentMetrics._metricsTotal["anticipation"] = sum(word._anticipation for word in self._sentimentBearingWords)
		self._sentimentMetrics._metricsTotal["disgust"] = sum(word._disgust for word in self._sentimentBearingWords)
		self._sentimentMetrics._metricsTotal["fear"] = sum(word._fear for word in self._sentimentBearingWords)
		self._sentimentMetrics._metricsTotal["joy"] = sum(word._joy for word in self._sentimentBearingWords)
		self._sentimentMetrics._metricsTotal["sadness"] = sum(word._sadness for word in self._sentimentBearingWords)
		self._sentimentMetrics._metricsTotal["surprise"] = sum(word._surprise for word in self._sentimentBearingWords)
		self._sentimentMetrics._metricsTotal["trust"] = sum(word._trust for word in self._sentimentBearingWords)

		self._sentimentMetrics._metricsTotal["emotion"] = sum(word._emotion for word in self._sentimentBearingWords)
		self._sentimentMetrics._metricsTotal["arousel"] = sum(word._arousel for word in self._sentimentBearingWords)
		self._sentimentMetrics._metricsTotal["positiveBawlDichotom"] = sum(word._positiveBawlDichotom for word in self._sentimentBearingWords)
		self._sentimentMetrics._metricsTotal["negativeBawlDichotom"] = sum(word._negativeBawlDichotom for word in self._sentimentBearingWords)
		self._sentimentMetrics._metricsTotal["polarityBawlDichotom"] = self._sentimentMetrics._metricsTotal["positiveBawlDichotom"] \
		- self._sentimentMetrics._metricsTotal["negativeBawlDichotom"]


		self._sentimentMetrics._metricsTotal["positiveCd"] = sum(word._positiveCd for word in self._sentimentBearingWords)
		self._sentimentMetrics._metricsTotal["negativeCd"] = sum(word._negativeCd for word in self._sentimentBearingWords)
		self._sentimentMetrics._metricsTotal["neutralCd"] = sum(word._neutralCd for word in self._sentimentBearingWords)
		self._sentimentMetrics._metricsTotal["polarityCd"] = self._sentimentMetrics._metricsTotal["positiveCd"] - self._sentimentMetrics._metricsTotal["negativeCd"]
		self._sentimentMetrics._metricsTotal["positiveCDDichotom"] = sum(word._positiveCDDichotom for word in self._sentimentBearingWords)
		self._sentimentMetrics._metricsTotal["negativeCDDichotom"] = sum(word._negativeCDDichotom for word in self._sentimentBearingWords)
		self._sentimentMetrics._metricsTotal["polarityCDDichotom"] = self._sentimentMetrics._metricsTotal["positiveCDDichotom"] \
		- self._sentimentMetrics._metricsTotal["negativeCDDichotom"]
		

		self._sentimentMetrics._metricsTotal["positiveGpc"] = sum(word._positiveGpc for word in self._sentimentBearingWords)
		self._sentimentMetrics._metricsTotal["negativeGpc"] = sum(word._negativeGpc for word in self._sentimentBearingWords)
		self._sentimentMetrics._metricsTotal["neutralGpc"] = sum(word._neutralGpc for word in self._sentimentBearingWords)
		self._sentimentMetrics._metricsTotal["polarityGpc"] = self._sentimentMetrics._metricsTotal["positiveGpc"] - self._sentimentMetrics._metricsTotal["negativeGpc"]

		self.calcMissingPosNegMetrics()

	def calcMissingPosNegMetrics(self):
		self._sentimentMetrics._metricsTotal["positiveSentiWS"] = sum(word._polaritySentiWS for word\
		 in self._sentimentBearingWords if word._polaritySentiWS > 0)
		self._sentimentMetrics._metricsTotal["negativeSentiWS"] = abs(sum(word._polaritySentiWS for word\
		 in self._sentimentBearingWords if word._polaritySentiWS < 0))

		self._sentimentMetrics._metricsTotal["positiveBawl"] = sum(word._emotion for word\
		 in self._sentimentBearingWords if word._emotion > 0)
		self._sentimentMetrics._metricsTotal["negativeBawl"] = abs(sum(word._emotion for word\
		 in self._sentimentBearingWords if word._emotion < 0))

if __name__ == "__main__":
    main()