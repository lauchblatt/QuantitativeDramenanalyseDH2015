DramaAnalyzer.DramaListView = function(){
	var that = {};

	var init = function(){

	};

	var renderList = function(dramaList){
		console.log(dramaList.length);
		for(var i = 0; i < dramaList.length; i++){
			var row = createListItem(dramaList[i]);
			$("#table-tbody").append(row);
		}
		$("#loading").css("display","none");
		$("#drama-table").fadeIn("slow");
	};

	var createListItem = function(drama){
		var row = $("<tr>");
		row.append(($("<td>")).text(drama["Title"]));
		row.append(($("<td>")).text(drama["Author"]));
		row.append(($("<td>")).text(drama["Type"]));
		row.append(($("<td>")).text(drama["Date"]));
		return row;
	};

	that.init = init;
	that.renderList = renderList;

	return that;
};