#coding: utf8

from statistic_functions import *
from collections import OrderedDict

# model for the whole drama
class DramaModel:

    def __init__ (self):
        self._title = None
        self._date = None
        self._type = None
        self._author = None
        self._acts = None
        # Zur Hilfe alle Speakers speichern, damit sie ueberhaupt irgendwo sind
        self._speakers = None
        self._castgroup = None
        self._speakerCount = None

        # Kann man berechnen innerhalb der Klasse ueber Konfigurationen der Akte
        self._configuration_matrix = None
        self._configuration_density = None

        self._speechesLength_avg = None
        self._speechesLength_max = None
        self._speechesLength_min = None
        self._speechesLength_med = None
        
    # calculates the configuration matrix
    def calc_config_matrix (self):
        configuration_matrix = []
        firstRow = ["Speaker/Configuration"]
        firstRow.extend(self.getAllConfigurationNames())
        configuration_matrix.append(firstRow)

        for speaker in self._speakers:
            nextRow = [speaker._name]
            nextRow.extend(self.getMatrixRow(speaker))
            configuration_matrix.append(nextRow)
        self._configuration_matrix = configuration_matrix

    def getAllConfigurationNames(self):
        configurationNames = []
        for act in self._acts:
            for configuration in act._configurations:
                configurationNames.append(configuration._name)
        return configurationNames

    def getMatrixRow(self, speaker):
        config_bin = []
        for act in self._acts:
            for configuration in act._configurations:
                if(speaker._name in configuration._appearing_speakers):
                    config_bin.append(1)
                else:
                    config_bin.append(0)
        return config_bin

    # calculates the configuration density
    def calc_config_density (self):
        sum_all = 0
        sum_speaking = 0
        for act in self._acts:
            for configuration in act._configurations:
                sum_speaking += len(configuration._appearing_speakers)
                sum_all += len(self._speakers)

        self._configuration_density = float(sum_speaking) / sum_all

    # calculates the speaker relations
    def calc_speaker_relations (self):
        for speaker in self._speakers:
            speaker._concomitant = self.get_concomitant_speakers(speaker)
            speaker._alternative = self.get_alternative_speakers(speaker)
        for speaker in self._speakers:
            self.check_dominating_status(speaker)
        for speaker in self._speakers:
            speaker._independent = self.get_independent_speakers(speaker)

    # returns a list of all speakers
    def get_list_of_speaker_names(self, current_speaker):
        speaker_names = []
        for speaker in self._speakers:
            if speaker is not current_speaker:
                speaker_names.append(speaker._name)
        return speaker_names

    # claculates concomitant speakers
    def get_concomitant_speakers (self, speaker):
        concomitant_speakers = self.get_list_of_speaker_names(speaker)
        for act in self._acts:
            for configuration in act._configurations:
                if speaker._name in configuration._appearing_speakers:
                    concomitant_speakers = list(set(concomitant_speakers).intersection(configuration._appearing_speakers))
        return concomitant_speakers

    # # claculates alternative speakers
    def get_alternative_speakers(self, speaker):
        alternative_speakers = self.get_list_of_speaker_names(speaker)
        for act in self._acts:
            for configuration in act._configurations:
                if speaker._name in configuration._appearing_speakers:
                    alternative_speakers = list(set(alternative_speakers) - set(configuration._appearing_speakers))
        return alternative_speakers

    # claculates dominant speakers
    def check_dominating_status(self, current_speaker):
        for speaker in self._speakers:
            if speaker is current_speaker:
                continue
            if speaker._name in current_speaker._concomitant:
                if current_speaker._name not in speaker._concomitant:
                    current_speaker._gets_dominated_by.append(speaker._name)
                    speaker._dominates.append(current_speaker._name)
                    current_speaker._concomitant.remove(speaker._name)

    # claculates independent speakers
    def get_independent_speakers(self, speaker):
        independent_speakers = self.get_list_of_speaker_names(speaker)
        independent_speakers = list(set(independent_speakers) - set(speaker._concomitant))
        independent_speakers = list(set(independent_speakers) - set(speaker._alternative))
        independent_speakers = list(set(independent_speakers) - set(speaker._dominates))
        independent_speakers = list(set(independent_speakers) - set(speaker._gets_dominated_by))
        return independent_speakers

    def get_speeches_drama(self):
        speeches_in_drama = []
        for act in self._acts:
            for configuration in act._configurations:
                for speeches in configuration._speeches:
                    speeches_in_drama.append(speeches)
        return speeches_in_drama

    def calc_speeches_statistics(self):
        speeches = self.get_speeches_drama()
        speeches_lengths = []
        for speech in speeches:
            speeches_lengths.append(speech._length)

        self._speechesLength_avg = average(speeches_lengths)
        self._speechesLength_max = max(speeches_lengths)
        self._speechesLength_min = min(speeches_lengths)
        self._speechesLength_med = median(speeches_lengths)

    def add_speeches_to_speakers(self):
        speeches = self.get_speeches_drama()
        for speech in speeches:
            for speaker in self._speakers:
                if(speech._speaker == speaker._name):
                    speaker._speeches.append(speech)
                    break

    def set_speaker_count(self):
        self._speakerCount = len(self._castgroup)

