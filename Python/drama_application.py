#coding: utf8

import os
from drama_parser import *
from drama_output import *

def main():
    debug = True

    #to generate one json-file
    """
    parser = DramaParser()
    dramaModel = parser.parse_xml("../Korpus/weis_masaniello_t.xml")
    drama_data = parser.generateDramaData(dramaModel)
    parser.writeJSON(drama_data)
    """

    #to generate a json-file of all dramas
    parser = DramaParser()
    output = DramaOutput()
    dramas = []
    dramasForDenormalizing = []

    if debug:

        for filename in os.listdir("../Korpus"):
            dramaModel = parser.parse_xml("../Korpus/" + filename)
            data = output.generateDramaData(dramaModel)
            dramas.append(data)
            dramasForDenormalizing.append(dramaModel)
            print("Erfolg beim Parsen eines Dramas")

    else:
        for filename in os.listdir("../Korpus"):
            try:
                dramaModel = parser.parse_xml("../Korpus/" + filename)
                data = output.generateDramaData(dramaModel)
                dramas.append(data)
                dramasForDenormalizing.append(dramaModel)
                print("Erfolg beim Parsen eines Dramas")
            except:
                print("Fehler beim Parsen eines Dramas")
                print("!!! " + filename)

    """
    print(len(dramas))
    dramas_json = json.dumps(dramas, indent=4, ensure_ascii=True) 
    doc = open('Dramas_data.json', 'w')
    doc.write(dramas_json)
    doc.close
    """

    output.generateDenormalizedJSON(dramasForDenormalizing)


if __name__ == "__main__":
    main()