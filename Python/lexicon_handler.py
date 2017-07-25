# -*- coding: utf8 -*-

import os
import re
import collections
import locale
import sys
from language_processor import *
from sentiWS import *
from nrc import *
from bawl import *
from clematide_dictionary import *

def main():
	reload(sys)
	sys.setdefaultencoding('utf8')

	lexiconHandler = Lexicon_Handler()
	lexiconHandler.initSingleDict("CD")

	print(len(lexiconHandler._sentimentDict))
	print(len(lexiconHandler._sentimentDictLemmas))

class Lexicon_Handler:

	def __init__(self):
		self._sentimentDict = {}
		self._sentimentDictLemmas = {}

	def initSingleDict (self, lexicon):
		if (lexicon == "SentiWS"):
			self.initSentiWS()
		elif (lexicon == "NRC"):
			self.initNrc()
		elif (lexicon == "Bawl"):
			self.initBawl()
		elif (lexicon == "CD"):
			self.initCD()
		else:
			return("Kein korrekter Lexikonname wurde übergeben")
	
	def initSentiWS(self):
		sentiWS = Senti_WS()
		sentiWS.readAndInitSentiWSAndLemmas()
		self._sentimentDict = sentiWS._sentimentDict
		self._sentimentDictLemmas = sentiWS._sentimentDictLemmas

	def initNrc(self):
		nrc = NRC()
		nrc.readAndInitNRCAndLemmas()
		self._sentimentDict = nrc._sentimentDict
		self._sentimentDictLemmas = nrc._sentimentDictLemmas

	def initBawl(self):
		bawl = Bawl()
		bawl.readAndInitBawlAndLemmas()
		self._sentimentDict = bawl._sentimentDict
		self._sentimentDictLemmas = bawl._sentimentDictLemmas

	def initCD(self):
		cd = CD()
		cd.readAndInitCDAndLemmas()
		self._sentimentDict = cd._sentimentDict
		self._sentimentDictLemmas = cd._sentimentDictLemmas

if __name__ == "__main__":
    main()