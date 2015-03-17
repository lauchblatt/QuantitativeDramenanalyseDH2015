DramaAnalyzer.DramaListView = function(){
	var that = {};

	var init = function(){

	};

	var renderList = function(dramaList){
		for(var i = 0; i < dramaList.length; i++){
			console.log(dramaList[i]);
			var row = createListItem(dramaList[i]);
			$("#table-tbody").append(row);
		}
	};

	var createListItem = function(drama){
		var row = $("<tr>");
		row.append(($("<td>")).text("0"));
		row.append(($("<td>")).text(drama.Title));
		row.append(($("<td>")).text(drama.Author));
		row.append(($("<td>")).text(drama.Type));
		row.append(($("<td>")).text(drama.Date));
		return row;
	};

	that.init = init;
	that.renderList = renderList;

	return that;
};