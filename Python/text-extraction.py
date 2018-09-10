#coding: utf8

import os
import re
import collections
import locale
import sys
import xml.etree.ElementTree as ET

def main():
	reload(sys)
	sys.setdefaultencoding('utf8')
	te = Text_Extraction()
	te.test()


class Text_Extraction:
	
	def __init__(self):
		self._tch = None

	def getRawTextDramas(self):
		for filename in os.listdir("Dramen-Textgrid"):
			try:
				text = open('Dramen-Textgrid/' + filename).read()
				textNoTags = ''.join(ET.fromstring(text).itertext())

				file = open('Dramen-Textgrid_rawInnerText/' + filename[:-3] + "txt", "w")
				file.write(textNoTags)
			except:
				print filename

	def getCleanRawTextDramas(self):



if __name__ == "__main__":
    main()