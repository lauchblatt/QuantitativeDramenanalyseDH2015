#coding: utf8

import os
from drama_parser import *
from drama_output import *

def main():
    debug = True

    # used to generate one JSON file

    parser = DramaParser()
    dramaModel = parser.parse_xml("../Korpus/toer_agnes_t.xml")
    output = DramaOutput()
    drama_data = output.generate_drama_data(dramaModel)
    output.write_JSON(drama_data)

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