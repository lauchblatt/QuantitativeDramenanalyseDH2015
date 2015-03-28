#coding: utf8

import json
import csv
from collections import OrderedDict

# class for generating output about dramas
class DramaOutput:

    def generateBasicCSV(self, dramas):
        basicCsv = []
        firstRow = ["Title", "Author", "Date", "Type", "Conf.Density",
        "Number of Speeches", "Avg. Length of Speeches","Max. Length of Speeches",
        "Min. Length of Speeches", "Med. Length of Speeches"]
        basicCsv.append(firstRow);
        for drama in dramas:
            # for attributes which can contain commas
            title = drama._title.replace(",", "")
            author = drama._author.replace(",", "")
            date = str(drama._date).replace(",", "")

            dramaData = [title, author, date, drama._type,
                drama._configuration_density, len(drama.get_speeches_drama()),
                drama._speechesLength_avg, drama._speechesLength_max, drama._speechesLength_min,
                drama._speechesLength_med]
            basicCsv.append(dramaData)        

        doc = open('basicData.csv', 'w', newline="")
        writer = csv.writer(doc, delimiter=",")
        writer.writerows(basicCsv)
        doc.close

    def generateDramaData(self, drama):
        drama_data = OrderedDict({})
        drama_data['title'] = drama._title
        drama_data['author'] = drama._author
        drama_data['date'] = drama._date
        drama_data['type'] = drama._type
        drama_data['castgroup'] = drama._castgroup
        drama_data['speaker_count_castgroup'] = drama._speakerCountCast
        drama_data['speaker_count'] = drama._speakerCountAll
        """
        drama_data['All Speakers'] = all_speakers
        """
        drama_data['configuration_density'] = drama._configuration_density
        drama_data['number_of_speeches_in_drama'] = len(drama.get_speeches_drama())
        drama_data['average_length_of_speeches_in_drama'] = drama._speechesLength_avg
        drama_data['maximum_length_of_speeches_in_drama'] = drama._speechesLength_max
        drama_data['minimum_length_of_speeches_in drama'] = drama._speechesLength_min
        drama_data['median_length_of_speeches_in_drama'] = drama._speechesLength_med

        speakers_json = self.generateJSONforSpeakers(drama._speakers)
        drama_data['speakers'] = speakers_json

        acts_json = self.generateJSONforActs(drama._acts)
        drama_data['content'] = acts_json

        return drama_data;

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
            speaker_data['number_of_speakers_speeches'] = len(speaker._speeches)
            speaker_data['average_length_of_speakers_speeches'] = speaker._speechesLength_avg
            speaker_data['maximum_length_of_speakers_speeches'] = speaker._speechesLength_max
            speaker_data['minimum_length_of_speakers_speeches'] = speaker._speechesLength_min
            speaker_data['median_length_of_speakers_speeches'] = speaker._speechesLength_med

            speaker_relations = OrderedDict({})
            speaker_relations['concomitant'] = speaker._concomitant
            speaker_relations['alternative'] = speaker._alternative
            speaker_relations['dominates'] = speaker._dominates
            speaker_relations['gets_dominated_by'] = speaker._gets_dominated_by
            speaker_relations['independent'] = speaker._independent

            speaker_data["relations"] = speaker_relations
            speakers_data.append(speaker_data)

        return speakers_data

    def generateJSONforActs(self, acts):
        acts_data = []
        iterator = 1
        for act in acts:
            act_data = OrderedDict({})
            act_data['number_of_act'] = act._number
            act_data['number_of_speeches_in_act'] = len(act.get_speeches_act())
            act_data['appearing_speakers'] = act._appearing_speakers

            act_data['average_length_of_speeches_in_act'] = act._speechesLength_avg
            act_data['maximum_length_of_speeches_in_act'] = act._speechesLength_max
            act_data['minimum_length_of_speeches_in_act'] = act._speechesLength_min
            act_data['median_length_of_speeches_in_act'] = act._speechesLength_med

            configurations_json = self.generateJSONforConfigurations(act._configurations)
            act_data['scenes'] = configurations_json

            acts_data.append(act_data)

        return acts_data

    def generateJSONforConfigurations(self, configurations):
        configurations_data = []

        for configuration in configurations:
            configuration_data = OrderedDict({})
            configuration_data['number_of_scene'] = configuration._number
            configuration_data['number_of_speeches_in_scene'] = len(configuration._speeches)
            configuration_data['appearing_speakers'] = configuration._appearing_speakers
            configuration_data['average_length_of_speeches_in_scene'] = configuration._speechesLength_avg
            configuration_data['maximum_length_of_speeches_in_scene'] = configuration._speechesLength_max
            configuration_data['minimum_length_of_speeches_in_scene'] = configuration._speechesLength_min
            configuration_data['median_length_of_speeches_in_scene'] = configuration._speechesLength_med

            configuration_data['speeches'] = self.generateJSONforSpeeches(configuration._speeches)

            configurations_data.append(configuration_data)

        return configurations_data

    def generateJSONforSpeeches(self, speeches):
        speeches_data = []

        for speech in speeches:
            speech_data = OrderedDict({})

            speech_data['speaker'] = speech._speaker
            speech_data['length'] = speech._length

            speeches_data.append(speech_data)

        return speeches_data

    def generateConfMatrixCSV(self, drama_model):
        doc = open(drama_model._author+"_"+drama_model._title+'_matrix.csv', 'w', newline="")
        writer = csv.writer(doc, delimiter=",")
        cf = drama_model._configuration_matrix
        writer.writerows(cf)
        doc.close

    def generateDenormalizedJSON(self, dramas):
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
        drama_data['number_of_speeches_in_drama'] = len(drama.get_speeches_drama())
        drama_data['average_length_of_speeches_in_drama'] = drama._speechesLength_avg
        drama_data['maximum_length_of_speeches_in_drama'] = drama._speechesLength_max
        drama_data['minimum_length_of_speeches_in_drama'] = drama._speechesLength_min
        drama_data['median_length_of_speeches_in_drama'] = drama._speechesLength_med
        drama_data['number_of_acts'] = self.getNumberOfActs(drama)
        drama_data['number_of_scenes'] = self.getNumberOfScenes(drama)
        drama_data['speakers'] = self.getListOfSpeakers(drama);
        return drama_data

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

    def generateDenormalizedJSONforActs(self, acts):
        acts_data = []
        iterator = 1
        for act in acts:
            act_data = OrderedDict({})
            act_data['number_of_act'] = act._number
            act_data['number_of_speeches_in_act'] = len(act.get_speeches_act())
            act_data['appearing_speakers'] = act._appearing_speakers
            
            act_data['average_length_of_speeches_in_act'] = act._speechesLength_avg
            act_data['maximum_length_of_speeches_in_act'] = act._speechesLength_max
            act_data['minimum_length_of_speeches_in_act'] = act._speechesLength_min
            act_data['median_length_of_speeches_in_act'] = act._speechesLength_med

            acts_data.append(act_data)

        return acts_data