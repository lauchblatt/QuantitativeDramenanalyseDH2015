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
	tce.attachSentimentInfoOnTestCorpus(False, True, "CombinedLexicon", "textblob")
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
			"""
			if(polarity < 0):
				print 1
			elif(polarity > 0):
				print 2
			elif(polarity == 0):
				print 0
			"""
			#print benchmark
			if(polarity < 0 and benchmark == 1):
				result._trueNegatives += 1
			elif(polarity > 0 and benchmark == 2):
				result._truePositives += 1
			elif(polarity < 0 and benchmark == 2):
				result._falseNegatives += 1
			elif(polarity > 0 and benchmark == 1):
				result._falsePositives += 1
			elif(polarity == 0 and benchmark == 1):
				result._falsePositivesAsZeros += 1
			elif(polarity == 0 and benchmark == 2):
				result._falseNegativesAsZeros += 1
			i += 1
		
		result.updateAllTruePolarities()
		result.updateFalsePolarities()
		result.setCrossTable()
		result.printCrossTable()
		result.calcMeasurements()
		print(result._accuracy)
		print(result._recallPositive)
		print(result._recallNegative)
		print(result._precisionPositive)
		print(result._precisionNegative)
		print(result._fMeasurePositive)
		print(result._fMeasureNegative)


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
		self._falseNegativesAsZeros = 0
		self._falsePositivesAsZeros = 0

		self._allFalsePositives = 0
		self._allFalseNegatives = 0
		self._allFalsePolarities = 0

		self._truePositives = 0
		self._trueNegatives = 0
		self._allTruePolarities = 0

		self._crossTable = []
		self._accuracy = 0
		self._recallPositive = 0
		self._recallNegative = 0
		self._precisionPositive = 0
		self._precisionNegative = 0
		self._fMeasurePositive = 0
		self._fMeasureNegative = 0

		self.init(polarityBenchmark)

	def calcMeasurements(self):
		self.setRecall()
		self.setPrecision()
		self.setAccuracy()
		self.setfMeasures()

	def setfMeasures(self):
		self._fMeasurePositive = \
		2 * ((self._precisionPositive * self._recallPositive)/(self._precisionPositive + self._recallPositive))

		self._fMeasureNegative = \
		2 * ((self._precisionNegative * self._recallNegative)/(self._precisionNegative + self._recallNegative))

	def setRecall(self):
		self._recallPositive = float(self._truePositives)/float(self._testCorpusPositives)
		self._recallNegative = float(self._trueNegatives)/float(self._testCorpusNegatives)

	def setPrecision(self):
		self._precisionPositive = float(self._truePositives)/float(self._truePositives + self._allFalsePositives)
		print self._trueNegatives
		print self._allFalseNegatives
		self._precisionNegative = float(self._trueNegatives)/float(self._trueNegatives + self._allFalseNegatives)

	def setAccuracy(self):
		accuracy = float(self._allTruePolarities)/float(self._testCorpusLength)
		self._accuracy = accuracy

	def setCrossTable(self):
		headline = ["Actual Class", "Predicted Negative", "Predicted Positive"]
		line1 = ["Negatives", self._testCorpusNegatives, self._trueNegatives, self._allFalsePositives]
		line2 = ["Positives", self._testCorpusPositives, self._allFalseNegatives, self._truePositives]
		self._crosstable = [headline, line1, line2]

	def printCrossTable(self):
		for row in self._crosstable:
			outputLine = [str(item) for item in row]
			outputLine = "\t".join(outputLine)
			print outputLine

	def updateAllTruePolarities(self):
		self._allTruePolarities = self._truePositives + self._trueNegatives
	
	def updateFalsePolarities(self):
		self._allFalsePositives = self._falsePositives + self._falsePositivesAsZeros
		self._allFalseNegatives = self._falseNegatives + self._falseNegativesAsZeros
		self._allFalsePolarities = self._allFalsePositives + self._allFalseNegatives

	def init(self, polarityBenchmark):
		self._testCorpusLength = len(polarityBenchmark)
		for item in polarityBenchmark:
			if(item == 1):
				self._testCorpusNegatives += 1
			if(item == 2):
				self._testCorpusPositives += 1

if __name__ == "__main__":
    main()