#coding: utf8

import os
import re
import collections
import locale
import sys
from sa_models import *
import pprint
import treetaggerwrapper

def main():
	reload(sys)
	sys.setdefaultencoding('utf8')

	tagger = treetaggerwrapper.TreeTagger(TAGLANG='de')
	tags = tagger.tag_text(unicode("Das ist ein schöner Tag. Das ist ein großer, aber schwerer Erfolg"))
	pprint.pprint(tags)


if __name__ == "__main__":
    main()