#coding: utf8

import xml.etree.ElementTree as ET
import re
import os
import nltk
from drama_models import *

class DramaParser:

    namespaces = {"tei":'http://www.tei-c.org/ns/1.0'} # used to read the tags in the xml correctly

    # starting point for the parsing
    def parse_xml(self, filepath):
        drama_model = DramaModel()
        xml_root = self.get_xml_root(filepath) # get xml treeroot

        # general information
        
        drama_model._title = self.get_title(xml_root)
        drama_model._author = self.get_author(xml_root)
        drama_model._date = self.get_date(xml_root)
        drama_model._year = drama_model._date

        drama_model._type = self.get_type(filepath)

        drama_model._subact_type = "Szene"
        
        drama_model._acts = self.extract_act_data(xml_root)

        drama_model._speakers = self.get_all_speakers(drama_model._acts)

        drama_model._castgroup = self.get_cast_group(drama_model._speakers)


        self.calc_statistics(drama_model)

        return drama_model

    def get_cast_group(self, speakerModels):
        names = []
        for speaker in speakerModels:
            names.append(speaker._name)
        return names


    # calculates statistics for the whole drama
    def calc_statistics(self, drama_model):
        drama_model.calc_config_density()
        drama_model.calc_config_matrix()
        drama_model.calc_speaker_relations()

        # speech statistics
        drama_model.calc_speeches_statistics()

        for act in drama_model._acts:
            act.calc_speeches_statistics()

            for configuration in act._configurations:
                configuration.calc_speeches_statistics()
                normal = 0
                for speech in configuration._speeches:
                    normal = normal + speech._length
                 

        drama_model.add_speeches_to_speakers()
        for speaker in drama_model._speakers:
            speaker.calc_speeches_statistics()

        drama_model.set_speaker_count()

    # returns the xml root for the file
    def get_xml_root(self, filepath):
        tree = ET.parse(filepath)
        return tree.getroot()

    # returns the drama title
    def get_title(self, xml_root):
        title = xml_root.find("tei:teiHeader/tei:fileDesc/tei:titleStmt/tei:title", self.namespaces).text
        return title

    # returns the drama author
    def get_author(self, xml_root):
        author = xml_root.find("tei:teiHeader/tei:fileDesc/tei:titleStmt/tei:author", self.namespaces).text
        return author

    # returns the drama date
    def get_date(self, xml_root):
        sourceDesc = xml_root.find("tei:teiHeader/tei:fileDesc/tei:sourceDesc", self.namespaces)
        bibl = sourceDesc.find("tei:bibl/tei:bibl", self.namespaces)
        date_premiere = bibl.find("tei:date[@type='premiere']", self.namespaces)
        date_print = bibl.find("tei:date[@type='print']", self.namespaces)
        date_written = bibl.find("tei:date[@type='written']", self.namespaces)
        if "when" in date_print.attrib:
            dateText = date_print.attrib["when"]
        elif "when" in date_premiere.attrib:
            dateText = date_premiere.attrib["when"]
        elif "when" in date_written.attrib:
            dateText = date_written.attrib["when"]
        else:
            dateText = "0"

        date = dateText
        return date

    # returns the drama type from the filename
    def get_type(self, filepath):
        filepath = filepath.lower()
        if filepath.find("_s.xml") != -1 or filepath.find("_.s.xml") != -1:
            return "Schauspiel"
        elif filepath.find("_t.xml") != -1 or filepath.find("_.t.xml") != -1 or filepath.find("_t4.xml") != -1:
            return "Trauerspiel"
        elif filepath.find("_k.xml") != -1 or filepath.find("_.k.xml") != -1:
            return "Komoedie"
        return "unknown"

    # every speaker, even if they are double with different names
    def get_all_speakers(self, acts):
        speaker_list = []
        for act in acts:
            for speaker in act._appearing_speakers:
                if speaker not in speaker_list:
                    speaker_list.append(speaker)

        speaker_model_list = []

        for speaker in speaker_list:
            speaker_model = SpeakerModel()
            speaker_model._name = speaker
            speaker_model_list.append(speaker_model)
        return speaker_model_list

    # returns informations about all acts of the drama
    def extract_act_data(self, xml_root):
        act_data = []
        position = 1
        # gets number of acts and corresponding count of scenes
        numberOfActs = len(xml_root.findall(".//tei:div[@type='act']", self.namespaces))

        if(numberOfActs > 0):
            for act in xml_root.findall(".//tei:div[@type='act']", self.namespaces):

                act_model = ActModel()
                act_model._number = position
                act_model._configurations = self.extract_subact_data(act, position)

                act_model.set_appearing_speakers()
                act_data.append(act_model)
                position += 1
        else:
            act = xml_root.find(".//tei:body", self.namespaces)
            act_model = ActModel()
            act_model._number = position
            act_model._configurations = self.extract_subact_data(act, position)

            act_model.set_appearing_speakers()
            act_data.append(act_model)

        return act_data

    # returns informations about all subacts of the drama
    def extract_subact_data(self, act, position):
        config_data = []
        subact_position = 1
        numberOfScenes = len(act.findall(".//tei:div[@type='scene']", self.namespaces))

        if (numberOfScenes > 0):
            for subact in act.findall(".//tei:div[@type='scene']", self.namespaces):
                config_model = ConfigurationModel()
                config_model._number = subact_position
                config_model._name = str(position) + " - " + str(subact_position)
                config_model._speeches = self.get_speeches_for_subact(subact)
                
                config_model._appearing_speakers = self.get_speakers_for_subact(config_model._speeches)

                config_data.append(config_model)
                subact_position += 1
        else:
            subact = act
            config_model = ConfigurationModel()
            config_model._number = subact_position
            config_model._name = str(position) + " - " + str(subact_position)
            config_model._speeches = self.get_speeches_for_subact(subact)
                
            config_model._appearing_speakers = self.get_speakers_for_subact(config_model._speeches)

            config_data.append(config_model)
            subact_position += 1

        return config_data

    # returns speech for subact
    def get_speeches_for_subact(self, subact):
        speech_data = []

        for subact_speaker_wrapper in subact.findall(".//tei:sp", self.namespaces):
            speech_model = SpeechModel()
            name = subact_speaker_wrapper.attrib["who"]
            name = name.replace("#", "")

            speech_model._speaker = name

            speech_model._text = self.get_speech_text(subact_speaker_wrapper)

            tokens = nltk.word_tokenize(speech_model._text)
            tokens = [w for w in tokens if w.isalpha()]

            speech_model._length = len(tokens)

            # speech with a length of zero or less are not added
            if(speech_model._length > 0):
                speech_data.append(speech_model)

        return speech_data

    def get_stage_text(self, sub_sp_wrapper):
        print ("no Idea")

    # calculates length of speech
    def get_speech_text(self, sub_sp_wrapper):
        speechText = ""
        
        speechText = ""
        children = sub_sp_wrapper.getchildren()
        

        for element in children:
            if (element.tag == "{http://www.tei-c.org/ns/1.0}l"):
                for text in element.itertext():
                    if (text[0] == " " or speechText.endswith(" ")):
                        speechText = speechText + text
                    else:
                        speechText = speechText + " " + text
            if (element.tag == "{http://www.tei-c.org/ns/1.0}lg"):
                for l_element in element.findall("./tei:l", self.namespaces):
                    for text in l_element.itertext():
                        if (text[0] == " " or speechText.endswith(" ")):
                            speechText = speechText + text
                        else:
                            speechText = speechText + " " + text
            if (element.tag == "{http://www.tei-c.org/ns/1.0}p"):
                for text in element.itertext():
                    if(text.startswith("Ende de")):
                        speechText = speechText
                    else:
                        if (text[0] == " " or speechText.endswith(" ")):
                            speechText = speechText + text
                        else:
                            speechText = speechText + " " + text
            
        ### Ohne Szenenanweisungen
        """
        for element in children:
            if (element.tag == "{http://www.tei-c.org/ns/1.0}l"):
                text = element.text
                if (text[0] == " " or speechText.endswith(" ")):
                    speechText = speechText + text
                else:
                    speechText = speechText + " " + text
            if (element.tag == "{http://www.tei-c.org/ns/1.0}lg"):
                for l_element in element.findall("./tei:l", self.namespaces):
                    text = element.text
                    if (text[0] == " " or speechText.endswith(" ")):
                        speechText = speechText + text
                    else:
                        speechText = speechText + " " + text
            if (element.tag == "{http://www.tei-c.org/ns/1.0}p"):
                text = element.text
                if(text.startswith("Ende de")):
                    speechText = speechText
                else:
                    if (text[0] == " " or speechText.endswith(" ")):
                        speechText = speechText + text
                    else:
                        speechText = speechText + " " + text
            """

        return speechText

    # returns all speakers for the subact
    def get_speakers_for_subact(self, speech_list):
        speaker_data = []

        for speech in speech_list:
            speaker = speech._speaker
            if speaker not in speaker_data:
                speaker_data.append(speaker)

        return speaker_data

#mistakes = 0

"""
parser = DramaParser()
model = parser.parse_xml("GerDracor/tei_with_annotations/wilbrandt-gracchus-der-volkstribun.xml")
print model._type
"""


"""
for files in os.listdir("GerDracor/tei"):
    path = "GerDracor/tei/" + files
    
    try:
        parser = DramaParser()
        parser.parse_xml(path)
        print path
    except:
        mistakes = mistakes + 1
        print "ERROR " + path

print mistakes
"""
