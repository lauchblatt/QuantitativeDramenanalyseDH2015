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
	
	sa = Sentiment_Analyzer()
	sa.init()

	parser = DramaParser()
	dramaModel = parser.parse_xml("../Lessing-Dramen/less-Philotas_t.xml")
	sa.attachPositionsToSpeechesAndConfs(dramaModel)
	sa.attachPreOccuringSpeakersToSpeeches(dramaModel)
	sa.attachSentimentBearingWordsToDrama(dramaModel)
	sa.attachLengthInWordsToStructuralElements(dramaModel)
	sa.attachStructuralSentimentMetricsToDrama(dramaModel)
	sa.attachSentimentMetricsToSpeaker(dramaModel)
	sa.attachSpeakerRelationsToSpeaker(dramaModel)

	"""
	for act in dramaModel._acts:
		for conf in act._configurations:
			for speech in conf._speeches:
				sentimentInformation = speech._sentimentInformation
				sentimentBearingWords  = sentimentInformation._sentimentBearingWords
				for word in sentimentBearingWords:
					print(word._token)
					print(word._positiveNrc)
	"""
	
	
class Sentiment_Analyzer:

	def __init__(self):
		self._languageProcessor = None
		self._sentiWS = {}
		self._nrc = {}
	
	def init(self):
		
		self._languageProcessor = Language_Processor()
		lexiconHandlerSentiWS = Lexicon_Handler()
		lexiconHandlerSentiWS.initSingleDict("SentiWS-Lemmas")
		self._sentiWS = lexiconHandlerSentiWS._sentimentDictLemmas
		lexiconHandlerNrc = Lexicon_Handler()
		lexiconHandlerNrc.initSingleDict("NRC-Lemmas")
		self._nrc = lexiconHandlerNrc._sentimentDictLemmas

	def attachStructuralSentimentMetricsToDrama(self, dramaModel):
		for act in dramaModel._acts:
			for conf in act._configurations[0:4]:
				for speech in conf._speeches:
					print("Speech")
					self.attachSentimentMetricsToUnit(speech)
					#speech._sentimentMetrics.printAllInfo(speech._lengthInWords)
				print("Conf")
				self.attachSentimentMetricsToUnit(conf)
				#conf._sentimentMetrics.printAllInfo(conf._lengthInWords)
			print("Act")
			self.attachSentimentMetricsToUnit(act)
			#act._sentimentMetrics.printAllInfo(act._lengthInWords)
		print("Drama")
		self.attachSentimentMetricsToUnit(dramaModel)
		#dramaModel._sentimentMetrics.printAllInfo(dramaModel._lengthInWords)

	def attachSentimentMetricsToSpeaker(self, dramaModel):
		for speaker in dramaModel._speakers:
			self.attachSentimentMetricsToUnit(speaker)
			#speaker._sentimentMetrics.printAllInfo(speaker._lengthInWords)

	def attachSpeakerRelationsToSpeaker(self, dramaModel):
		for speaker in dramaModel._speakers:
			self.createSpeakerRelationsForSpeaker(speaker)

	def createSpeakerRelationsForSpeaker(self, speaker):
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

		for targetSpeaker in targetSpeakerSpeeches:
			speeches = targetSpeakerSpeeches[targetSpeaker]
			speakerRelation = Speaker_Relation(originSpeaker, targetSpeaker, speeches)
			#todo array and return

		"""
		print("############")
		print(originSpeaker)
		print(targetSpeakerSpeeches)
		for targetSpeaker in targetSpeakerSpeeches:
			print targetSpeaker
			for speech in targetSpeakerSpeeches[targetSpeaker]:
				print speech._preOccuringSpeaker
		"""

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

			for configuration in act._configurations[0:4]:
				sentimentBearingWordsConf = []

				for speech in configuration._speeches:
					text = speech._text
					speech._sentimentBearingWords = self.getSentimentBearingWordsSpeech(text)
					####
					speechLength = len(self._languageProcessor._lemmasWithLanguageInfo)
					speech._lengthInWords = speechLength
					####
						
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

	def attachLengthInWordsToStructuralElements(self, dramaModel):
		dramaLength = 0
		for act in dramaModel._acts:
			actLength = 0
			for conf in act._configurations[0:4]:
				confLength = 0
				for speech in conf._speeches:
					confLength = confLength + speech._lengthInWords
					actLength = actLength + speech._lengthInWords
					dramaLength = dramaLength + speech._lengthInWords
					#print("Speech: " + str(speech._lengthInWords))
				conf._lengthInWords = confLength
				#print("Conf: " + str(conf._lengthInWords))
			act._lengthInWords = actLength
			#print("Act: " + str(act._lengthInWords))
		dramaModel._lengthInWords = dramaLength
		#print("Drama: " + str(dramaModel._lengthInWords))

		for speaker in dramaModel._speakers:
			speakerLength = 0
			for speech in speaker._speeches:
				speakerLength = speakerLength + speech._lengthInWords
			speaker._lengthInWords = speakerLength

	def attachPositionsToSpeechesAndConfs(self, dramaModel):
		subsequentNumberSpeech = 1
		subsequentNumberConf = 1

		for act in dramaModel._acts:
			numberInAct = 1
			for conf in act._configurations:
				numberInConf = 1
				conf._subsequentNumber = subsequentNumberConf
				subsequentNumberConf = subsequentNumberConf + 1
				for speech in conf._speeches:
					speech._subsequentNumber = subsequentNumberSpeech
					speech._numberInAct = numberInAct
					speech._numberInConf = numberInConf

					subsequentNumberSpeech = subsequentNumberSpeech + 1
					numberInAct = numberInAct + 1
					numberInConf = numberInConf +1

	def attachPreOccuringSpeakersToSpeeches(self, dramaModel):
		preOccuringSpeaker = ""

		for act in dramaModel._acts:
			# Reset every speaker when new act starts
			preOccuringSpeaker = ""
			for conf in act._configurations:
				for speech in conf._speeches:
					speech._preOccuringSpeaker = preOccuringSpeaker
					preOccuringSpeaker = speech._speaker


	def getSentimentBearingWordsSpeech(self, text):
		lemmasWithLanguageInfo = self.getLemmasWithLanguageInfo(text)					
		sentimentBearingWords = self.getSentimentBearingWords(lemmasWithLanguageInfo)
		return sentimentBearingWords

	def getLemmasWithLanguageInfo(self, text):
		self._languageProcessor.processText(text)
		lemmaInformation = self._languageProcessor._lemmasWithLanguageInfo
		return lemmaInformation

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

	def getSentimentBearingWord(self, languageInfo):
		sentimentBearingWord = Sentiment_Bearing_Word()
		sentimentBearingWord._lemma = languageInfo[0]
		sentimentBearingWord._token = languageInfo[1][0]
		sentimentBearingWord._POS = languageInfo[1][1]

		self.setSentiWSInformation(sentimentBearingWord)
		self.setNrcInformation(sentimentBearingWord)

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

		if((word in self._sentiWS) or (word in self._nrc)):
			return True
		else:
			return False


if __name__ == "__main__":
	main()