#coding: utf8

import os
import re
import collections
import locale
import sys
import random
import pickle
from drama_parser import *
from sa_pre_processing import *
from statistic_functions import *
from sentiment_analysis import *

def main():
	reload(sys)
	sys.setdefaultencoding('utf8')

	
	tcc = Test_Corpus_Creator()

	"""
	tcc.createNewTestCorpus()
	tcc.createTxtOutputForTestCorpus("../Evaluation/Test-Korpus/test-corpus7.txt")
	tcc.saveTestCorpusAsPickle("../Evaluation/Test-Korpus/test-corpus7.p")
	
	"""
	tch = Test_Corpus_Handler()
	tch.readAndInitTestCorpusFromPickle("../Evaluation/Test-Korpus/switch-test-corpus-6.p")
	tch.writeInfoPerLine()
	#tcr.calcTestCorpusMetrics()
	#tcc.switchSpecificSpeechesOfTestCorpusByDramaNumber(10, tcr._testCorpusSpeeches)
	#tcc.createTxtOutputForTestCorpus("../Evaluation/Test-Korpus/switch-test-corpus-6.txt")
	#tcc.saveTestCorpusAsPickle("../Evaluation/Test-Korpus/switch-test-corpus-6.p")
	#tcc._testCorpusSpeeches = tcr._testCorpusSpeeches
	#tcc.createTxtOutputForTestCorpus("../Evaluation/Test-Korpus/switch-test-corpus-6-test.txt")

	#tcr.attachLanguageInfoToTestCorpus()
	#tcr.saveTestCorpusAsPickle("../Evaluation/Test-Korpus/test-corpus6-with-Language-Info.p")

	"""
	sa = Sentiment_Analyzer(False)
	for corpusSpeech in tcr._testCorpusSpeeches:
		corpusSpeech._speech._sentimentBearingWords = sa.getSentimentBearingWordsSpeech(corpusSpeech._speech._textAsLanguageInfo)
		sa.attachSentimentMetricsToUnit(corpusSpeech._speech)
		corpusSpeech._speech._sentimentMetrics.printAllInfo(corpusSpeech._speech._lengthInWords)
		for word in corpusSpeech._speech._sentimentBearingWords:
			word.printAllInformation()
	"""

	#tcr.calcTestCorpusMetrics()
	#tcr.writeLengths("../Evaluation/Test-Korpus/test-corpus7-lengths.txt")
	#tcc._testCorpusSpeeches = tcr._testCorpusSpeeches
	#tcc.createTxtOutputForTestCorpus("../Evaluation/Test-Korpus/test-corpus2.txt")


class Test_Corpus_Handler:
	def __init__(self):
		self._testCorpusSpeeches = []

		self._average = -1
		self._median = -1
		self._max = -1
		self._min = -1

	def attachLanguageInfoToTestCorpus(self):
		languageProcessor = Language_Processor()
		for corpusSpeech in self._testCorpusSpeeches:
			languageProcessor.processText(corpusSpeech._speech._text)
			lemmaInformation = languageProcessor._lemmasWithLanguageInfo
			corpusSpeech._speech._textAsLanguageInfo = lemmaInformation

	def readAndInitTestCorpusFromPickle(self,path):
		self._testCorpusSpeeches = pickle.load(open(path, "rb"))

	def writeInfoPerLine(self):
		outputFile = open("../Evaluation/Test-Korpus/test-corpus-infoLines", "w")
		for corpusSpeech in self._testCorpusSpeeches:
			info = [corpusSpeech._id, corpusSpeech._dramaTitle,\
			corpusSpeech._actNumber, corpusSpeech._confNumber,\
			corpusSpeech._speech._numberInAct, corpusSpeech._speech._numberInConf,\
			corpusSpeech._speech._subsequentNumber,corpusSpeech._speech._speaker,\
			corpusSpeech._speech._lengthInWords]
			infoString = ("\t").join(str(x) for x in info)
			outputFile.write(infoString + "\n")
		outputFile.close()

	def writeLengths(self, path):
		wordLengths = []
		for corpusSpeech in self._testCorpusSpeeches:
			wordLengths.append(corpusSpeech._speech._lengthInWords)
		outputFile = open(path, "w")
		wordLengths.sort()
		for length in wordLengths:
			outputFile.write(str(length) + "\n")
		outputFile.close()

	def saveTestCorpusAsPickle(self, path):
		pickle.dump(self._testCorpusSpeeches, open(path, "wb" ))
	
	def calcTestCorpusMetrics(self):
		wordLengths = []
		for corpusSpeech in self._testCorpusSpeeches:
			wordLengths.append(corpusSpeech._speech._lengthInWords)
		self._average = average(wordLengths)
		self._median = median(wordLengths)
		self._min = custom_min(wordLengths)
		self._max = custom_max(wordLengths)

		print(self._average)
		print(self._median)
		print(self._min)
		print(self._max)

