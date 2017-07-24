#coding: utf8

import os
import re
import collections
import locale
import sys
from language_processor import *

def main():
	reload(sys)
	sys.setdefaultencoding('utf8')

	dlOutput = DramaLanguage_Output()
	#dlOutput.processEntireCorpusAndGenereateOutputLemmas("../Lessing-Dramen/", "../Word-Frequencies/Lemmas/EntireCorpus")

	#dlOutput.generateWordFrequenciesOutputTokens("../Lessing-Dramen/less-Der_Freigeist_k.xml", "../Word-Frequencies/test")
	dlOutput.processMultipleDramasAndGenerateOutputTokens("../Lessing-Dramen/", "../Word-Frequencies/Tokens_ohneKursiv/")

class DramaLanguage_Output:

	def __init__(self):
		self._lp = None

		self.setLanguageProcessor()

	def setLanguageProcessor(self):
		self._lp = Language_Processor()

	def generateWordFrequenciesOutputTokens(self, inputPath, outputPath):
		self._lp.processSingleDramaTokens(inputPath)
		self._lp.removeStopwordsFromTokens()
		wordFrequencies = self.calcWordFrequencies(self._lp._tokensWithoutStopwords)

		outputFile = open(outputPath + ".txt", "w")
		self.writeOutputTokens(outputFile, wordFrequencies)
		
		outputFile.close()
		print("Output ready...")

	def writeOutputTokens(self, outputFile, wordFrequencies):
		outputFile.write("Title: " + self._lp._currentDramaName + "\n")
		outputFile.write("Number of all tokens: " + str(len(self._lp._tokensWithoutStopwords)) + "\n")
		outputFile.write("Nummber of different tokens: " + str(len(wordFrequencies)) + "\n\n")

		outputFile.write("Token" +"\t" + "Frequency" + "\n")
		for frequ in wordFrequencies:
			token = frequ[0]
			outputFile.write(token + "\t" + str(frequ[1]) + "\n")
		return outputFile

	def generateWordFrequenciesOutputLemmas(self, inputPath, outputPath):
		self._lp.processSingleDrama(inputPath)
		outputFile = open(outputPath + ".txt", "w")
		wordFrequencies = self.calcWordFrequencies(self._lp._lemmasWithoutStopwords)
		self.writeOutputLemmas(outputFile, wordFrequencies)
		outputFile.close()
		print("Output ready...")

	def writeOutputLemmas(self, outputFile, wordFrequencies):
		outputFile.write("Title: " + self._lp._currentDramaName + "\n") 
		outputFile.write("Number of all lemmas: " + str(len(self._lp._lemmasWithoutStopwords)) + "\n")
		outputFile.write("Nummber of different lemmas: " + str(len(wordFrequencies)) + "\n\n")

		outputFile.write("Lemma" + "\t" + "POS" + "\t" + "Frequency" + "\t" + "Tokens" +"\n")
		for frequ in wordFrequencies:
			lemma = frequ[0]
			POS = self._lp._lemmasAndPOSAndTokensDict[lemma][0]
			tokens = self._lp._lemmasAndPOSAndTokensDict[lemma][1]
			outputFile.write(str(lemma) + "\t" + ', '.join(POS) + "\t" + str(frequ[1]) + "\t" + ', '.join(tokens) + "\n")
		return outputFile

	def processMultipleDramasAndGenerateOutputTokens(self, originpath, resultpath):
		parser = DramaParser()

		for filename in os.listdir(originpath):
			print(filename + " processing starts...")
			dramaModel = parser.parse_xml(originpath + filename)
			print("DramaModel ready...")
			title = dramaModel._title
			self.generateWordFrequenciesOutputTokens(originpath + filename, resultpath + title)

	def processMultipleDramasAndGenerateOutputLemmas(self, originpath, resultpath):
		parser = DramaParser()

		for filename in os.listdir(originpath):
			print(filename + " processing starts...")
			dramaModel = parser.parse_xml(originpath + filename)
			print("DramaModel ready...")
			title = dramaModel._title
			self.generateWordFrequenciesOutputLemmas(originpath + filename, resultpath + title)

	def processEntireCorpusAndGenereateOutputTokens(self, originpath, outputPath):
		totalText = self.getEntireCorpus(originpath)
		self._lp.processTextTokens(totalText)
		self._lp.removeStopwordsFromTokens()
		self._lp._currentDramaName = "EntireCorpus"

		wordFrequencies = self.calcWordFrequencies(self._lp._tokensWithoutStopwords)

		outputFile = open(outputPath + ".txt", "w")
		self.writeOutputTokens(outputFile, wordFrequencies)
		
		outputFile.close()
		print("Output ready...")

	def processEntireCorpusAndGenereateOutputLemmas(self, originpath, outputPath):
		totalText = self.getEntireCorpus(originpath)
		self._lp.processTextFully(totalText)

		self._lp._currentDramaName = "EntireCorpus"

		wordFrequencies = self.calcWordFrequencies(self._lp._lemmasWithoutStopwords)

		outputFile = open(outputPath + ".txt", "w")
		self.writeOutputLemmas(outputFile, wordFrequencies)
		
		outputFile.close()
		print("Output ready...")

	def getEntireCorpus(self, originpath):
		parser = DramaParser()
		totalText = "";
		for filename in os.listdir(originpath):
			print(filename + " processing starts...")
			dramaModel = parser.parse_xml(originpath + filename)
			
			for act in dramaModel._acts:
				for conf in act._configurations:
					for speech in conf._speeches:
						newText = unicode(speech._text.replace("–", ""))
						totalText = totalText + newText
		return totalText

	def calcWordFrequencies(self, wordList):
		fdist = FreqDist(wordList)
		frequencies = fdist.most_common()
		return frequencies

if __name__ == "__main__":
    main()