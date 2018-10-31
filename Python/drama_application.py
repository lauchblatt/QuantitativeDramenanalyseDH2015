#coding: utf8

import os
from drama_parser import *
from drama_output import *
import sys
import codecs
import nltk

def main():
    
    reload(sys)
    sys.setdefaultencoding('utf8')

    debug = True

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
    
    """
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