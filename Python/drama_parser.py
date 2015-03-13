#coding: utf8

import xml.etree.ElementTree as ET
import re
import json
import csv
import os
from drama_models import *
from collections import OrderedDict

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
        drama_model._castgroup = self.get_speakers_from_castgroup(xml_root)

        drama_model.calc_config_density()
        drama_model.calc_config_matrix()
        drama_model.calc_speaker_relations()
        drama_model.calc_replicas_statistics()
        #print (vars(drama_model))

        for act in drama_model._acts:
            act.calc_replicas_statistics()
            for configuration in act._configurations:
                #print(configuration._name)
                configuration.calc_replicas_statistics()

        drama_model.add_replicas_to_speakers()
        for speaker in drama_model._speakers:
            speaker.calc_replicas_statistics()
            #print (vars(speaker))

        #self.generateJSON(drama_model)
        #self.generateConfMatrixCSV(drama_model)
        #self.generateBasicCSV(drama_model)
        return drama_model

    def generateBasicCSV(self, dramas):
        basicCsv = []
        firstRow = ["Title", "Author", "Date", "Type", "Conf.Density",
        "Number of Replicas", "Avg. Length of Replicas","Max. Length of Replicas",
        "Min. Length of Replicas", "Med. Length of Replicas"]
        basicCsv.append(firstRow);
        for drama in dramas:
            #Für Attribute die Kommas enthalten können
            title = drama._title.replace(",", "")
            author = drama._author.replace(",", "")
            date = str(drama._date).replace(",", "")

            dramaData = [title, author, date, drama._type,
                drama._configuration_density, len(drama.get_replicas_drama()),
                drama._replicasLength_avg, drama._replicasLength_max, drama._replicasLength_min,
                drama._replicasLength_med]
            basicCsv.append(dramaData)        

        doc = open('basicData.csv', 'w', newline="")
        writer = csv.writer(doc, delimiter=",")
        writer.writerows(basicCsv)
        doc.close

    def generateJSON(self, drama):
        drama_data = OrderedDict({})
        drama_data['Title'] = drama._title
        drama_data['Author'] = drama._author
        drama_data['Date'] = drama._date
        drama_data['Type'] = drama._type
        drama_data['Castgroup'] = drama._castgroup
        """
        drama_data['All Speakers'] = all_speakers
        """
        drama_data['Configuration Density'] = drama._configuration_density
        drama_data['Number of Replicas in Drama'] = len(drama.get_replicas_drama())
        drama_data['Average Length of Replicas in Drama'] = drama._replicasLength_avg
        drama_data['Maximum Length of Replicas in Drama'] = drama._replicasLength_max
        drama_data['Minimum Length of Replicas in Drama'] = drama._replicasLength_min
        drama_data['Median Length of Replicas in Drama'] = drama._replicasLength_med

        speakers_json = self.generateJSONforSpeakers(drama._speakers)
        drama_data['Speakers'] = speakers_json

        acts_json = self.generateJSONforActs(drama._acts)
        drama_data['Content'] = acts_json

        drama_json = json.dumps(drama_data, indent=4, ensure_ascii=False)
        drama_output = OrderedDict({})
        drama_output[0] = drama_data
        drama_output_json = json.dumps(drama_output, indent=4, ensure_ascii=False)
        print(drama_output_json)  

        doc = open(drama._author+ "_"+drama._title+'_data.json', 'w')
        doc.write(drama_json)
        doc.close

    def generateJSONforSpeakers(self, speakers):
        speakers_data = []
        for speaker in speakers:
            speaker_data = OrderedDict({})
            speaker_data['Name'] = speaker._name
            speaker_data['Number of Speakers Replicas'] = len(speaker._replicas)
            speaker_data['Average Length of Speakers Replicas'] = speaker._replicasLength_avg
            speaker_data['Maximum Length of Speakers Replicas'] = speaker._replicasLength_max
            speaker_data['Minimum Length of Speakers Replicas'] = speaker._replicasLength_min
            speaker_data['Median Length of Speakers Replicas'] = speaker._replicasLength_med

            speaker_relations = OrderedDict({})
            speaker_relations['Concomitant'] = speaker._concomitant
            speaker_relations['Alternative'] = speaker._alternative
            speaker_relations['Dominates'] = speaker._dominates
            speaker_relations['Gets dominated by'] = speaker._gets_dominated_by
            speaker_relations['Independent'] = speaker._independent

            speaker_data["Relations"] = speaker_relations
            speakers_data.append(speaker_data)

        return speakers_data

    def generateJSONforActs(self, acts):
        acts_data = []
        iterator = 1
        for act in acts:
            act_data = OrderedDict({})
            act_data['Number of Act'] = act._number
            act_data['Number of Replicas in Act'] = len(act.get_replicas_act())
            act_data['Average Length of Replicas in Act'] = act._replicasLength_avg
            act_data['Maximum Length of Replicas in Act'] = act._replicasLength_max
            act_data['Minimum Length of Replicas in Act'] = act._replicasLength_min
            act_data['Median Length of Replicas in Act'] = act._replicasLength_med

            configurations_json = self.generateJSONforConfigurations(act._configurations)
            act_data['Scenes_Configurations'] = configurations_json

            acts_data.append(act_data)

        return acts_data

    def generateJSONforConfigurations(self, configurations):
        configurations_data = []

        for configuration in configurations:
            configuration_data = OrderedDict({})
            configuration_data['Number of Scene_Configuration'] = configuration._number
            configuration_data['Number of Replicas in Scene_Configuration'] = len(configuration._replicas)
            configuration_data['Appearing Speakers'] = configuration._appearing_speakers
            configuration_data['Average Length of Replicas in Scene'] = configuration._replicasLength_avg
            configuration_data['Maximum Length of Replicas in Scene'] = configuration._replicasLength_max
            configuration_data['Minimum Length of Replicas in Scene'] = configuration._replicasLength_min
            configuration_data['Median Length of Replicas in Scene'] = configuration._replicasLength_med

            configurations_data.append(configuration_data)

        return configurations_data

    def generateConfMatrixCSV(self, drama_model):

        doc = open(drama_model._author+"_"+drama_model._title+'_matrix.csv', 'w', newline="")
        writer = csv.writer(doc, delimiter=",")
        cf = drama_model._configuration_matrix
        writer.writerows(cf)
        doc.close

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

    ### Hier werden auch Speakers außerhalb Akt und Szene-Struktur erfasst
    ### Repliken außerhalb Akt und Szene Struktur werden jedoch schon erfasst
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
            #print(speaker_model._name)
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

            #Repliken mit Länge 0 (oder geringer) nicht hinzufügen
            if(replica_model._length > 0):
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
        #print (castgroup)
        #print (all_speakers)

        # stopwortliste!!!!!!
        # compare lists

        #for castgroup_member in castgroup:
            #for speaker in all_speakers:

def main():

    dramas = []
    parser = DramaParser()
    dramaModel = parser.parse_xml("../Korpus/arnim_halle_s.xml")
    parser.generateJSON(dramaModel)


    #Schleife über alle Dramen
    """
    for filename in os.listdir("../Korpus"):
        try:
            dramaModel = parser.parse_xml("../Korpus/" + filename)
            parser.generateJSON(dramaModel)
        except:
            print("Fehler beim Parsen eines Dramas")
    """
    

if __name__ == "__main__":
    main()


    # Ideen fürs Mapping:
    # wenn nur eine Person pro Tag drinsteht, ein Name vor dem Komma, mehrere nach dem Komma -> Stoppwortliste
    # 'gemm_hausvater' überprüfen, ob mehrere Punkte genutzt werden und einfach alles ignorieren?
    # 'zwsch_abbelino': mehreren Personen eine Bezeichnung zugewiesen, zB Diener, 
    #       aber das steht erst einige Zeilen weiter unten: erkennbar: Die Zeilen schließen nicht mit Punkt ab???

    # gemm_hausvater hat noch handlungen????!!!