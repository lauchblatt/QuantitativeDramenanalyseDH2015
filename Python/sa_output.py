#coding: utf8

import os
import re
import collections
import locale
import sys
from drama_parser import *
from language_processor import *
from lexicon_handler import *
from sa_models import *
from sa_calculator import *

def main():
	reload(sys)
	sys.setdefaultencoding('utf8')

class Sentiment_Output_Generator:

	def createTxtOutputSingleDrama(self, name, dramaModel):
		outputFile = open("../SentimentAnalysis/SA-Output/" + name +".txt", "w")

		outputFile.write(dramaModel._title +"\n\n")
		outputFile.write("Sentiments for entire #DRAMA: " + "\n\n")
		dramaInformation = self.getMetrics(dramaModel)
		outputFile.write(dramaInformation)

		for act in dramaModel._acts:
			outputFile.write("\n\nSentiments for entire #ACT " + str(act._number) + ":\n\n")
			actInformation = self.getMetrics(act)
			outputFile.write(actInformation)
			for conf in act._configurations:
				outputFile.write("\n\nSentiments for entire #CONFIGURATION " + str(conf._subsequentNumber) + ":\n\n")
				confInformation = self.getMetrics(conf)
				outputFile.write(confInformation)
				for speech in conf._speeches:
					outputFile.write("\n\nSentiments for #SPEECH " + str(speech._subsequentNumber) + ":\n\n")
					speechInformation = self.getMetrics(speech)
					outputFile.write(speechInformation)
					
					sentimentBearingWordsInformation = self.getSentimentBearingWordsInformation(speech)
					outputFile.write(sentimentBearingWordsInformation)

		for speaker in dramaModel._speakers:
			outputFile.write("\n\nSentiments for entire #SPEAKER " + speaker._name +"\n\n")
			speakerInformation = self.getMetrics(speaker)
			outputFile.write(speakerInformation)

			sentimentBearingWordsInformation = self.getSentimentBearingWordsInformation(speaker)
			outputFile.write(sentimentBearingWordsInformation)

		for speaker in dramaModel._speakers:
			for sentimentRelation in speaker._sentimentRelations:
				outputFile.write("\n\n#SENTIMENT-RELATION " + speaker._name + " --> " + sentimentRelation._targetSpeaker + ":\n\n")
				sentimentInformation = self.getMetrics(sentimentRelation)
				outputFile.write(sentimentInformation)

				sentimentBearingWordsInformation = self.getSentimentBearingWordsInformation(sentimentRelation)
				outputFile.write(sentimentBearingWordsInformation)

		outputFile.close()

	def getMetrics(self, unit):
		info = "Length in Words: " + str(unit._lengthInWords) + "\n"

		if hasattr(unit, "_speeches"):
			info = info + "Number of Speeches: " + str(len(unit._speeches)) + "\n"
		else:
			pass

		info = info + "\nTotal Values:" + "\n"
		for metric in unit._sentimentMetrics._metricsTotal:
			metricValuePair = metric + ": " + str(unit._sentimentMetrics._metricsTotal[metric])
			info = info + metricValuePair +"\n"
		info = info + "\n" + "Normalised Values: " + "\n"
		for metric in unit._sentimentMetrics._metricsNormalised:
			metricValuePair = metric + ": " + str(unit._sentimentMetrics._metricsNormalised[metric])
			info = info + metricValuePair + "\n"
		info = info + "\n" + "Sentiment Ratio: " + "\n"
		info = info + str(unit._sentimentMetrics._sentimentRatio)
		return info
	
	def getSentimentBearingWordsInformation(self, unit):
		info = ("\n\nSentiment Bearing Words: \n")
		info = info + ("(Token, Lemma, POS), polaritySentiWS, nrcPositive, nrcNegative, anger, anticipation, disgust, fear, joy, sadness, surprise, trust\n")	
		for sentimentBearingWord in unit._sentimentBearingWords:
			wordInfo = sentimentBearingWord.returnInfoAsString()
			info = info + wordInfo + "\n"

		return info

	def createShortTxtOutputSingleDrama(self, name, dramaModel):
		outputFile = open("../SentimentAnalysis/SA-Output/" + name +".txt", "w")

		outputFile.write(dramaModel._title +"\n\n")
		outputFile.write("Sentiments for entire #DRAMA: " + "\n\n")
		dramaInformation = self.getMetrics(dramaModel)
		outputFile.write(dramaInformation)

		for act in dramaModel._acts:
			outputFile.write("\n\nSentiments for entire #ACT " + str(act._number) + ":\n\n")
			actInformation = self.getMetrics(act)
			outputFile.write(actInformation)
			for conf in act._configurations:
				outputFile.write("\n\nSentiments for entire #CONFIGURATION " + str(conf._subsequentNumber) + ":\n\n")
				confInformation = self.getMetrics(conf)
				outputFile.write(confInformation)

		for speaker in dramaModel._speakers:
			outputFile.write("\n\nSentiments for entire #SPEAKER " + speaker._name +"\n\n")
			speakerInformation = self.getMetrics(speaker)
			outputFile.write(speakerInformation)

		for speaker in dramaModel._speakers:
			for sentimentRelation in speaker._sentimentRelations:
				outputFile.write("\n\n#SENTIMENT-RELATION " + speaker._name + " --> " + sentimentRelation._targetSpeaker + ":\n\n")
				sentimentInformation = self.getMetrics(sentimentRelation)
				outputFile.write(sentimentInformation)

		outputFile.close()

if __name__ == "__main__":
	main()