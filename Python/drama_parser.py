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

    # starting point for the parsing
    def parse_xml(self, filepath):
        drama_model = DramaModel()
        xml_root = self.get_xml_root(filepath) # get xml treeroot

        # create speaker mapping
        self.speaker_mapping(xml_root)

        # general information
        drama_model._title = self.get_title(xml_root)
        drama_model._author = self.get_author(xml_root)
        drama_model._date = self.get_date(xml_root)
        drama_model._year = drama_model._date['when'];
        drama_model._type = self.get_type(filepath)

        drama_model._subact_type = self.get_subact_type(xml_root)
        drama_model._acts = self.extract_act_data(xml_root)
        drama_model._speakers = self.get_all_speakers(xml_root)
        drama_model._castgroup = self.get_speakers_from_castgroup(xml_root)

        drama_model.calc_config_density()
        drama_model.calc_config_matrix()
        drama_model.calc_speaker_relations()
        drama_model.calc_replicas_statistics()

        for act in drama_model._acts:
            act.calc_replicas_statistics()
            for configuration in act._configurations:
                configuration.calc_replicas_statistics()

        drama_model.add_replicas_to_speakers()
        for speaker in drama_model._speakers:
            speaker.calc_replicas_statistics()

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
            # for attributes which can contain commas
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

    def generateDenormalizedJSON(self):
        dramas = []
        for filename in os.listdir("../Korpus"):
            try:
                dramaModel = self.parse_xml("../Korpus/" + filename)
                dramas.append(dramaModel)
                print("Erfolg")
            except:
                print("Fehler")

        dramas_output = OrderedDict({})
        i = 0
        drama_level_infos = []
        speakers_level_infos = OrderedDict({})
        acts_level_infos = OrderedDict({})
        scenes_level_infos = OrderedDict({})
        print len(dramas);

        for drama in dramas:
            drama_level_info = self.generateDenormalizedDramaData(drama, i)
            drama_level_infos.append(drama_level_info)

            speakers_level_info = self.generateJSONforSpeakers(drama._speakers)
            speakers_level_infos[i] = speakers_level_info

            acts_level_info = self.generateDenormalizedJSONforActs(drama._acts)
            acts_level_infos[i] = acts_level_info

            scenes_level_info = OrderedDict({})
            iterator = 0
            for act in drama._acts:
                scenes_level_info[iterator] = self.generateJSONforConfigurations(act._configurations)
                iterator = iterator + 1
            scenes_level_infos[i] = scenes_level_info

            i = i + 1
        dramas_output["drama_data"] = drama_level_infos
        dramas_output["speakers_data"] = speakers_level_infos
        dramas_output["acts_data"] = acts_level_infos
        dramas_output["scenes_data"] = scenes_level_infos

        dramas_json = json.dumps(dramas_output, indent=4, ensure_ascii=True) 
        doc = open('Dramas_data.json', 'w')
        doc.write(dramas_json)
        doc.close

    def generateDenormalizedDramaData(self, drama, drama_id):
        drama_data = OrderedDict({})
        drama_data['id'] = drama_id
        drama_data['title'] = drama._title
        drama_data['author'] = drama._author
        drama_data['date'] = drama._date
        drama_data['year'] = drama._year
        drama_data['type'] = drama._type
        drama_data['castgroup'] = drama._castgroup
        drama_data['configuration_density'] = drama._configuration_density
        drama_data['number_of_speeches_in_drama'] = len(drama.get_replicas_drama())
        drama_data['average_length_of_speeches_in_drama'] = drama._replicasLength_avg
        drama_data['maximum_length_of_speeches_in_drama'] = drama._replicasLength_max
        drama_data['minimum_length_of_speeches_in_drama'] = drama._replicasLength_min
        drama_data['median_length_of_speeches_in_drama'] = drama._replicasLength_med
        drama_data['number_of_acts'] = self.getNumberOfActs(drama)
        drama_data['number_of_scenes'] = self.getNumberOfScenes(drama)
        drama_data['speakers'] = self.getListOfSpeakers(drama);
        return drama_data

    def generateDramaData(self, drama):
        drama_data = OrderedDict({})
        drama_data['title'] = drama._title
        drama_data['author'] = drama._author
        drama_data['date'] = drama._date
        drama_data['type'] = drama._type
        drama_data['castgroup'] = drama._castgroup
        """
        drama_data['All Speakers'] = all_speakers
        """
        drama_data['configuration_density'] = drama._configuration_density
        drama_data['number_of_speeches_in_drama'] = len(drama.get_replicas_drama())
        drama_data['average_length_of_speeches_in_drama'] = drama._replicasLength_avg
        drama_data['maximum_length_of_speeches_in_drama'] = drama._replicasLength_max
        drama_data['minimum_length_of_speeches_in drama'] = drama._replicasLength_min
        drama_data['median_length_of_speeches_in_drama'] = drama._replicasLength_med

        speakers_json = self.generateJSONforSpeakers(drama._speakers)
        drama_data['speakers'] = speakers_json

        acts_json = self.generateJSONforActs(drama._acts)
        drama_data['content'] = acts_json

        return drama_data;

    def getNumberOfActs(self, drama):
        return len(drama._acts)

    def getNumberOfScenes(self, drama):
        number = 0
        for act in drama._acts:
            number = number + len(act._configurations)
        return number

    def getListOfSpeakers(self, drama):
        speakersList = []
        for speaker in drama._speakers:
            speakersList.append(speaker._name)
        return speakersList

    def writeJSON(self, dramaData):
        drama_json = json.dumps(dramaData, indent=4, ensure_ascii=True)
        #print(drama_json)
        doc = open(dramaData["Author"]+ "_"+dramaData["Title"]+'_data.json', 'w')
        doc.write(drama_json)
        doc.close

    def generateJSONforSpeakers(self, speakers):
        speakers_data = []
        for speaker in speakers:
            speaker_data = OrderedDict({})
            speaker_data['name'] = speaker._name
            speaker_data['number_of_speakers_speeches'] = len(speaker._replicas)
            speaker_data['average_length_of_speakers_speeches'] = speaker._replicasLength_avg
            speaker_data['maximum_length_of_speakers_speeches'] = speaker._replicasLength_max
            speaker_data['minimum_length_of_speakers_speeches'] = speaker._replicasLength_min
            speaker_data['median_length_of_speakers_speeches'] = speaker._replicasLength_med

            speaker_relations = OrderedDict({})
            speaker_relations['concomitant'] = speaker._concomitant
            speaker_relations['alternative'] = speaker._alternative
            speaker_relations['dominates'] = speaker._dominates
            speaker_relations['gets_dominated_by'] = speaker._gets_dominated_by
            speaker_relations['independent'] = speaker._independent

            speaker_data["relations"] = speaker_relations
            speakers_data.append(speaker_data)

        return speakers_data

    def generateDenormalizedJSONforActs(self, acts):
        acts_data = []
        iterator = 1
        for act in acts:
            act_data = OrderedDict({})
            act_data['number_of_act'] = act._number
            act_data['number_of_speeches_in_act'] = len(act.get_replicas_act())
            act_data['average_length_of_speeches_in_act'] = act._replicasLength_avg
            act_data['maximum_length_of_speeches_in_act'] = act._replicasLength_max
            act_data['minimum_length_of_speeches_in_act'] = act._replicasLength_min
            act_data['median_length_of_speeches_in_act'] = act._replicasLength_med

            acts_data.append(act_data)

        return acts_data

    def generateJSONforActs(self, acts):
        acts_data = []
        iterator = 1
        for act in acts:
            act_data = OrderedDict({})
            act_data['number_of_act'] = act._number
            act_data['number_of_speeches_in_act'] = len(act.get_replicas_act())
            act_data['average_length_of_speeches_in_act'] = act._replicasLength_avg
            act_data['maximum_length_of_speeches_in_act'] = act._replicasLength_max
            act_data['minimum_length_of_speeches_in_act'] = act._replicasLength_min
            act_data['median_length_of_speeches_in_act'] = act._replicasLength_med

            configurations_json = self.generateJSONforConfigurations(act._configurations)
            act_data['scenes'] = configurations_json

            acts_data.append(act_data)

        return acts_data

    def generateJSONforConfigurations(self, configurations):
        configurations_data = []

        for configuration in configurations:
            configuration_data = OrderedDict({})
            configuration_data['number_of_scene'] = configuration._number
            configuration_data['number_of_speeches_in_scene'] = len(configuration._replicas)
            configuration_data['appearing_speakers'] = configuration._appearing_speakers
            configuration_data['average_length_of_speeches_in_scene'] = configuration._replicasLength_avg
            configuration_data['maximum_length_of_speeches_in_scene'] = configuration._replicasLength_max
            configuration_data['minimum_length_of_speeches_in_scene'] = configuration._replicasLength_min
            configuration_data['median_length_of_speeches_in_scene'] = configuration._replicasLength_med

            configurations_data.append(configuration_data)

        return configurations_data

    def generateConfMatrixCSV(self, drama_model):
        doc = open(drama_model._author+"_"+drama_model._title+'_matrix.csv', 'w', newline="")
        writer = csv.writer(doc, delimiter=",")
        cf = drama_model._configuration_matrix
        writer.writerows(cf)
        doc.close

    # returns the xml root for the file
    def get_xml_root(self, filepath):
        tree = ET.parse(filepath)
        return tree.getroot()

    # returns the drama title
    def get_title(self, xml_root):
        title = xml_root.find(".//tei:fileDesc/tei:titleStmt/tei:title", self.namespaces).text
        return title

    # returns the drama author
    def get_author(self, xml_root):
        author = xml_root.find(".//tei:sourceDesc/tei:biblFull/tei:titleStmt/tei:author", self.namespaces).text
        return author

    # returns the drama date
    def get_date(self, xml_root):
        date = xml_root.find(".//tei:profileDesc/tei:creation/tei:date", self.namespaces).attrib
        if "when" in date:
            date['when'] = (int) (date['when'])
        #print("Date: ", date)
        if "notBefore" in date:
            #print "if clause"
            date['when'] = ((int) (date['notBefore']) + (int) (date['notAfter'])) / 2

        #print("Date...: ", date)
        return date

    # returns the drama type from the filename
    def get_type(self, filepath):
        if filepath.find("_s.xml") != -1:
            return "Schauspiel"
        elif filepath.find("_t.xml") != -1:
            return "Trauerspiel"
        elif filepath.find("_k.xml") != -1:
            return "Komoedie"

    # returns if the drama contains Szene or Auftritt
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
        for speaker in xml_root.findall(".//tei:div[@type='act']//tei:speaker", self.namespaces):
            name = speaker.text
            if name and name[-1] == ".":
                name = name[:-1]
            if name and name not in speaker_list:
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
            elif real_name and real_name[-1] == ".":
                real_name = real_name[:-1]

            castgroup.append(real_name)

        return castgroup

    # returns informations about all acts of the drama
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

    # returns informations about all subacts of the drama
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

    # returns replica for subact
    def get_replicas_for_subact(self, subact):
        replica_data = []

        for subact_speaker_wrapper in subact.findall(".//tei:sp", self.namespaces):
            replica_model = ReplicaModel()
            subact_speaker = subact_speaker_wrapper.find("./tei:speaker", self.namespaces)
            name = subact_speaker.text
            if name and name[-1] == ".":
                name = name[:-1]

            replica_model._speaker = name
            replica_model._length = self.get_replica_length(subact_speaker_wrapper)

            # replica with a length of zero or less are not added
            if(replica_model._length > 0):
                replica_data.append(replica_model)

        return replica_data

    # calculates length of replica
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

        # for classic dramas with noted line breaks
        if l_tag is None:
            lg_tag = sub_sp_wrapper.findall("./tei:lg", self.namespaces)
            for lg_element in sub_sp_wrapper.findall("./tei:lg", self.namespaces):
                for l_element in lg_element.findall("./tei:l", self.namespaces):
                    length += self.get_wordcount_from_string(l_element.text)

        return length

    # calculates the wordcount of a string
    def get_wordcount_from_string(self, text):
        word_list = re.sub("[^\w]", " ", text).split()
        return len(word_list)

    # returns all speakers for the subact
    def get_speakers_for_subact(self, subact):
        speaker_data = []

        for subact_speaker in subact.findall(".//tei:speaker", self.namespaces):
            name = subact_speaker.text
            if name and name[-1] == ".":
                name = name[:-1]
            if name and name not in speaker_data:
                speaker_data.append(name)

        return speaker_data

    # generates a mapping for speakers and castgroup
    def speaker_mapping(self, xml_root):
        castgroup = self.get_speakers_from_castgroup(xml_root)
        all_speakers = self.get_all_speakers(xml_root, False)
        #print (castgroup)
        #print (all_speakers)

        # stopwortliste!!!!!!
        # compare lists

        #for castgroup_member in castgroup:
            #for speaker in all_speakers:


        # Ideen fürs Mapping:
        # wenn nur eine Person pro Tag drinsteht, ein Name vor dem Komma, mehrere nach dem Komma -> Stoppwortliste
        # 'gemm_hausvater' überprüfen, ob mehrere Punkte genutzt werden und einfach alles ignorieren?
        # 'zwsch_abbelino': mehreren Personen eine Bezeichnung zugewiesen, zB Diener, 
        #       aber das steht erst einige Zeilen weiter unten: erkennbar: Die Zeilen schließen nicht mit Punkt ab???


