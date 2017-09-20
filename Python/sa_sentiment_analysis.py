#coding: utf8

import os
import re
import collections
import locale
import sys
from drama_parser import *
from lexicon_handler import *
from sa_models import *
from sa_calculator import *
from sa_output import *
from sa_pre_processing import *

def main():
	reload(sys)
	sys.setdefaultencoding('utf8')

	processor = Drama_Pre_Processing("treetagger")
	dramaModel = processor.readDramaModelFromDump("Dumps/ProcessedDramas/treetagger/Nathan der Weise.p")
	
	sa = Sentiment_Analyzer(True,"textblob", True, "standardList", False)
	sentimentExtendedDramaModel = sa.attachAllSentimentInfoToDrama(dramaModel)
	
class Sentiment_Analyzer:

	def __init__(self, DTAExtension, processor, lemmaModeOn, stopwordList, caseSensitive):

		self._sentimentDict = {}
		self._lemmaModeOn = lemmaModeOn
		self._caseSensitive = caseSensitive
		self._removeStopwords = False
		self._stopwords = []

		self.initLexicons(DTAExtension, processor)
		self.initStopWords(processor, stopwordList)
	
	def attachAllSentimentInfoToDrama(self, dramaModel):
		self.attachSentimentBearingWordsToDrama(dramaModel)
		self.attachStructuralSentimentMetricsToDrama(dramaModel)
		self.attachSentimentMetricsToSpeaker(dramaModel)
		self.attachSentimentRelationsToSpeaker(dramaModel)
		return dramaModel

	def initStopWords(self, processor, stopwordList):
		if(stopwordList != None and stopwordList != ""):
			self._removeStopwords = True

		if(self._removeStopwords):
			lp = Language_Processor(processor)
			lp.setProcessor(processor)

			lp._processor.initStopWords(stopwordList)
			if(self._lemmaModeOn):
				self._stopwords = lp._processor._stopwords_lemmatized
			else:
				self._stopwords = lp._processor._stopwords
		else:
			self._stopwords = []

	def initLexicons(self, DTAExtension, processor):
		
		"""
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
		"""
		lexicon = ""
		lexiconHandler = Lexicon_Handler()
		if(DTAExtension):
			lexicon = "CombinedLexicon-DTAExtended"
		else:
			lexicon = "CombinedLexicon"

		lexiconHandler.initSingleDict(lexicon, processor)
		sentimentDictTokens = lexiconHandler._sentimentDict
		sentimentDictLemmas = lexiconHandler._sentimentDictLemmas
		if(self._lemmaModeOn):
			self._sentimentDict = sentimentDictLemmas
		else:
			self._sentimentDict = sentimentDictTokens

	def attachStructuralSentimentMetricsToDrama(self, dramaModel):
		for act in dramaModel._acts:
			for conf in act._configurations:
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
			print("Speaker")
			#speaker._sentimentMetrics.printAllInfo(speaker._lengthInWords)
		for act in dramaModel._acts:
			for name in act._actSpeakers:
				self.attachSentimentMetricsToUnit(act._actSpeakers[name])
			for conf in act._configurations:
				for name in conf._confSpeakers:
					self.attachSentimentMetricsToUnit(conf._confSpeakers[name])

	def attachSentimentRelationsToSpeaker(self, dramaModel):
		for speaker in dramaModel._speakers:
			sentimentRelations = self.createSentimentRelationsForSpeaker(speaker)
			speaker._sentimentRelations = sentimentRelations
		for act in dramaModel._acts:
			for name in act._actSpeakers:
				speaker = act._actSpeakers[name]
				sentimentRelations = self.createSentimentRelationsForSpeaker(speaker)
				speaker._sentimentRelations = sentimentRelations
			for conf in act._configurations:
				for name in conf._confSpeakers:
					speaker = conf._confSpeakers[name]
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

		for act in dramaModel._acts:
			for name in act._actSpeakers:
				speaker = act._actSpeakers[name]
				sentimentBearingWordsSpeaker = []
				for speech in speaker._speeches:
					sentimentBearingWordsSpeaker.extend(speech._sentimentBearingWords)
				speaker._sentimentBearingWords = sentimentBearingWordsSpeaker

			for conf in act._configurations:
				for name in conf._confSpeakers:
					speaker = conf._confSpeakers[name]
					sentimentBearingWordsSpeaker = []
					for speech in speaker._speeches:
						sentimentBearingWordsSpeaker.extend(speech._sentimentBearingWords)
					speaker._sentimentBearingWords = sentimentBearingWordsSpeaker

	def getSentimentBearingWordsSpeech(self, textAsLanguageInfo):				
		sentimentBearingWords = self.getSentimentBearingWords(textAsLanguageInfo)
		return sentimentBearingWords
	
	def getSentimentBearingWord(self, languageInfo, word):
		sentimentBearingWord = Sentiment_Bearing_Word()

		sentimentBearingWord._lemma = languageInfo[0]
		sentimentBearingWord._token = languageInfo[1][0]
		sentimentBearingWord._POS = languageInfo[1][1]
		#print word
		if(word in self._sentimentDict):
			allSentiments = self._sentimentDict[word]
		else:
			upperWord = word[:1].upper() + word[1:]
			lowerWord = word.lower()
			if(lowerWord in self._sentimentDict):
				#sentimentBearingWord._token = lowerWord
				allSentiments = self._sentimentDict[lowerWord]
			if(upperWord in self._sentimentDict):
				#sentimentBearingWord._token = upperWord
				allSentiments = self._sentimentDict[upperWord]

		sentimentBearingWord.setAllSentiments(allSentiments)

		return sentimentBearingWord
				
	def getSentimentBearingWords(self, lemmasWithLanguageInfo):
		sentimentBearingWords = []

		for languageInfo in lemmasWithLanguageInfo:
			if(self._lemmaModeOn):
				word = languageInfo[0]
			else:
				word = languageInfo[1][0]
			
			if (self.isSentimentBearingWordAndNotStopword(word)):
				sentimentBearingWord = self.getSentimentBearingWord(languageInfo, word)
				sentimentBearingWords.append(sentimentBearingWord)

		return sentimentBearingWords

	def isSentimentBearingWordAndNotStopword(self, word):

		if(word in self._stopwords):
			return False
		
		if(self._caseSensitive):
			if(word in self._sentimentDict):
				return True
			else:
				return False
		else:	
			upperWord = word[:1].upper() + word[1:]
			lowerWord = word.lower()

			if(upperWord in self._sentimentDict or lowerWord in self._sentimentDict):
				return True
			else:
				return False


if __name__ == "__main__":
	main()