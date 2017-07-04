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
		outputFile.write("Sentiments for entire Drama: " + "\n\n")
		dramaInformation = self.getMetrics(dramaModel)
		outputFile.write(dramaInformation)

		for act in dramaModel._acts:
			outputFile.write("Sentiments for entire Act" + str(act._number) + ":\n\n")
			actInformation = self.getMetrics(act)
			outputFile.write(actInformation)
			for conf in act._configurations[0:2]:
				outputFile.write("Sentiments for entire Configuration" + str(conf._subsequentNumber) + ":\n\n")
				confInformation = self.getMetrics(conf)
				outputFile.write(confInformation)
				for speech in conf._speeches:
					outputFile.write("Sentiments for Speech" + str(speech._subsequentNumber) + ":\n\n")
					speechInformation = self.getMetrics(conf)
					outputFile.write(speechInformation)


		outputFile.close()

	def getMetrics(self, unit):
		info = "Total Values:" + "\n"
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

if __name__ == "__main__":
	main()