def main():
    debug = False

    #to generate one json-file
    """
    parser = DramaParser()
    dramaModel = parser.parse_xml("../Korpus/weis_masaniello_t.xml")
    drama_data = parser.generateDramaData(dramaModel)
    parser.writeJSON(drama_data)
    """

    """
    #to generate a json-file of all dramas
    parser = DramaParser()
    dramas = []

    if debug:

        for filename in os.listdir("../Korpus"):
            dramaModel = parser.parse_xml("../Korpus/" + filename)
            data = parser.generateDramaData(dramaModel)
            dramas.append(data)
            print("Erfolg beim Parsen eines Dramas")

    else:
        for filename in os.listdir("../Korpus"):
            try:
                dramaModel = parser.parse_xml("../Korpus/" + filename)
                data = parser.generateDramaData(dramaModel)
                dramas.append(data)
                print("Erfolg beim Parsen eines Dramas")
            except:
                print("Fehler beim Parsen eines Dramas")
                print("!!! " + filename)


    print(len(dramas))
    dramas_json = json.dumps(dramas, indent=4, ensure_ascii=True) 
    doc = open('Dramas_data.json', 'w')
    doc.write(dramas_json)
    doc.close
    """
    parser = DramaParser()
    parser.generateDenormalizedJSON()


if __name__ == "__main__":
    main()

