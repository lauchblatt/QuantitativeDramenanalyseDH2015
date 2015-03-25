SingleDrama.TableDramaView = function(){
	var that = {};

	var init = function(){

	};

	var renderAct = function(actInfo){
		console.log(actInfo);
		for(var i = 0; i < actInfo.length; i++){
			$("#table-tbody").append(createListItem(actInfo[i]));
		}

	};

	var createListItem = function(act){
		var row = $("<tr>");

		row.append(($("<td>")).text(act.number_of_act));
		row.append(($("<td>")).text(act.number_of_scenes));
		//TODO
		row.append(($("<td>")).text(0));
		row.append(($("<td>")).text(act.number_of_speeches_in_act));
		row.append(($("<td>")).text(roundToTwoDecimals(act.average_length_of_speeches_in_act)));
		row.append(($("<td>")).text(act.median_length_of_speeches_in_act));
		row.append(($("<td>")).text(act.maximum_length_of_speeches_in_act));
		row.append(($("<td>")).text(act.minimum_length_of_speeches_in_act));

		return row;
	};

	var roundToTwoDecimals = function(number){
		number = (Math.round(number * 100)/100).toFixed(2);
		return number
	};

	that.init = init;
	that.renderAct = renderAct;

	return that;
};