# model for acts
class ActModel:

    def __init__ (self):
        self._number = None
        #Akt besteht aus Konfigurationen
        self._configurations = None

        self._appearing_speakers = None

        self._speechesLength_avg = None
        self._speechesLength_max = None
        self._speechesLength_min = None
        self._speechesLength_med = None        

    def get_speeches_act(self):
        speeches_in_act = []
        for configuration in self._configurations:
            for speeches in configuration._speeches:
                speeches_in_act.append(speeches)
        return speeches_in_act

    def calc_speeches_statistics(self):
        speeches = self.get_speeches_act()
        speeches_lengths = []
        for speech in speeches:
            speeches_lengths.append(speech._length)

        self._speechesLength_avg = average(speeches_lengths)
        self._speechesLength_max = max(speeches_lengths)
        self._speechesLength_min = min(speeches_lengths)
        self._speechesLength_med = median(speeches_lengths)

# model for configurations
class ConfigurationModel:
    def __init__ (self):
        #Waere vielleicht nicht schlecht den Namen, also 1.Akt, 1.Szene zu speichern
        self._name = None
        self._number = None
        #Konfiguration besteht aus Repliken
        self._speeches = None
        # um spaeter leichter Beziehungen zu berechnen, als namen
        self._appearing_speakers = None

        self._speechesLength_avg = None
        self._speechesLength_max = None
        self._speechesLength_min = None
        self._speechesLength_med = None

    def calc_speeches_statistics(self):
        speeches = self._speeches
        speeches_lengths = []
        for speech in speeches:
            speeches_lengths.append(speech._length)

        if(speeches):
            self._speechesLength_avg = average(speeches_lengths)
            self._speechesLength_max = max(speeches_lengths)
            self._speechesLength_min = min(speeches_lengths)
            self._speechesLength_med = median(speeches_lengths)

# model for speech
class SpeechModel:

    def __init__ (self):
        self._id = None
        self._length = None
        #Eine Replik hat einen zugewiesenen Speaker, Name des Speakers speichern
        self._speaker = None


# model for speakers
class SpeakerModel:

    def __init__ (self):
        self._name = None   
        self._alternative_names = None
        self._speeches = []
        self._concomitant = []
        self._alternative = []
        self._dominates = []
        self._gets_dominated_by = []
        self._independent = []
        # self._repetitive_config = None

        self._speechesLength_avg = None
        self._speechesLength_med = None
        self._speechesLength_min = None
        self._speechesLength_max = None

    def calc_speeches_statistics(self):
        speeches_lengths = []
        for speeches in self._speeches:
            speeches_lengths.append(speeches._length)

        if(speeches_lengths):
            self._speechesLength_avg = average(speeches_lengths)
            self._speechesLength_max = max(speeches_lengths)
            self._speechesLength_min = min(speeches_lengths)
            self._speechesLength_med = median(speeches_lengths)
        """
        print(self._name)
        print(self._speechesLength_avg)
        print(self._speechesLength_max)
        print(self._speechesLength_min)
        print(self._speechesLength_med)
        """

