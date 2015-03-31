Search.DramaListView = function(){
	var that = {};

	var init = function(){
		setAllSelector();
	};

	var setAllSelector = function(){
		$("#all-selector").on("click", selectAll);
	};

	var selectAll = function(event){
		console.log($(event.target).prop("checked"));

		if($(event.target).prop("checked")){
			console.log("check");
			$("td input[type='checkbox']").prop("checked", true);
		}else{
			$("td input[type='checkbox']").prop("checked", false);
			
		}
	};

	/*var renderList = function(list){
		$("#table-tbody").empty();
		console.log("hello world");
		if(list.length !== undefined){
			for(var i = 0; i < list.length; i++){
				renderListItem(list[i]);
			}
		}else{
			for(var drama_id in list){
				renderListItem(list[drama_id]);
			}
		}
	};*/

	var showNoResults = function(){
		$("#no-results").fadeIn("slow");
	};

	var renderListItem = function(listItem){
		$("#no-results").css("display", "none");
		var row = createListItem(listItem);
		$("#table-tbody").append(row);
	};

	var createListItem = function(drama){
		var row = $("<tr>");

		var firstTd = $("<td>");
		firstTd.addClass("selection-box");
		var checkbox = $("<input checked>");
		checkbox.attr("type", "checkbox");
		checkbox.attr("drama_id", drama.id);
		firstTd.append(checkbox);
		row.append(firstTd);

		row.append(($("<td>")).text(drama.title));

		row.append(($("<td>")).text(drama.author));

		if(drama.type !== undefined){
			row.append(($("<td>")).text(drama.type));
		}else{
			row.append(($("<td>")).text("Unbekannt"));
		}

		row.append(($("<td>")).text(drama.year));
		row.append(($("<td>")).text(drama.number_of_acts));
		row.append(($("<td>")).text(drama.number_of_scenes));
		row.append(($("<td>")).text(getNumberOfSpeakers(drama)));

		row.append(($("<td>")).text(roundToTwoDecimals(drama.configuration_density)));
		row.append(($("<td>")).text(drama.number_of_speeches_in_drama));
		row.append(($("<td>")).text(roundToTwoDecimals(drama.average_length_of_speeches_in_drama)));
		row.append(($("<td>")).text(drama.median_length_of_speeches_in_drama));
		row.append(($("<td>")).text(drama.maximum_length_of_speeches_in_drama));
		row.append(($("<td>")).text(drama.minimum_length_of_speeches_in_drama));
		var tdDownload = $("<td>");
		var spanDownload = $("<span>");
		spanDownload.addClass("glyphicon glyphicon-download");
		tdDownload.attr("title", "Download JSON");
		tdDownload.append(spanDownload);
		row.append(tdDownload);

		row.attr("drama_id", drama.id);
		row.on("click", dramaClicked);

		return row;
	};

	var dramaClicked = function(event){
		if($(event.target).is("input")){
			return;
		}
		var $row = ($(event.target).parent());
		var drama_id = ($row.attr("drama_id"));
		var title = $($row.children()[1]).text();
		var author = $($row.children()[2]).text();
		var year = $($row.children()[4]).text();
		$(that).trigger("DramaClicked", [drama_id, title, author, year]);
	};

	var getNumberOfSpeakers = function(drama){
		var speakers = drama.speakers;
		return speakers.length;
	};

	var roundToTwoDecimals = function(number){
		number = (Math.round(number * 100)/100).toFixed(2);
		return number
	};

	var emptyTable = function(){
		$("#table-tbody").empty();
	};

	that.init = init;
	that.renderListItem = renderListItem;
	that.emptyTable = emptyTable;
	that.showNoResults = showNoResults;

	return that;
};