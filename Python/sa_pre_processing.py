import os
import re
import collections
import locale
import sys
from drama_parser import *
from language_processor import *

def main():
	reload(sys)
	sys.setdefaultencoding('utf8')

class Drama_Pre_Processing:

	def __init__(self, dramaPath):
		self._dramaModel = None
		self._languageProcessor = None

		self.initDramaModel(dramaPath)
		self.initLanguageProcessor()


	def initDramaModel(self, dramaPath):
		parser = DramaParser()
		self._dramaModel = parser.parse_xml(dramaPath)

	def initLanguageProcessor(self):
		self._languageProcessor = Language_Processor()

	def preProcess(self):
		self.attachPositionsToSpeechesAndConfs()
		self.attachPreOccuringSpeakersToSpeeches()
		self.attachLengthInWordsToStructuralElements()
		return self._dramaModel

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