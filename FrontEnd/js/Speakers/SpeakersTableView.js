Speakers.SpeakersTableView = function(){
	var that = {};

	var init = function(){

	};

	var renderTable = function(speakersInfo){
		$table = $("#table-tbody");
		for(i = 0; i < speakersInfo.length; i++){
			var $item = createSpeakerItem(speakersInfo[i]);
			$table.append($item);
		}

	};

	var createSpeakerItem = function(speaker){
		var row = $("<tr>");


		row.append(($("<td>")).text(speaker.name));
		row.append(($("<td>")).text(speaker.number_of_appearances));
		row.append(($("<td>")).text(speaker.appearances_percentage + " %"));
		row.append(($("<td>")).text(speaker.number_of_speakers_speeches));
		row.append(($("<td>")).text(speaker.average_length_of_speakers_speeches));
		row.append(($("<td>")).text(speaker.median_length_of_speakers_speeches));
		row.append(($("<td>")).text(speaker.maximum_length_of_speakers_speeches));
		row.append(($("<td>")).text(speaker.minimum_length_of_speakers_speeches));

		return row;
	};

	that.renderTable = renderTable;
	that.init = init;

	return that;
};