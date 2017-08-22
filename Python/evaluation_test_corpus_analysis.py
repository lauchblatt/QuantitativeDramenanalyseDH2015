#coding: utf8

import os
import re
import collections
import locale
import sys
from drama_parser import *
from sa_pre_processing import *
from statistic_functions import *
from sa_sentiment_analysis import *
from evaluation_test_corpus_creation import *

def main():
	reload(sys)
	sys.setdefaultencoding('utf8')

	tce = Test_Corpus_Evaluation()
	tce.initTestCorpus("Dumps/TestCorpus/testCorpus_" + "treetagger" + ".p")
	tce.attachSentimentInfoOnTestCorpus(False, True, "CombinedLexicon", "treetagger")
	tce.initPolarityBenchmark("../Evaluation/Test-Korpus-Evaluation/Benchmark-Daten/Polaritaet_dichotom.txt")
	tce.comparePolarityMetricWithBenchmark("polaritySentiWS")

class Test_Corpus_Evaluation:
	def __init__(self):
		self._testCorpusSpeeches = []
		self._polarityBenchmark = []
		self._polarityNames = ["polaritySentiWS", "polaritySentiWSDichotom", "polarityNrc", "emotion", "polarityBawlDichotom"\
		"polarityCd", "polarityCdDichotom", "polarityGpc", "polarityCombined"]

	def attachSentimentInfoOnTestCorpus(self, removeStopwords, lemmaModeOn, lexicon, processor):
		sa = Sentiment_Analyzer(removeStopwords, lemmaModeOn, lexicon, processor)

		for testCorpusSpeech in self._testCorpusSpeeches:
			textAsLanguageInfo = testCorpusSpeech._speech._textAsLanguageInfo
			testCorpusSpeech._speech._sentimentBearingWords = sa.getSentimentBearingWordsSpeech(textAsLanguageInfo)
			sa.attachSentimentMetricsToUnit(testCorpusSpeech._speech)

	def comparePolarityMetricWithBenchmark(self, polarityMetric):
		result = Comparison_Result_Polarity(self._polarityBenchmark)

		i = 0
		while(i < len(self._polarityBenchmark)):
			polarity = self._testCorpusSpeeches[i]._speech._sentimentMetrics._metricsTotal[polarityMetric]
			benchmark = self._polarityBenchmark[i]
			
			if(polarity < 0 and benchmark == 1):
				result._correctNegatives += 1
			elif(polarity > 0 and benchmark == 2):
				result._correctPositives += 1
			elif(polarity < 0 and benchmark == 2):
				result._falseNegatives += 1
			elif(polarity > 0 and benchmark == 1):
				result._falsePositives += 1
			elif(polarity == 0 and benchmark == 1):
				result._positiveZeros += 1
			elif(polarity == 0 and benchmark == 2):
				result._negativeZeros += 1
			i += 1
			


	def initPolarityBenchmark(self, pathToBenchmark):
		polarityBenchmark = []
		data = open(pathToBenchmark)
		lines = data.readlines()
		for line in lines:
			number = int(line.strip())
			polarityBenchmark.append(number)
		self._polarityBenchmark = polarityBenchmark

	def initTestCorpus(self, path):
		tcc = Test_Corpus_Creator()
		tcc.readAndInitTestCorpusFromPickle(path)
		self._testCorpusSpeeches = tcc._testCorpusSpeeches


class Comparison_Result_Polarity:
	
	def __init__(self, polarityBenchmark):
		self._testCorpusLength = 0
		self._testCorpusPositives = 0
		self._testCorpusNegatives = 0
		self._falsePositives = 0
		self._falseNegatives = 0
		self._negativeZeros = 0
		self._positiveZeros = 0
		self._allFalsePositives = 0
		self._allFalseNegatives = 0
		self._allFalsePolarities = 0
		self._truePositives = 0
		self._trueNegatives = 0
		self._allCorrectPolarities = 0

		self.init(polarityBenchmark)

	def init(self, polarityBenchmark):
		self._testCorpusLength = len(polarityBenchmark)
		for item in polarityBenchmark:
			if(item == 1):
				self._testCorpusNegatives += 1
			if(item == 2):
				self._testCorpusPositives += 1

if __name__ == "__main__":
    main()