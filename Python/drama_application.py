#coding: utf8

import os
from drama_parser import *
from drama_output import *
import sys
import codecs
import nltk
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag

def main():
    
    reload(sys)
    sys.setdefaultencoding('utf8')

    debug = True
    text = ("I saw the dog carrying some sausages.")
    
    tokens = word_tokenize(text)
    lemmatizer = WordNetLemmatizer()
    print tokens
    lemmas = []
    lemmas.append(lemmatizer.lemmatize("I", pos="n"))
    lemmas.append(lemmatizer.lemmatize("saw", pos="v"))
    lemmas.append(lemmatizer.lemmatize("the", pos="n"))
    lemmas.append(lemmatizer.lemmatize("dog", pos="n"))
    lemmas.append(lemmatizer.lemmatize("carrying", pos="v"))
    lemmas.append(lemmatizer.lemmatize("some", pos="a"))
    lemmas.append(lemmatizer.lemmatize("sausages", pos="n"))
    
    print lemmas

    #tags = pos_tag(tokens)
    #print tags
    #pos = []
    #for token in tokens:
       # posTag = pos_tag(token)
        #print posTag
    #print (" ".join(lemmas))
    """
    stems = []
    porter_stemmer = PorterStemmer()
    for token in tokens:
        stem = porter_stemmer.stem(token)
        stems.append(stem)
    print(" ".join(stems))
    """
    """
    for filename in os.listdir("Korpus"):
        parser = DramaParser()
        dramaModel = parser.parse_xml("Korpus/" + filename)
        #print filename
        numberOfAllSpeaker = float(len(dramaModel._speakers))
        acts = dramaModel._acts
        lastAct = acts[len(dramaModel._acts)-1]
        confs = lastAct._configurations
        lastConf = confs[len(lastAct._configurations)-1]
        #print len(lastConf._appearing_speakers)
        numberOfFinalSpeakers = float(len(lastConf._appearing_speakers))
        proportion = numberOfFinalSpeakers/numberOfAllSpeaker
        line = [dramaModel._title, dramaModel._author, dramaModel._type]
        line.append(str(len(dramaModel._speakers)))
        line.append(str(int(numberOfFinalSpeakers)))
        line.append(str(proportion).replace(".", ","))
        printLine = "\t".join(line)
        print printLine
        #print proportion
        #if (proportion == 1.0):
            #print dramaModel._title + " von " + dramaModel._author
            #print "true"
        #else:
           # print "false"
    # used to generate one JSON file
    
    parser = DramaParser()
    dramaModel = parser.parse_xml("../Lessing-Dramen/-Der_junge_Gelehrte.xml")
    output = DramaOutput()
    drama_data = output.generate_drama_data(dramaModel)
    output.write_JSON(drama_data)
    """

    """
    # used to generate a JSON file of all dramas
    parser = DramaParser()
    output = DramaOutput()
    dramas = []
    dramasForDenormalizing = []

    # if debug mode is true, no exception will be catched
    if debug:

        for filename in os.listdir("../Korpus"):
            
            dramaModel = parser.parse_xml("../Korpus/" + filename)
            dramasForDenormalizing.append(dramaModel)
            print("Erfolg beim Parsen eines Dramas")
            
            dramaModel = parser.parse_xml("../Korpus/" + filename)
            dramas.append(dramaModel)
            print("Erfolg beim Parsen eines Dramas")
            

    else:
        for filename in os.listdir("../Korpus"):
            try:
                dramaModel = parser.parse_xml("../Korpus/" + filename)
                dramasForDenormalizing.append(dramaModel)
                print("Erfolg beim Parsen eines Dramas")
            except:
                print("Fehler beim Parsen eines Dramas")
                print("!!! " + filename)


    output.generate_denormalized_JSON(dramasForDenormalizing)
    output.generates_normalized_JSON(dramas)
    """


if __name__ == "__main__":
    main()