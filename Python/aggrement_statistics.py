# -*- coding: utf8 -*-

import os
import re
import collections
import locale
import sys
from lexicon_handler import *
from lp_language_processor import *
from lexicon_clematide_dictionary import *
from k_alpha import *

def main():
	reload(sys)
	sys.setdefaultencoding('utf8')

	#matrix = [[0,0,0,0,14],[0,2,6,4,2],[0,0,3,5,6],[0,3,9,2,0],[2,2,8,1,1],[7,7,0,0,0],[3,2,6,3,0],[2,5,3,2,2],[6,5,2,1,0],[0,2,2,3,7]]
	#matrix = [[5, 0], [5, 0], [0, 5], [5, 0], [5, 0], [5, 0]]
	ag = Agreement_Statistics()
	print(ag.calcKAlphaForAllDramas("../Agreement-Daten/polaritaet_standard.txt"))
	#matrix = ag.getTwoDMatrix("../Agreement-Daten/ekel.txt")
	#print krippendorff_alpha(matrix, nominal_metric, missing_items="*")
	#ag.printAllInfo("../Agreement-Daten/zorn.txt", "../Agreement-Daten/zorn_sortiert.txt", 2, 0)
	#ag.calcFleissCappaForAllDramas(2,1)
	#ag.calcFleissCappaForLengths("../Agreement-Daten/angst_sortiert.txt", 2, 0)
	#ag.getAvgPercentsForAllDramas("../Agreement-Daten/angst.txt")
	#ag.getAvgPercentsForLengths("../Agreement-Daten/angst_sortiert.txt")
	#ag.getAgreementMatrixFromData("../Agreement-Daten/zorn.txt", 2, 0)
	#matrix = ag.getAgreementMatrixFromData("../Agreement-Daten/polaritaet_dichotom.txt",2,1)
	#ag.getNumberAndPercentsOfTotalAgreements(matrix)
	#matrix = ag.getAgreementMatrixFromData(6, 1)
	#print(str(ag.fleissKappa(matrix))).replace(".", ",")
	#ag.calcFleissCappaForAllDramas("../Agreement-Daten/angst.txt", 2, 0)

	#print (ag.fleissKappa(matrix))

