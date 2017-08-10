#coding: utf8

import os
import re
import collections
import locale
import sys
from drama_parser import *
from sa_models import *
from sa_calculator import *
from sa_pre_processing import *
from sa_sentiment_analysis import *

def main():
	reload(sys)
	sys.setdefaultencoding('utf8')
	
	processor = Drama_Pre_Processing("treetagger")
	dramaModel = processor.readDramaModelFromDump("Dumps/ProcessedDramas/treetagger/Emilia Galotti.p")
	
	sa = Sentiment_Analyzer(True, "CombinedLexicon", "treetagger")
	sentimentExtendedDramaModel = sa.attachAllSentimentInfoToDrama(dramaModel)

	sog = Sentiment_Output_Generator()
	sog.generateJSONFromDrama("../SentimentAnalysis/json-test.json", sentimentExtendedDramaModel)
	#sog.createTxtOutputSingleDrama("testo2", sentimentExtendedDramaModel)
	
	#sog = Sentiment_Output_Generator()
	#sog.processAndCreateTxtOutputMutlipleDramas()
	

class Sentiment_Output_Generator:

	def __init__(self):

		self._lpProcessors = ["treetagger", "textblob"]

	def generateJSONFromDrama (self, outputFile, dramaModel):
		output = open(outputFile, "w")
		dramaData = OrderedDict([])
		dramaData['title'] = dramaModel._title
		dramaData['author'] = dramaModel._author
		dramaData['date'] = dramaModel._date
		dramaData['type'] = dramaModel._type
		dramaData['lengthInWords'] = dramaModel._lengthInWords
		dramaData['lengthSentimentBearingWords'] = len(dramaModel._sentimentBearingWords)
		dramaData['sentimentMetricsBasic'] = dramaModel._sentimentMetrics.returnAllBasicMetricsLists()
		jsonData = json.dumps(dramaData, indent=2)
		output.write(jsonData)
		output.close()

	def processAndCreateTxtOutputMutlipleDramas(self):
		for processor in self._lpProcessors:
			folder = "Dumps/ProcessedDramas/" + processor
			for filename in os.listdir(folder):
				dpp = Drama_Pre_Processing(processor)
				dramaModel = dpp.readDramaModelFromDump(folder + "/" + filename)
				sa = Sentiment_Analyzer(False, "CombinedLexicon-DTAExtended", processor)
				sentimentExtendedDramaModel = sa.attachAllSentimentInfoToDrama(dramaModel)
				self.createTxtOutputSingleDrama("DTAExtended/tokens" + "/" + filename, sentimentExtendedDramaModel)

	def createTxtOutputSingleDrama(self, name, dramaModel):
		outputFile = open("../SentimentAnalysis/SA-Output/" + name +".txt", "w")

		outputFile.write(dramaModel._title +"\n\n")
		outputFile.write("Sentiments for entire #DRAMA: " + "\n\n")
		dramaInformation = self.getMetrics(dramaModel)
		outputFile.write(dramaInformation)
		#"""
		for act in dramaModel._acts:
			outputFile.write("\n\nSentiments for entire #ACT " + str(act._number) + ":\n\n")
			actInformation = self.getMetrics(act)
			outputFile.write(actInformation)
			
			outputFile.write("\n\nSentiments for #SPEAKERSPERACT: " + str(act._number) + ":")
			for name in act._actSpeakers:
				speaker = act._actSpeakers[name]
				outputFile.write("\n\nSentiments for #SPEAKERPERACT " + speaker._name +"\n\n")
				speakerInformation = self.getMetrics(speaker)
				outputFile.write(speakerInformation)

			for conf in act._configurations:
				outputFile.write("\n\nSentiments for entire #CONFIGURATION " + str(conf._subsequentNumber) + ":\n\n")
				confInformation = self.getMetrics(conf)
				outputFile.write(confInformation)
				
				outputFile.write("\n\nSentiments for #SPEAKERSPERCONFIGURATION " + str(conf._number) + ":")
				for name in conf._confSpeakers:
					speaker = conf._confSpeakers[name]
					outputFile.write("\n\nSentiments for #SPEAKERPERCONFIGURATION " + speaker._name +"\n\n")
					speakerInformation = self.getMetrics(speaker)
					outputFile.write(speakerInformation)
					sentimentBearingWordsInformation = self.getSentimentBearingWordsInformation(speaker)
					outputFile.write(sentimentBearingWordsInformation)

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

			#sentimentBearingWordsInformation = self.getSentimentBearingWordsInformation(speaker)
			#outputFile.write(sentimentBearingWordsInformation)
		outputFile.write("\n\n#SENTIMENT-RELATION DRAMA: ")
		for speaker in dramaModel._speakers:
			for sentimentRelation in speaker._sentimentRelations:
				outputFile.write("\n\n#SENTIMENT-RELATION " + speaker._name + " --> " + sentimentRelation._targetSpeaker + ":\n\n")
				sentimentInformation = self.getMetrics(sentimentRelation)
				outputFile.write(sentimentInformation)

				#sentimentBearingWordsInformation = self.getSentimentBearingWordsInformation(sentimentRelation)
				#outputFile.write(sentimentBearingWordsInformation)
		#"""
		for act in dramaModel._acts:
			outputFile.write("\n\n#SENTIMENT-RELATION PER ACT " + str(act._number) + ":")
			for name in act._actSpeakers:
				speaker = act._actSpeakers[name]
				for sentimentRelation in speaker._sentimentRelations:
					#print ("BOING")
					outputFile.write("\n\n#SENTIMENT-RELATION " + speaker._name + " --> " + sentimentRelation._targetSpeaker + ":\n\n")
					sentimentInformation = self.getMetrics(sentimentRelation)
					outputFile.write(sentimentInformation)

			for conf in act._configurations:
				outputFile.write("\n\n#SENTIMENT-RELATION PER CONFIGURATION " + str(conf._number) + ":")
				for name in conf._confSpeakers:
					speaker = conf._confSpeakers[name]
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
		for metric in unit._sentimentMetrics._metricsNormalisedLengthInWords:
			metricValuePair = metric + ": " + str(unit._sentimentMetrics._metricsNormalisedLengthInWords[metric])
			info = info + metricValuePair + "\n"

		info = info + "\n" + "Normalised by Length of Sentiment Bearing Words Values: " + "\n"
		for metric in unit._sentimentMetrics._metricsNormalisedSBWs:
			metricValuePair = metric + ": " + str(unit._sentimentMetrics._metricsNormalisedSBWs[metric])
			info = info + metricValuePair + "\n"

		info = info + "\n" + "Sentiment Ratio: " + "\n"
		info = info + str(unit._sentimentMetrics._sentimentRatio)
		return info
	
	def getSentimentBearingWordsInformation(self, unit):
		info = ("\n\nSentiment Bearing Words: \n")
		info = info + "(Token, Lemma, POS), polaritySentiWS | nrcPositive, nrcNegative,"\
		 + "anger, anticipation, disgust, fear, joy, sadness, surprise, trust | emotion, arousel"\
		 + "positiveCd, negativeCd, neutralCd | positiveGpc, negativeGpc, neutralGpc\n"
		
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