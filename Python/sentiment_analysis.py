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

def main():
	reload(sys)
	sys.setdefaultencoding('utf8')
	
	sa = Sentiment_Analyzer()
	sa.init()

	parser = DramaParser()
	dramaModel = parser.parse_xml("../Lessing-Dramen/less-Philotas_t.xml")
	sa.attachSAInformationToSingleDrama(dramaModel)

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

	def attachSAInformationToSingleDrama(self, dramaModel):
		lengthInWords = 0
		for act in dramaModel._acts:
			
			for configuration in act._configurations:
				
				for speech in configuration._speeches[0:3]:
					text = speech._text
					lemmasWithLanguageInfo = self.getLemmasWithLanguageInfo(text)
					
					lengthInWords = lengthInWords + len(lemmasWithLanguageInfo)					

					sentimentBearingWords = self.getSentimentBearingWords(lemmasWithLanguageInfo)
					print(len(sentimentBearingWords))
					print(lengthInWords)

	def getLemmasWithLanguageInfo(self, text):
		self._languageProcessor.processText(text)
		lemmaInformation = self._languageProcessor._lemmasWithLanguageInfo
		return lemmaInformation

	def getSentimentBearingWords(self, lemmasWithLanguageInfo):
		sentimentBearingWords = []
		
		for languageInfo in lemmasWithLanguageInfo:
			lemma = languageInfo[0]
			token = languageInfo[1][0]
			POS = languageInfo[1][1]

			sentimentBearingWord = Sentiment_Bearing_Word()
			
			if (self.isSentimentBearingWord(lemma)):
				sentimentBearingWord._lemma = lemma
				sentimentBearingWord._token = token
				sentimentBearingWord._POS = POS
				
				if(lemma in self._sentiWS):
					sentimentBearingWord._polaritySentiWS = self._sentiWS[lemma]

				if(lemma in self._nrc):
					sentiments = self._nrc[lemma]
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

				print(sentimentBearingWord)
				print(sentimentBearingWord._lemma)
				print(sentimentBearingWord._token)
				print(sentimentBearingWord._POS)
				print(sentimentBearingWord._polaritySentiWS)
				print(sentimentBearingWord._positiveNrc)
				print(sentimentBearingWord._negativeNrc)
				sentimentBearingWords.append(sentimentBearingWord)

		return sentimentBearingWords

	def isSentimentBearingWord(self, word):

		if((word in self._sentiWS) or (word in self._nrc)):
			return True
		else:
			return False


if __name__ == "__main__":
	main()