class Agreement_Statistics:

	def __init__(self):
		self._sentimentDict = {}

	def printAllInfo(self, pathNormal, pathToSorted, categories, startValue):
		fleissKappaAndTotalAgreementData = self.calcFleissCappaAndTotalAgreementForAllDramas(pathNormal, categories, startValue)
		fleissKappas = fleissKappaAndTotalAgreementData[0]
		totalAgreementsData= fleissKappaAndTotalAgreementData[1]
		averages = self.getAvgPercentsForAllDramas(pathNormal)
		i = 0
		while(i < len(fleissKappas)):
			print "\t".join([str(fleissKappas[i]), str(totalAgreementsData[i][0]),\
			 str(totalAgreementsData[i][1]), averages[i][0], averages[i][1]])
			i += 1
		
		fleissKappaAndTotalAgreementData = self.calcFleissCappaAndTotalAgreementForAllLengths(pathToSorted, categories, startValue)
		fleissKappas = fleissKappaAndTotalAgreementData[0]
		totalAgreementsData= fleissKappaAndTotalAgreementData[1]
		averages = self.getAvgPercentsForLengths(pathToSorted)

		i = 0
		print ("\n".rstrip())
		while(i < len(fleissKappas)):
			print "\t".join([str(fleissKappas[i]), str(totalAgreementsData[i][0]),\
			 str(totalAgreementsData[i][1]), averages[i][0], averages[i][1]])
			i += 1

	def fleissKappa(self, matrix):
		raters = 5
		N = len(matrix)
		categories = len(matrix[0])
		allRates = N*raters
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
		if (1 - P_e == 0):
			return 1
		fleiss_kappa = (P_ - P_e)/(1 - P_e)
		return fleiss_kappa

	def getTwoDMatrix(self, path):
		data = open(path)
		lines = data.readlines()
		twoDMatrix = []
		for line in lines:
			numbers = line.split("\t")
			numbers = [number.strip() for number in numbers]
			twoDMatrix.append(numbers)
		twoDMatrix = zip(*twoDMatrix)
		twoDMatrix = [list(unit) for unit in twoDMatrix]
		return twoDMatrix

	def getAgreementMatrixFromData(self, path, categories, startValue):
		data = open(path)
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
			matrixRows.append(counters)
		return matrixRows

	def getNumberAndPercentsOfTotalAgreements(self, agreementMatrix):
		totalAgreements = 0
		for row in agreementMatrix:
			for number in row:
				if(int(number) == 5):
					totalAgreements += 1
		#print totalAgreements
		percent = str(float(totalAgreements)/len(agreementMatrix)).replace(".", ",")
		return (totalAgreements, percent)

	def calcKAlphaForAllDramas(self, path):
		matrix = self.getTwoDMatrix(path)
		dramas = []
		dramas.append([row[0:6] for row in matrix])
		dramas.append([row[6:26] for row in matrix])
		dramas.append([row[26:54] for row in matrix])
		dramas.append([row[54:68] for row in matrix])
		dramas.append([row[68:80] for row in matrix])
		dramas.append([row[80:92] for row in matrix])
		dramas.append([row[92:102] for row in matrix])
		dramas.append([row[102:122] for row in matrix])
		dramas.append([row[122:146] for row in matrix])
		dramas.append([row[146:166] for row in matrix])
		dramas.append([row[166:194] for row in matrix])
		dramas.append([row[194:200] for row in matrix])
		
		kAlphas = []
		for dramaMatrix in dramas:
			kAlphas.append(krippendorff_alpha(dramaMatrix, nominal_metric, missing_items="*"))
		return kAlphas

	def calcFleissCappaAndTotalAgreementForAllDramas(self, path, categories, startValue):
		data = open(path)
		lines = data.readlines()
		matrixRows = []
		dramaLines = []
		dramaLines.append(lines[0:6])
		dramaLines.append(lines[6:26])
		dramaLines.append(lines[26:54])
		dramaLines.append(lines[54:68])
		dramaLines.append(lines[68:80])
		dramaLines.append(lines[80:92])
		dramaLines.append(lines[92:102])
		dramaLines.append(lines[102:122])
		dramaLines.append(lines[122:146])
		dramaLines.append(lines[146:166])
		dramaLines.append(lines[166:194])
		dramaLines.append(lines[194:200])
		dramaLines.append(lines)
		fleissKappas = []
		totalAgreementData = []

		for lines in dramaLines:
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
				matrixRows.append(counters)
			fleissKappas.append((str(self.fleissKappa(matrixRows))).replace(".", ","))
			numberAndPercents = self.getNumberAndPercentsOfTotalAgreements(matrixRows)
			totalAgreementData.append(numberAndPercents)
			#print numberAndPercents[0]
			#print str(numberAndPercents[1]).replace(".", ",")
		return (fleissKappas, totalAgreementData)

	def calcFleissCappaAndTotalAgreementForAllLengths(self, path, categories, startValue):
		data = open(path)
		lines = data.readlines()
		matrixRows = []
		dramaLines = []
		dramaLines.append(lines[0:101])
		dramaLines.append(lines[101:200])
		dramaLines.append(lines[0:61])
		dramaLines.append(lines[61:200])
		fleissKappas = []
		totalAgreementData = []

		for lines in dramaLines:
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
				matrixRows.append(counters)
			fleissKappas.append((str(self.fleissKappa(matrixRows))).replace(".", ","))
			numberAndPercents = self.getNumberAndPercentsOfTotalAgreements(matrixRows)
			totalAgreementData.append(numberAndPercents)
		return (fleissKappas, totalAgreementData)

	def getAvgPercentsForAllDramas(self, path):
		data = open(path)
		lines = data.readlines()
		matrixRows = []
		dramaLines = []
		#"""
		dramaLines.append(lines[0:6])
		dramaLines.append(lines[6:26])
		dramaLines.append(lines[26:54])
		dramaLines.append(lines[54:68])
		dramaLines.append(lines[68:80])
		dramaLines.append(lines[80:92])
		dramaLines.append(lines[92:102])
		dramaLines.append(lines[102:122])
		dramaLines.append(lines[122:146])
		dramaLines.append(lines[146:166])
		dramaLines.append(lines[166:194])
		dramaLines.append(lines[194:200])
		#"""
		dramaLines.append(lines)
		averageNumbersAndPercents = []
		for unit in dramaLines:
			averageNumbersAndPercents.append(self.getAveragedPercents(unit))
		return averageNumbersAndPercents

	def getAvgPercentsForLengths(self, path):
		data = open(path)
		lines = data.readlines()
		dramaLines = []
		dramaLines.append(lines[0:101])
		dramaLines.append(lines[101:200])
		dramaLines.append(lines[0:61])
		dramaLines.append(lines[61:200])

		averageNumbersAndPercents = []
		for unit in dramaLines:
			averageNumbersAndPercents.append(self.getAveragedPercents(unit))
		return averageNumbersAndPercents

	def getAveragedPercents(self, lines):
		numberOfRaters = 5
		raterRatings = []
		i = 0
		while(i < numberOfRaters):
			raterRating = []
			for line in lines:
				numbers = line.split("\t")
				numbers = [int(number.strip()) for number in numbers]
				raterRating.append(numbers[i])
			i += 1
			#print raterRating
			raterRatings.append(raterRating)
		#print self.compareListsAndReturnPercent(raterRatings[0], raterRatings[1])
		comparisons = []
		comparisons.append(self.compareListsAndReturnPercent(raterRatings[0], raterRatings[1]))
		comparisons.append(self.compareListsAndReturnPercent(raterRatings[0], raterRatings[2]))
		comparisons.append(self.compareListsAndReturnPercent(raterRatings[0], raterRatings[3]))
		comparisons.append(self.compareListsAndReturnPercent(raterRatings[0], raterRatings[4]))

		comparisons.append(self.compareListsAndReturnPercent(raterRatings[1], raterRatings[2]))
		comparisons.append(self.compareListsAndReturnPercent(raterRatings[1], raterRatings[3]))
		comparisons.append(self.compareListsAndReturnPercent(raterRatings[1], raterRatings[4]))

		comparisons.append(self.compareListsAndReturnPercent(raterRatings[2], raterRatings[3]))
		comparisons.append(self.compareListsAndReturnPercent(raterRatings[2], raterRatings[4]))

		comparisons.append(self.compareListsAndReturnPercent(raterRatings[3], raterRatings[4]))
		comparisonsPercent = []
		comparisonsTotalNumber = []
		for compare in comparisons:
			comparisonsTotalNumber.append(compare[0])
			comparisonsPercent.append(compare[1])
		
		totalAvg = float(sum(comparisonsTotalNumber))/float(len(comparisonsTotalNumber))
		totalAvgPercent = float(sum(comparisonsPercent))/float(len(comparisonsPercent))
		#print str(totalAvg).replace(".", ",")
		return (str(totalAvg).replace(".", ","), str(totalAvgPercent).replace(".", ","))


	def compareListsAndReturnPercent(self, list1, list2):
		i = 0
		length = len(list1)
		same = 0
		while(i < length):
			if(list1[i] == list2[i]):
				same += 1
			i += 1
		return (same, float(same)/float(length))


if __name__ == "__main__":
    main()