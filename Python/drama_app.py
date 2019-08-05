import os
import sys
import xml.etree.ElementTree as ET
from drama_parser import *
from drama_output import *


def main():
    
    reload(sys)
    sys.setdefaultencoding('utf8')

    """
    namespaces = {"tei":'http://www.tei-c.org/ns/1.0'}

    korpusTitles = []
    dracorTitles = []

    for file in os.listdir("Korpus/"):
        filepath = "Korpus/" + file
        tree = ET.parse(filepath)
        xml_root = tree.getroot()
        title = xml_root.find("tei:teiHeader/tei:fileDesc/tei:titleStmt/tei:title", namespaces).text
        korpusTitles.append(title)
    counter = 0
    for file in os.listdir("GerDracor/tei/"):
        
        filepath = "GerDracor/tei/" + file
        tree = ET.parse(filepath)
        xml_root = tree.getroot()
        title = xml_root.find("tei:teiHeader/tei:fileDesc/tei:titleStmt/tei:title", namespaces).text
        dracorTitles.append(title)
        
    for title in korpusTitles:
        if title not in dracorTitles:
            print title
    """

    parser = DramaParser()
    output = DramaOutput()
    dramas = []
    dramasForDenormalizing = []

    debug = False

    print "hello world"

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

        for filename in os.listdir("GerDracor/tei_with_annotations/"):
            try:
                dramaModel = parser.parse_xml("GerDracor/tei_with_annotations/" + filename)
                dramasForDenormalizing.append(dramaModel)
                print("Erfolg beim Parsen eines Dramas")
            except:
                print("Fehler beim Parsen eines Dramas")
                print("!!! " + filename)


    output.generate_denormalized_JSON(dramasForDenormalizing)
    #output.generates_normalized_JSON(dramas)



if __name__ == "__main__":
    main()