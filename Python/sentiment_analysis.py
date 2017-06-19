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
from sa_metrics import *

def main():
	reload(sys)
	sys.setdefaultencoding('utf8')
	
	sa = Sentiment_Analyzer()
	sa.init()

	parser = DramaParser()
	dramaModel = parser.parse_xml("../Lessing-Dramen/less-Philotas_t.xml")
	sa.attachSentimentBearingWordsToSpeeches(dramaModel)

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
	for act in dramaModel._acts:
		for conf in act._configurations[0:2]:
			for speech in conf._speeches:
				saMetrics = sa.calcAndGetSentimentMetrics(speech._sentimentInformation)

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

	def attachStructuralSentimentInformationToDrama(self, dramaModel):
		print("#TODO")

	def calcAndGetSentimentMetrics(self, sentimentInformation):
		sentimentBearingWords = sentimentInformation._sentimentBearingWords
		saMetrics = Sentiment_Metrics()
		saMetrics.init(sentimentBearingWords)
		saMetrics.printAllInformation()
		return saMetrics

	def attachSentimentBearingWordsToSpeeches(self, dramaModel):
		lengthInWords = 0
		sentimentBearingWordsLength = 0
		for act in dramaModel._acts:
			for configuration in act._configurations[0:2]:
				for speech in configuration._speeches:
					text = speech._text
					lemmasWithLanguageInfo = self.getLemmasWithLanguageInfo(text)					

					sentimentBearingWords = self.getSentimentBearingWords(lemmasWithLanguageInfo)

					sentimentInformationSpeech = Sentiment_Information()
					sentimentInformationSpeech._sentimentBearingWords = sentimentBearingWords
					speech._sentimentInformation = sentimentInformationSpeech

					"""
					sentimentBearingWordsLength = sentimentBearingWordsLength + len(sentimentBearingWords)
					lengthInWords = lengthInWords + len(lemmasWithLanguageInfo)
					print(sentimentBearingWordsLength)
					print(lengthInWords)
					"""

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