class Test_Corpus_Creator:

	def __init__(self):
		self._testCorpusSpeeches = []
		
		self._speechesCorpus = []
		self._speechesCorpusPerDrama = []
		self._filteredSpeechesCorpus = []
		self._filteredSpeechesCorpusPerDrama = []
		self._partsPerDrama = [3, 10, 14, 7, 6, 6, 5, 10, 12, 10, 14, 3]
		self._testCorpusSizeFactor = 2

	def createNewTestCorpus(self):
		self.initSpeechesCorpus()
		self.setTestCorpus()
		print(len(self._speechesCorpus))
		#self.shuffleTestCorpus()
		self.setIdsAndPositionInfoOfTestCorpus()

	def saveTestCorpusAsPickle(self, path):
		pickle.dump(self._testCorpusSpeeches, open(path, "wb" ))
	
	def createTxtOutputForTestCorpus(self, path):
		outputFile = open(path, "w")
		text = ""
		i = 0
		for corpusSpeech in self._testCorpusSpeeches:
			text = text + self.generateSpeechText(corpusSpeech)
			text = text + "--------------------\n"
			if(i == 99):
				text = text + "###\n"
			i = i + 1
		outputFile.write(text)
		outputFile.close()

	def shuffleTestCorpus(self):
		random.shuffle(self._testCorpusSpeeches)
	
	def setIdsAndPositionInfoOfTestCorpus(self):
		i = 1
		for corpusSpeech in self._testCorpusSpeeches:
			corpusSpeech._id = i
			i = i + 1
			corpusSpeech.setPositionInfo()

	def generateSpeechText(self, testCorpusSpeech):
		text = testCorpusSpeech._dramaTitle + " " + testCorpusSpeech._positionInfo + "\n"
		previousSpeech = testCorpusSpeech._previousSpeech._speaker + ":\n" + testCorpusSpeech._previousSpeech._text.strip() + "\n"
		currentSpeech = testCorpusSpeech._speech._speaker + ":\n" + testCorpusSpeech._speech._text.strip() + "\n"
		nextSpeech = testCorpusSpeech._nextSpeech._speaker + ":\n" + testCorpusSpeech._nextSpeech._text.strip() + "\n"
		text = text + previousSpeech + currentSpeech + nextSpeech
		return text

	def switchSpecificSpeechesOfTestCorpusByDramaNumber(self, dramaNumber, testCorpusSpeeches):
		self.initSpeechesCorpus()
		self._testCorpusSpeeches = testCorpusSpeeches

		start = self.getStartAndEndSpeechByDramaNumber(dramaNumber)[0]
		end = self.getStartAndEndSpeechByDramaNumber(dramaNumber)[1]
		speechesPerDrama = self._filteredSpeechesCorpusPerDrama[dramaNumber]
		alreadyChosenNumbers = []
		print start
		print end

		while (start < end):
			randomNumber = random.randint(0, len(speechesPerDrama[1])-1)
			while (randomNumber in alreadyChosenNumbers):
				randomNumber = random.randint(0, len(speechesPerDrama[1])-1)
			alreadyChosenNumbers.append(randomNumber)
			testCorpusSpeech = speechesPerDrama[1][randomNumber]
			self._testCorpusSpeeches[start] = testCorpusSpeech
			print testCorpusSpeech._speech._text
			start = start + 1
		self.setIdsAndPositionInfoOfTestCorpus()

	def getStartAndEndSpeechByDramaNumber(self, dramaNumber):
		i = 0
		start = 0
		end = 0
		print ("DramaNumber")
		print dramaNumber
		while(i < dramaNumber):
			dramaSpeeches = self._partsPerDrama[i] * self._testCorpusSizeFactor
			start = start + dramaSpeeches

			i = i + 1	
		endDrama = self._partsPerDrama[dramaNumber] * self._testCorpusSizeFactor
		end = start + endDrama
		return (start, end)

	def setTestCorpus(self):
		dramaInPartsPerDrama = 0
		for speechesPerDrama in self._filteredSpeechesCorpusPerDrama:
			numberOfSpeeches = self._partsPerDrama[dramaInPartsPerDrama] * self._testCorpusSizeFactor
			dramaInPartsPerDrama = dramaInPartsPerDrama + 1
			i = 0
			alreadyChosenNumbers = []
			while (i < numberOfSpeeches):
				i = i + 1
				randomNumber = random.randint(0, len(speechesPerDrama[1])-1)
				while (randomNumber in alreadyChosenNumbers):
					randomNumber = random.randint(0, len(speechesPerDrama[1])-1)
				alreadyChosenNumbers.append(randomNumber)
				testCorpusSpeech = speechesPerDrama[1][randomNumber]
				self._testCorpusSpeeches.append(testCorpusSpeech)

	def getRandomSpeeches(self):
		randomNumber = random.randint(0, (len(self._filteredSpeechesCorpus)-1))
		testCorpusSpeech = self._filteredSpeechesCorpus[randomNumber]
		text = self.generateSpeechText(testCorpusSpeech)
		print text

	def printInfoOfTestCorpus(self):
		print(len(self._testCorpusSpeeches))
		for corpusSpeech in self._testCorpusSpeeches:
			text = self.generateSpeechText(corpusSpeech)
			print text

	def printInfoOfSingleDramas(self):	
		for speechesPerDrama in self._speechesCorpusPerDrama:
			print speechesPerDrama[0]
			print len(speechesPerDrama[1])
			print (float(float(len(speechesPerDrama[1]))/8171)*100)
			print ((float(float(len(speechesPerDrama[1]))/8171)*100))

	def getAverageSpeechLengthOfCorpus(self):
		lengths = []
		for corpusSpeech in self._speechesCorpus:
			lengths.append(corpusSpeech._speech._lengthInWords)
		average = (float(sum(lengths)))/(float(len(lengths)))
		return average
	
	def printInfoOfFilteredSingleDramas(self):
		print(len(self._filteredSpeechesCorpus))
		for speechesPerDrama in self._filteredSpeechesCorpusPerDrama:
			print speechesPerDrama[0]
			print len(speechesPerDrama[1])
			allSpeeches = float(len(self._filteredSpeechesCorpus))
			allSpeechesPerDrama = float(len(speechesPerDrama[1]))
			print (allSpeechesPerDrama/allSpeeches)*100

	def initSpeechesCorpus(self):
		dramas = []
		path = "../Lessing-Dramen/"	

		for filename in os.listdir(path):		
			dpp = Drama_Pre_Processing()
			dramaModel = dpp.preProcess(path + filename)
			dramaTitle = dramaModel._title
			print(path+filename)
			speechesPerDrama = []
			filteredSpeechesPerDrama = []

			for act in  dramaModel._acts:
				actNumber = act._number
				for conf in act._configurations:
					confNumber = conf._number
					confLength = len(conf._speeches)
					i = 0
					while (i < confLength):
						previousSpeech = None
						nextSpeech = None
						if((i-1) >= 0):
							previousSpeech = conf._speeches[i-1]

						currentSpeech = conf._speeches[i]
						speechLength = conf._speeches[i]._lengthInWords
						
						if((i+1) < confLength):
							nextSpeech = conf._speeches[i+1]

						tcSpeech = Test_Corpus_Speech(currentSpeech, previousSpeech, nextSpeech, dramaTitle, actNumber, confNumber, i+1)
						self._speechesCorpus.append(tcSpeech)
						"""
						print("Speech")
						print(tcSpeech._previousSpeech)
						print(tcSpeech._speech)
						print(tcSpeech._nextSpeech)
						print(tcSpeech._actNumber)
						print(tcSpeech._confNumber)
						print(tcSpeech._speechNumberInConf)
						"""

						speechesPerDrama.append(tcSpeech)
						if(previousSpeech is not None and nextSpeech is not None and speechLength > 18):
							self._filteredSpeechesCorpus.append(tcSpeech)
							filteredSpeechesPerDrama.append(tcSpeech)
						i = i + 1
			titleSpeechesTuple = (dramaTitle, speechesPerDrama)
			self._speechesCorpusPerDrama.append(titleSpeechesTuple)
			titleFilteredSpeechesTuple = (dramaTitle, filteredSpeechesPerDrama)
			self._filteredSpeechesCorpusPerDrama.append(titleFilteredSpeechesTuple)



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