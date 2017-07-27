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
from sa_output import *
from sa_pre_processing import *

def main():
	reload(sys)
	sys.setdefaultencoding('utf8')

	processor = Drama_Pre_Processing()
	dramaModel = processor.readDramaModelFromDump("Dumps/ProcessedDramas/Der Misogyn.p")
	
	sa = Sentiment_Analyzer()
	sentimentExtendedDramaModel = sa.attachAllSentimentInfoToDrama(dramaModel)
	
	
class Sentiment_Analyzer:

	def __init__(self):
		self._languageProcessor = None
		
		self._sentiWS = {}
		self._nrc = {}
		self._bawl = {}

		self.initLexiconsAndLp()
	
	def attachAllSentimentInfoToDrama(self, dramaModel):
		self.attachSentimentBearingWordsToDrama(dramaModel)
		self.attachStructuralSentimentMetricsToDrama(dramaModel)
		self.attachSentimentMetricsToSpeaker(dramaModel)
		self.attachSentimentRelationsToSpeaker(dramaModel)
		return dramaModel

	def initLexiconsAndLp(self):
		
		self._languageProcessor = Language_Processor()
		lexiconHandlerSentiWS = Lexicon_Handler()
		lexiconHandlerSentiWS.initSingleDict("SentiWS")
		self._sentiWS = lexiconHandlerSentiWS._sentimentDictLemmas
		lexiconHandlerNrc = Lexicon_Handler()
		lexiconHandlerNrc.initSingleDict("NRC")
		self._nrc = lexiconHandlerNrc._sentimentDictLemmas
		lexiconHandlerBawl = Lexicon_Handler()
		lexiconHandlerBawl.initSingleDict("Bawl")
		self._bawl = lexiconHandlerBawl._sentimentDictLemmas

	def attachStructuralSentimentMetricsToDrama(self, dramaModel):
		for act in dramaModel._acts:
			for conf in act._configurations:
				for speech in conf._speeches:
					print("Speech")
					self.attachSentimentMetricsToUnit(speech)
					speech._sentimentMetrics.printAllInfo(speech._lengthInWords)
				print("Conf")
				self.attachSentimentMetricsToUnit(conf)
				conf._sentimentMetrics.printAllInfo(conf._lengthInWords)
			print("Act")
			self.attachSentimentMetricsToUnit(act)
			act._sentimentMetrics.printAllInfo(act._lengthInWords)
		print("Drama")
		self.attachSentimentMetricsToUnit(dramaModel)
		dramaModel._sentimentMetrics.printAllInfo(dramaModel._lengthInWords)

	def attachSentimentMetricsToSpeaker(self, dramaModel):
		for speaker in dramaModel._speakers:
			self.attachSentimentMetricsToUnit(speaker)
			print("Speaker")
			speaker._sentimentMetrics.printAllInfo(speaker._lengthInWords)

	def attachSentimentRelationsToSpeaker(self, dramaModel):
		for speaker in dramaModel._speakers:
			sentimentRelations = self.createSentimentRelationsForSpeaker(speaker)
			speaker._sentimentRelations = sentimentRelations

	def createSentimentRelationsForSpeaker(self, speaker):
		originSpeaker = speaker._name
		targetSpeakerSpeeches = {}

		for speech in speaker._speeches:
			if (speech._preOccuringSpeaker == ""):
				pass
			else:
				if (speech._preOccuringSpeaker in targetSpeakerSpeeches):
					targetSpeakerSpeeches[speech._preOccuringSpeaker].append(speech)
				else:
					targetSpeeches = []
					targetSpeeches.append(speech)
					targetSpeakerSpeeches[speech._preOccuringSpeaker] = targetSpeeches

		sentimentRelations = []
		for targetSpeaker in targetSpeakerSpeeches:
			speeches = targetSpeakerSpeeches[targetSpeaker]
			sentimentRelation = Sentiment_Relation(originSpeaker, targetSpeaker, speeches)
			self.attachSentimentMetricsToUnit(sentimentRelation)
			sentimentRelations.append(sentimentRelation)

		return sentimentRelations

	def attachSentimentMetricsToUnit(self, unit):
		sentimentMetrics = self.calcAndGetSentimentMetrics(unit._sentimentBearingWords, unit._lengthInWords)
		unit._sentimentMetrics = sentimentMetrics

	def calcAndGetSentimentMetrics(self, sentimentBearingWords, lengthInWords):
		sCalculator = Sentiment_Calculator(sentimentBearingWords, lengthInWords)
		sCalculator.calcMetrics()

		return sCalculator._sentimentMetrics

	def attachSentimentBearingWordsToDrama(self, dramaModel):
		sentimentBearingWordsDrama = []

		for act in dramaModel._acts:
			sentimentBearingWordsAct = []

			for configuration in act._configurations:
				sentimentBearingWordsConf = []

				for speech in configuration._speeches:
					textAsLanguageInfo = speech._textAsLanguageInfo
					speech._sentimentBearingWords = self.getSentimentBearingWordsSpeech(textAsLanguageInfo)
						
					sentimentBearingWordsConf.extend(speech._sentimentBearingWords)
					sentimentBearingWordsAct.extend(speech._sentimentBearingWords)
					sentimentBearingWordsDrama.extend(speech._sentimentBearingWords)

				configuration._sentimentBearingWords = sentimentBearingWordsConf

			act._sentimentBearingWords = sentimentBearingWordsAct

		dramaModel._sentimentBearingWords = sentimentBearingWordsDrama

		self.attachSentimentBearingWordsToSpeakers(dramaModel)

	def attachSentimentBearingWordsToSpeakers(self, dramaModel):
		for speaker in dramaModel._speakers:
			sentimentBearingWordsSpeaker = []
			for speech in speaker._speeches:
				sentimentBearingWordsSpeaker.extend(speech._sentimentBearingWords)
			speaker._sentimentBearingWords = sentimentBearingWordsSpeaker

	def getSentimentBearingWordsSpeech(self, textAsLanguageInfo):				
		sentimentBearingWords = self.getSentimentBearingWords(textAsLanguageInfo)
		return sentimentBearingWords

	def setSentiWSInformation(self, sentimentBearingWord):
		if(sentimentBearingWord._lemma in self._sentiWS):
			sentimentBearingWord._polaritySentiWS = self._sentiWS[sentimentBearingWord._lemma]
	
	def setNrcInformation(self, sentimentBearingWord):
		if(sentimentBearingWord._lemma in self._nrc):
			sentiments = self._nrc[sentimentBearingWord._lemma]
			sentimentBearingWord._positiveNrc = sentiments["positive"]
			sentimentBearingWord._negativeNrc = sentiments["negative"]
			sentimentBearingWord._anger = sentiments["anger"]
			sentimentBearingWord._anticipation = sentiments["anticipation"]
			sentimentBearingWord._disgust = sentiments["disgust"]
			sentimentBearingWord._fear = sentiments["fear"]
			sentimentBearingWord._joy = sentiments["joy"]
			sentimentBearingWord._sadness = sentiments["sadness"]
			sentimentBearingWord._surprise = sentiments["surprise"]
			sentimentBearingWord._trust = sentiments["trust"]

	def setBawlInformation(self, sentimentBearingWord):
		if(sentimentBearingWord._lemma in self._bawl):
			info = self._bawl[sentimentBearingWord._lemma]
			sentimentBearingWord._emotion = info["emotion"]
			sentimentBearingWord._arousel = info["arousel"]
	
	def getSentimentBearingWord(self, languageInfo):
		sentimentBearingWord = Sentiment_Bearing_Word()
		sentimentBearingWord._lemma = languageInfo[0]
		sentimentBearingWord._token = languageInfo[1][0]
		sentimentBearingWord._POS = languageInfo[1][1]

		self.setSentiWSInformation(sentimentBearingWord)
		self.setNrcInformation(sentimentBearingWord)
		self.setBawlInformation(sentimentBearingWord)

		return sentimentBearingWord
				
	def getSentimentBearingWords(self, lemmasWithLanguageInfo):
		sentimentBearingWords = []

		for languageInfo in lemmasWithLanguageInfo:
			lemma = languageInfo[0]
			
			if (self.isSentimentBearingWord(lemma)):
				sentimentBearingWord = self.getSentimentBearingWord(languageInfo)
				sentimentBearingWords.append(sentimentBearingWord)

		return sentimentBearingWords

	def isSentimentBearingWord(self, word):

		if((word in self._sentiWS) or (word in self._nrc) or (word in self._bawl)):
			return True
		else:
			return False


if __name__ == "__main__":
	main()