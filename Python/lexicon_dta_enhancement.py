# -*- coding: utf8 -*-

import os
import re
import collections
import locale
import sys
from lexicon_handler import *

def main():
	reload(sys)
	sys.setdefaultencoding('utf8')

	dta = DTA_Handler()
	dta.extendSentimentDictWithDTAWords()

class DTA_Handler:
	def __init__(self):
		
		self._sentimentDict = {}

	def extendSentimentDictWithDTAWords(self):
		words = []
		for filename in os.listdir("../SentimentAnalysis/DTA-Output/"):
		 outputFile = open("../SentimentAnalysis/DTA-Output/" + filename) 
		 for line in outputFile:
		 	if (not line.startswith("\t")):
		 		word = line.strip()
		 		#print word
		 		words.append(word)
		print(len(words))

		lh = Lexicon_Handler()
		lh.combineSentimentLexica("treetagger")

		for sentWord in lh._sentimentDict:
			if(not sentWord in words):
				print sentWord

if __name__ == "__main__":
    main()