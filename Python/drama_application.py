#coding: utf8

import os
from drama_parser import *
from drama_output import *

def main():
    debug = True

    # used to generate one JSON file
    """
    parser = DramaParser()
    dramaModel = parser.parse_xml("../Korpus/weis_masaniello_t.xml")
    drama_data = parser.generate_drama_data(dramaModel)
    parser.write_JSON(drama_data)
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
            """
            dramaModel = parser.parse_xml("../Korpus/" + filename)
            dramas.append(dramaModel)
            print("Erfolg beim Parsen eines Dramas")
            """

    else:
        for filename in os.listdir("../Korpus"):
            try:
                dramaModel = parser.parse_xml("../Korpus/" + filename)
                data = output.generate_drama_data(dramaModel)
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
    output.generate_denormalized_JSON(dramasForDenormalizing)
    """
    output.generates_normalized_JSON(dramas)
    """


if __name__ == "__main__":
    main()