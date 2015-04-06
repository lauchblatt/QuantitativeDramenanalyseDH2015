Speakers.SpeakersTableView = function(){
	var that = {};

	var init = function(dramaInfo){
		$("#dramaTitle").text(dramaInfo.title + " (" + dramaInfo.year + ")");
		$("#dramaAuthor").text(dramaInfo.author);
		initSorting();
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

	var initSorting = function(){
		$('th').click(function(){
    		var table = $(this).parents('table').eq(0)
    		var rows = table.find('tr:gt(0)').toArray().sort(comparer($(this).index()))
    		this.asc = !this.asc
    		if (!this.asc){rows = rows.reverse()}
    		for (var i = 0; i < rows.length; i++){table.append(rows[i])}
		});
	};

	var comparer = function(index){
		return function(a, b) {
        var valA = getCellValue(a, index), valB = getCellValue(b, index)
        return $.isNumeric(valA) && $.isNumeric(valB) ? valA - valB : valA.localeCompare(valB)
    	}
	};

	var getCellValue = function(row, index){
		return $(row).children('td').eq(index).html()
	};

	that.renderTable = renderTable;
	that.init = init;

	return that;
};