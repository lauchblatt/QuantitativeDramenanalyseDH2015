#coding: utf8

import os
import re
import collections
import locale
import sys
from drama_parser import *
from sa_pre_processing import *
from statistic_functions import *
from sa_sentiment_analysis import *
from evaluation_test_corpus_creation import *

def main():
	reload(sys)
	sys.setdefaultencoding('utf8')

	tce = Test_Corpus_Evaluation()
	tce.initTestCorpus()

class Test_Corpus_Evaluation:
	def __init__(self):
		self._testCorpusSpeeches = []

	def initTestCorpus(self):
		tch = Test_Corpus_Handler()
		tch.readAndInitTestCorpusFromPickle("../Evaluation/Test-Korpus/UPDATED-switch-test-corpus-6.p")

		for corpusSpeech in tch._testCorpusSpeeches:
			print corpusSpeech._positionInfo
			print corpusSpeech._speech._text
			print corpusSpeech._speech._lengthInWords

if __name__ == "__main__":
    main()