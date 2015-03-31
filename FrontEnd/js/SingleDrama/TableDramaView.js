SingleDrama.TableDramaView = function(){
	var that = {};

	var init = function(){
		$("#dramaTitle").text(localStorage["title"] + " (" + localStorage["year"] + ")");
		$("#dramaAuthor").text(localStorage["author"]);
	};

	var renderTable = function(actInfo, scenesInfo){
		for(var i = 0; i < actInfo.length; i++){
			$("#table-tbody").append(createActItem(actInfo[i]));
			renderScene(scenesInfo[i], (i+1));
		}

	};

	var renderScene = function(sceneInfo, actNumber){
		for(var j = 0; j < sceneInfo.length; j++){
			$("#table-tbody").append(createSceneItem(sceneInfo[j], actNumber));
		}
	};

	var createSceneItem = function(scene, actNumber){
		var row = $("<tr>");
		row.addClass("act-scenes-" + actNumber);
		row.css("display", "none");

		row.append(($("<td>")).text(actNumber + " - " + scene.number_of_scene));
		row.append(($("<td>")).text("-"));
		row.append(($("<td>")).text(scene.appearing_speakers.length));
		row.append(($("<td>")).text(scene.number_of_speeches_in_scene));
		row.append(($("<td>")).text(roundToTwoDecimals(scene.average_length_of_speeches_in_scene)));
		row.append(($("<td>")).text(scene.median_length_of_speeches_in_scene));
		row.append(($("<td>")).text(scene.maximum_length_of_speeches_in_scene));
		row.append(($("<td>")).text(scene.minimum_length_of_speeches_in_scene));

		return row;
	};

	var createActItem = function(act){
		var row = $("<tr>");

		row.append(($("<td>")).text(act.number_of_act));
		row.append(($("<td>")).text(act.number_of_scenes));
		if(act.appearing_speakers !== undefined){
			row.append(($("<td>")).text(act.appearing_speakers.length));
		}else{
			row.append(($("<td>")).text(0));
		}
		row.append(($("<td>")).text(act.number_of_speeches_in_act));
		row.append(($("<td>")).text(roundToTwoDecimals(act.average_length_of_speeches_in_act)));
		row.append(($("<td>")).text(act.median_length_of_speeches_in_act));
		row.append(($("<td>")).text(act.maximum_length_of_speeches_in_act));
		row.append(($("<td>")).text(act.minimum_length_of_speeches_in_act));
		var td = $("<td>");
		td.addClass("unfold-col");
		var $unfoldTd = $("<button>");
		$unfoldTd.addClass('glyphicon');
		$unfoldTd.addClass('glyphicon-menu-down');
		$unfoldTd.addClass("unfold-down");
		$unfoldTd.attr("act-number", act.number_of_act);
		$unfoldTd.on("click", unfold);
		td.append($unfoldTd)
		row.append(td);

		return row;
	};

	var unfold = function(event){
		$unfoldButton = $(event.target);
		var act_number = ($unfoldButton.attr("act-number"));
		if($unfoldButton.hasClass("unfold-down")){
			unfoldScenes(act_number);
			$unfoldButton.removeClass("unfold-down");
			$unfoldButton.removeClass("glyphicon-menu-down");
			$unfoldButton.addClass("unfold-up");
			$unfoldButton.addClass("glyphicon-menu-up");
		} else{
			foldScenes(act_number);
			$unfoldButton.removeClass("unfold-up");
			$unfoldButton.removeClass("glyphicon-menu-up");
			$unfoldButton.addClass("unfold-down");
			$unfoldButton.addClass("glyphicon-menu-down");
		}
	};

	var unfoldScenes = function(actNumber){
		$(".act-scenes-" + actNumber).fadeIn("slow");
	};

	var foldScenes = function(actNumber){
		$(".act-scenes-" + actNumber).fadeOut("slow");
	};

	var roundToTwoDecimals = function(number){
		number = (Math.round(number * 100)/100).toFixed(2);
		return number
	};

	that.init = init;
	that.renderTable = renderTable;

	return that;
};