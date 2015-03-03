#coding: utf8

import xml.etree.ElementTree as ET
import re
from drama_models import *

class DramaParser:

    namespaces = {'tei':'http://www.tei-c.org/ns/1.0'} # used to read the tags in the xml correctly

    def parse_xml(self, filepath):
        drama_model = DramaModel()
        xml_root = self.get_xml_root(filepath) # get xml treeroot

        # create speaker mapping
        self.speaker_mapping(xml_root)

        # general information
        drama_model._title = self.get_title(xml_root)
        drama_model._author = self.get_author(xml_root)
        drama_model._date = self.get_date(xml_root)
        drama_model._type = self.get_type(filepath)

        drama_model._subact_type = self.get_subact_type(xml_root)
        drama_model._acts = self.extract_act_data(xml_root)
        drama_model._speakers = self.get_all_speakers(xml_root)
        self.get_speakers_from_castgroup(xml_root)

        drama_model.calc_config_density()
        drama_model.calc_speaker_relations()
        drama_model.calc_replicas_statistics()
        print (vars(drama_model))

        for act in drama_model._acts:
            act.calc_replicas_statistics()
            for configuration in act._configurations:
                #print(configuration._name)
                configuration.calc_replicas_statistics()

        drama_model.add_replicas_to_speakers()
        for speaker in drama_model._speakers:
            speaker.calc_replicas_statistics()
            #print (vars(speaker))



    def get_xml_root(self, filepath):
        tree = ET.parse(filepath)
        return tree.getroot()

    def get_title(self, xml_root):
        title = xml_root.find(".//tei:fileDesc/tei:titleStmt/tei:title", self.namespaces).text
        return title

    def get_author(self, xml_root):
        author = xml_root.find(".//tei:sourceDesc/tei:biblFull/tei:titleStmt/tei:author", self.namespaces).text
        return author

    def get_date(self, xml_root):
        date = xml_root.find(".//tei:profileDesc/tei:creation/tei:date", self.namespaces).attrib
        return date

    def get_type(self, filepath):
        if filepath.find("_s.xml") != -1:
            return "Schauspiel"
        elif filepath.find("_t.xml") != -1:
            return "Trauerspiel"
        elif filepath.find("_k.xml") != -1:
            return "Komoedie"

    def get_subact_type(self, xml_root):
        subact_type = xml_root.find(".//tei:div[@type='act']/tei:div[@subtype='work:no']//tei:desc/tei:title", self.namespaces).text
        if subact_type.find("Auftritt") != -1:
            return "Auftritt"
        elif subact_type.find("Szene") != -1:
            return "Szene"

    # every speaker, even if they are double with different names
    def get_all_speakers(self, xml_root, as_objects = True):
        speaker_list = []
        for speaker in xml_root.findall(".//tei:speaker", self.namespaces):
            name = speaker.text
            if name[-1] == ".":
                name = name[:-1]
            if name not in speaker_list:
                speaker_list.append(name)

        if not as_objects:
            return speaker_list

        speaker_model_list = []

        for speaker in speaker_list:
            speaker_model = SpeakerModel()
            speaker_model._name = speaker
            speaker_model_list.append(speaker_model)
        return speaker_model_list

    # persons which are listed in the beginning
    def get_speakers_from_castgroup(self, xml_root):
        castgroup = []
        for actor in xml_root.findall(".//tei:castGroup/tei:castItem", self.namespaces):
            real_name = actor.text

            if "," in real_name:
                comma = real_name.index(",")
                real_name = real_name[:comma]
            elif real_name[-1] == ".":
                real_name = real_name[:-1]

            castgroup.append(real_name)

        return castgroup

    def extract_act_data(self, xml_root):
        act_data = []
        position = 1
        # gets number of acts and corresponding count of scenes
        for act in xml_root.findall(".//tei:div[@type='act']", self.namespaces):

            # number_of_scenes = len(act.findall("./tei:div[@subtype='work:no']", self.namespaces))
            act_model = ActModel()
            act_model._number = position
            act_model._configurations = self.extract_subact_data(act, position)
            act_data.append(act_model)
            position += 1

        return act_data

    def extract_subact_data(self, act, position):
        config_data = []
        subact_position = 1
        for subact in act.findall("./tei:div[@subtype='work:no']", self.namespaces):
            config_model = ConfigurationModel()
            config_model._number = subact_position
            config_model._name = str(position) + " - " + str(subact_position)
            config_model._replicas = self.get_replicas_for_subact(subact)
            config_model._appearing_speakers = self.get_speakers_for_subact(subact)
            config_data.append(config_model)
            subact_position += 1
        return config_data

    def get_replicas_for_subact(self, subact):
        replica_data = []

        for subact_speaker_wrapper in subact.findall(".//tei:sp", self.namespaces):
            replica_model = ReplicaModel()
            subact_speaker = subact_speaker_wrapper.find("./tei:speaker", self.namespaces)
            name = subact_speaker.text
            if name[-1] == ".":
                name = name[:-1]

            replica_model._speaker = name
            replica_model._length = self.get_replica_length(subact_speaker_wrapper)
            replica_data.append(replica_model)

        return replica_data

    def get_replica_length(self, sub_sp_wrapper):
        length = 0
        stage_dir_length = 0
        p_tag = sub_sp_wrapper.find("./tei:p", self.namespaces)
        l_tag = sub_sp_wrapper.find("./tei:l", self.namespaces)

        if p_tag is not None:
            for element in p_tag.findall("./tei:hi[@rend='italic']", self.namespaces):
                stage_dir_length += self.get_wordcount_from_string(element.text)
            for text in p_tag.itertext():
                length += self.get_wordcount_from_string(text)
            length = length - stage_dir_length

        elif l_tag is not None:
            for element in l_tag.findall("./tei:hi[@rend='italic']", self.namespaces):
                stage_dir_length += self.get_wordcount_from_string(element.text)
            for text in l_tag.itertext():
                length += self.get_wordcount_from_string(text)
            length = length - stage_dir_length

        #Für klassische Dramen, deren Zeilenwechsel notiert wurde
        if l_tag is None:
            lg_tag = sub_sp_wrapper.findall("./tei:lg", self.namespaces)
            for lg_element in sub_sp_wrapper.findall("./tei:lg", self.namespaces):
                for l_element in lg_element.findall("./tei:l", self.namespaces):
                    length += self.get_wordcount_from_string(l_element.text)

        return length

    def get_wordcount_from_string(self, text):
        word_list = re.sub("[^\w]", " ", text).split()
        return len(word_list)


    def get_speakers_for_subact(self, subact):
        speaker_data = []

        for subact_speaker in subact.findall(".//tei:speaker", self.namespaces):
            name = subact_speaker.text
            if name[-1] == ".":
                name = name[:-1]
            if name not in speaker_data:
                speaker_data.append(name)

        return speaker_data

    def speaker_mapping(self, xml_root):
        castgroup = self.get_speakers_from_castgroup(xml_root)
        all_speakers = self.get_all_speakers(xml_root, False)
        print (castgroup)
        print (all_speakers)

        # stopwortliste!!!!!!
        # compare lists

        #for castgroup_member in castgroup:
            #for speaker in all_speakers:



def main():
    parser = DramaParser()
    parser.parse_xml('../Korpus/krue_geistlichen_k.xml')

if __name__ == "__main__":
    main()


    # Ideen fürs Mapping:
    # wenn nur eine Person pro Tag drinsteht, ein Name vor dem Komma, mehrere nach dem Komma -> Stoppwortliste
    # 'gemm_hausvater' überprüfen, ob mehrere Punkte genutzt werden und einfach alles ignorieren?
    # 'zwsch_abbelino': mehreren Personen eine Bezeichnung zugewiesen, zB Diener, 
    #       aber das steht erst einige Zeilen weiter unten: erkennbar: Die Zeilen schließen nicht mit Punkt ab???

    # gemm_hausvater hat noch handlungen????!!!