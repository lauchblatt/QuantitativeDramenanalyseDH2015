Search.DramaListView = function(){
	var that = {};

	var init = function(){

	};

	var renderListItem = function(listItem){
		var row = createListItem(listItem);
		$("#table-tbody").append(row);
		$("#loading").css("display","none");
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
	that.renderListItem = renderListItem;

	return that;
};