# -*- coding: utf8 -*-

import os
import re
import collections
import locale
import sys
from lexicon_handler import *
from lp_language_processor import *
from lexicon_clematide_dictionary import *

def main():
	reload(sys)
	sys.setdefaultencoding('utf8')

	ag = Agreement_Statistics()
	matrix = ag.getAgreementMatrixFromData(6, 1)
	print(ag.fleissKappa(matrix))

class Agreement_Statistics:

	def __init__(self):
		self._sentimentDict = {}

	def fleissKappa(self, matrix):
		raters = 5
		N = len(matrix)
		categories = len(matrix[0])
		allRates = N*raters
		print allRates
		pjs = []
		i = 0
		while(i < categories):
			colSum = 0
			for line in matrix:
				colSum = colSum + line[i]
			pjs.append(float(float(colSum)/allRates))
			i = i + 1
		Pis = []
		for line in matrix:
			squares = [item * item for item in line]
			squaresSum = sum(squares)
			result = (float(squaresSum - raters))/float(raters * (raters - 1))
			Pis.append(result)
		sumPis = sum(Pis)
		P_ = float(sumPis)/N
		squaresPjs = [item * item for item in pjs]
		P_e = sum(squaresPjs)
		fleiss_kappa = (P_ - P_e)/(1 - P_e)
		return fleiss_kappa

	def getAgreementMatrixFromData(self, categories, startValue):
		data = open("../Agreement-Daten/agreement_polaritaet_standard.txt")
		lines = data.readlines()
		matrixRows = []
		for line in lines:
			numbers = line.split("\t")
			numbers = [int(number.strip()) for number in numbers]
			counters = []
			i = 0
			while (i < categories):
				counters.append(0)
				i = i + 1
			for number in numbers:
				columnToIncrease = number - startValue
				counters[columnToIncrease] += 1

			output = "\t".join([str(x) for x in counters])
			print output
			matrixRows.append(counters)
		return matrixRows

if __name__ == "__main__":
    main()