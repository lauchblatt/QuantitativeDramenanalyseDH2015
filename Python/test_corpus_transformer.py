#coding: utf8

import os
import re
import collections
import locale
import sys
from evaluation_test_corpus_creation import *

def main():
	reload(sys)
	sys.setdefaultencoding('utf8')
	tct = Test_Corpus_Transformer()
	tct.readAndInitTestCorpusHandler("test")
	tct.printTable()

# Class to create a Test-Corpus for Evaluation Purposes
class Test_Corpus_Transformer:

	def __init__(self):
		self._tch = None

	def readAndInitTestCorpusHandler(self,path):
		self._tch = Test_Corpus_Handler()
		self._tch.readAndInitTestCorpusFromPickle("Dumps/testCorpus_treetagger.p")

	def printTable(self):
		for tc_speech in self._tch._testCorpusSpeeches:
			print tc_speech._id
			print tc_speech._dramaTitle
			print tc_speech._positionInfo
			previousSpeech = tc_speech._previousSpeech._speaker + ":\n" + tc_speech._previousSpeech._text
			speechToRate = tc_speech._speech._speaker + ":\n" + tc_speech._speech._text
			nextSpeech = tc_speech._nextSpeech._speaker + ":\n" + tc_speech._nextSpeech._text
			print previousSpeech
			print speechToRate
			print nextSpeech

class Test_Corpus_Speech:

	def __init__(self, speech, previousSpeech, nextSpeech, dramaTitle, actNumber, confNumber, speechNumberInConf):
		self._speech = speech
		self._previousSpeech = previousSpeech
		self._nextSpeech = nextSpeech
		self._dramaTitle = dramaTitle

		self._actNumber = actNumber
		self._confNumber = confNumber
		self._speechNumberInConf = speechNumberInConf
		
		self._positionInfo = ""
		self._id = -1
		#self.setPositionInfo()

	def setPositionInfo(self):
		self._positionInfo = str(self._actNumber) + ".Akt, " + str(self._confNumber) + \
		".Szene, " + str(self._speechNumberInConf) + ".Replik" + ", Drama-Nummer: " + str(self._speech._subsequentNumber) + \
		", ID:" + str(self._id)

if __name__ == "__main__":
    main()