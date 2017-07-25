#coding: utf8

import os
import re
import collections
import locale
import sys
import random
from drama_parser import *
from sa_pre_processing import *

def main():
	reload(sys)
	sys.setdefaultencoding('utf8')

	tcc = Test_Corpus_Creator()
	tcc.shuffleTestCorpus()
	tcc.createTxtOutputForTestCorpus()

class Test_Corpus_Creator:

	def __init__(self):
		self._testCorpusSpeeches = []
		
		self._speechesCorpus = []
		self._speechesCorpusPerDrama = []
		self._filteredSpeechesCorpus = []
		self._filteredSpeechesCorpusPerDrama = []
		self._partsPerDrama = [3, 10, 14, 7, 6, 6, 6, 10, 11, 10, 14, 3]
		self._testCorpusSizeFactor = 2

		self.initSpeechesCorpus()
		self.setTestCorpus()


	def createTxtOutputForTestCorpus(self):
		outputFile = open("../Evaluation/Test-Korpus.txt", "w")
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
	
	def generateSpeechText(self, testCorpusSpeech):
		text = testCorpusSpeech._dramaTitle + " " + testCorpusSpeech._positionInfo + "\n"
		previousSpeech = testCorpusSpeech._previousSpeech._speaker + ":\n" + testCorpusSpeech._previousSpeech._text.strip() + "\n"
		currentSpeech = testCorpusSpeech._speech._speaker + ":\n" + testCorpusSpeech._speech._text.strip() + "\n"
		nextSpeech = testCorpusSpeech._nextSpeech._speaker + ":\n" + testCorpusSpeech._nextSpeech._text.strip() + "\n"
		text = text + previousSpeech + currentSpeech + nextSpeech
		return text

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
			dpp = Drama_Pre_Processing(path + filename)
			dramaModel = dpp.preProcess()
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

						if(conf._speeches[i-1] is not None):
							previousSpeech = conf._speeches[i-1]
						currentSpeech = conf._speeches[i]
						speechLength = conf._speeches[i]._lengthInWords
						if((i+1) < confLength):
							nextSpeech = conf._speeches[i+1]

						tcSpeech = Test_Corpus_Speech(currentSpeech, previousSpeech, nextSpeech, dramaTitle, actNumber, confNumber, i-1)
						self._speechesCorpus.append(tcSpeech)
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
		self.setPositionInfo()

	def setPositionInfo(self):
		self._positionInfo = str(self._actNumber) + ".Akt, " + str(self._confNumber) + \
		".Szene, " + str(self._speechNumberInConf) + ".Replik" + ", Nummer im Drama: " + str(self._speech._subsequentNumber)


if __name__ == "__main__":
    main()