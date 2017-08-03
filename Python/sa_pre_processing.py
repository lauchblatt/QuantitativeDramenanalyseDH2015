import os
import re
import collections
import locale
import sys
from drama_parser import *
from language_processor import *
import pickle

def main():
	reload(sys)
	sys.setdefaultencoding('utf8')

	dpp = Drama_Pre_Processing("treetagger")
	#dpp.preProcessLemmatizeAndDump("../Lessing-Dramen/less-Nathan_der_Weise_s.xml")
	dpp.preProcessAndDumpAllDramas()

class Drama_Pre_Processing:

	def __init__(self, processor):
		self._dramaModel = None
		self._languageProcessor = None
		self._processor = processor
		self.initLanguageProcessor(processor)
	
	def preProcessAndDumpAllDramas(self):
		for filename in os.listdir("../Lessing-Dramen/"):
			self.preProcessAndLemmatize("../Lessing-Dramen/" + filename)
			targetPath = "Dumps/ProcessedDramas/" + self._processor + "/" + self._dramaModel._title + ".p"
			self.dumpDramaModel(targetPath)
	
	def initDramaModel(self, dramaPath):
		parser = DramaParser()
		self._dramaModel = parser.parse_xml(dramaPath)
	
	def readDramaModelFromDump(self, dramaPath):
		self._dramaModel = pickle.load(open(dramaPath, "rb"))
		return self._dramaModel

	def preProcessLemmatizeAndDump(self, dramaPath):
		self.preProcessAndLemmatize(dramaPath)

		self.dumpDramaModel("Dumps/ProcessedDramas/" + self._processor + "/" + self._dramaModel._title + ".p")

	def dumpDramaModel(self, dramaPath):
		pickle.dump(self._dramaModel, open(dramaPath, "wb" ))

	def initLanguageProcessor(self, processor):
		lp = Language_Processor(processor)
		self._languageProcessor = lp._processor

	def preProcess(self, path):
		self.initDramaModel(path)
		self.attachPositionsToSpeechesAndConfs()
		self.attachPreOccuringSpeakersToSpeeches()
		self.attachLengthInWordsToStructuralElements()
		return self._dramaModel

	def preProcessAndLemmatize(self, path):
		self.preProcess(path)
		self.attachLanguageInfoToSpeeches()

	def attachLanguageInfoToSpeeches(self):
		for act in self._dramaModel._acts:
			for conf in act._configurations:
				for speech in conf._speeches:
					self._languageProcessor.processText(speech._text)
					lemmaInformation = self._languageProcessor._lemmasWithLanguageInfo
					speech._textAsLanguageInfo = lemmaInformation

	def attachLengthInWordsToStructuralElements(self):
		dramaLength = 0
		for act in self._dramaModel._acts:
			actLength = 0
			for conf in act._configurations:
				confLength = 0
				for speech in conf._speeches:
					self._languageProcessor.processTextTokens(speech._text)
					speech._lengthInWords = len(self._languageProcessor._tokens)
					confLength = confLength + speech._lengthInWords
					actLength = actLength + speech._lengthInWords
					dramaLength = dramaLength + speech._lengthInWords
				conf._lengthInWords = confLength
			act._lengthInWords = actLength
		self._dramaModel._lengthInWords = dramaLength

		for speaker in self._dramaModel._speakers:
			speakerLength = 0
			for speech in speaker._speeches:
				speakerLength = speakerLength + speech._lengthInWords
			speaker._lengthInWords = speakerLength

	def attachPreOccuringSpeakersToSpeeches(self):
		preOccuringSpeaker = ""

		for act in self._dramaModel._acts:
			# Reset every speaker when new act starts
			preOccuringSpeaker = ""
			for conf in act._configurations:
				for speech in conf._speeches:
					speech._preOccuringSpeaker = preOccuringSpeaker
					preOccuringSpeaker = speech._speaker

	def attachPositionsToSpeechesAndConfs(self):
		subsequentNumberSpeech = 1
		subsequentNumberConf = 1

		for act in self._dramaModel._acts:
			numberInAct = 1
			for conf in act._configurations:
				numberInConf = 1
				conf._subsequentNumber = subsequentNumberConf
				subsequentNumberConf = subsequentNumberConf + 1
				for speech in conf._speeches:
					speech._subsequentNumber = subsequentNumberSpeech
					speech._numberInAct = numberInAct
					speech._numberInConf = numberInConf

					subsequentNumberSpeech = subsequentNumberSpeech + 1
					numberInAct = numberInAct + 1
					numberInConf = numberInConf +1

if __name__ == "__main__":
	main()