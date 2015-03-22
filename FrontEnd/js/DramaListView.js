Search.DramaListView = function(){
	var that = {};

	var init = function(){

	};

	var renderList = function(){

	};

	var renderListItem = function(listItem){
		var row = createListItem(listItem);
		$("#table-tbody").append(row);
		$("#loading").css("display","none");
	};

	var createListItem = function(drama){
		var row = $("<tr>");

		row.append(($("<td>")).text(drama.title));

		row.append(($("<td>")).text(drama.author));

		if(drama.type !== undefined){
			row.append(($("<td>")).text(drama.type));
		}else{
			row.append(($("<td>")).text("Unbekannt"));
		}

		if(drama.date.middle !== undefined){
			row.append(($("<td>")).text("ca. " + drama.date.middle));
		}else{
			row.append(($("<td>")).text(drama.date.when));
		}

		row.append(($("<td>")).text(roundToTwoDecimals(drama.configuration_density)));
		row.append(($("<td>")).text(drama.number_of_speeches_in_Drama));
		row.append(($("<td>")).text(roundToTwoDecimals(drama.average_length_of_speeches_in_drama)));
		row.append(($("<td>")).text(drama.median_length_of_speeches_in_drama));
		row.append(($("<td>")).text(drama.maximum_length_of_speeches_in_drama));
		row.append(($("<td>")).text(drama.minimum_length_of_speeches_in_drama));

		return row;
	};

	var roundToTwoDecimals = function(number){
		number = (Math.round(number * 100)/100).toFixed(2);
		return number
	};

	that.init = init;
	that.renderListItem = renderListItem;

	return that;
};