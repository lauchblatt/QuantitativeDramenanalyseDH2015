# -*- coding: utf8 -*-

import os
import re
import collections
import locale
import sys
from shutil import copyfile

def main():
	analyzer = Analyzer()
	analyzer.analyseSpeechSentiments()


class Analyzer:

	def __init__(self):
		self._dramaSpeechValues = {}

	def analyseSpeechSentiments(self):
		negatives = 0
		positives = 0
		zeros = 0
		sumnegative = 0
		sumpositive = 0
		for drama in os.listdir("textblob"):
			textfile = open("textblob/" + drama)
			self._dramaSpeechValues[drama] = []
			i = -1
			for line in textfile.readlines():
				i = i + 1
				if line.startswith("Sentiments for #SPEECH"):
					self._dramaSpeechValues[drama].append(i+5)

		for name in self._dramaSpeechValues:
			textfile = open("textblob/" + name)
			lines = textfile.readlines()
			for linenumber in self._dramaSpeechValues[name]:
				resultLine = lines[linenumber]
				number = float(resultLine[17:])
				if number < 0:
					negatives = negatives + 1
					sumnegative = sumnegative + abs(number)
					pass
				if number > 0:
					positives = positives + 1
					sumpositive = sumpositive + abs(number)
					pass
				if number == 0:
					zeros = zeros + 1
					pass

		print negatives
		print positives
		print zeros
		print sumpositive
		print sumnegative

if __name__ == "__main__":
    main()
