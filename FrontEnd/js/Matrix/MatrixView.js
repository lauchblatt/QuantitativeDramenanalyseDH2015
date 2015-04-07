Matrix.MatrixView = function(){
	var that = {};
	var currentDrama_id = 0;

	var init = function(dramaInfo, actsInfo, scenesInfo, speakersInfo, matrix){
		$("#dramaTitle").text(dramaInfo.title + " (" + dramaInfo.year + ")");
		$("#dramaAuthor").text(dramaInfo.author);
		renderheadline(scenesInfo);
		renderSpeakerColumn(dramaInfo);
		fillTable(dramaInfo, scenesInfo);
		fillCellsWithConfMatrix(matrix);
		initTooltipsForSpeakers(speakersInfo);
		initTooltipsForActs(actsInfo);
		initTooltipsForScenes(scenesInfo);
		initTooltipsForTitleHeader(dramaInfo);
		initId();
		initLinks();
		$(".container").fadeIn("slow");
	};

	var initTooltipsForTitleHeader = function(dramaInfo){
		var $titleHeader = $("#title-header");
		$titleHeader.text(dramaInfo.title);
		var $content = getDramaTooltip(dramaInfo);
		$titleHeader.tooltipster({
					content: $content,
					position: "right",
					trigger: 'hover'
				});
	};

	var getCellTooltip = function(cellObject){
		var $content = $("<div>");
		var strings = ["Sprecher:", "Replikenzahl:", "Mittel Replikenlänge:", "Median Replikenlänge:",
		"Maximum Replikenlänge:", "Minimum Replikenlänge:"];
		var data = [cellObject.speaker, cellObject.number_of_speeches, cellObject.average,
		cellObject.median, cellObject.max, cellObject.min];

		var $leftColumn = getColumn(strings, "insideLeft");
		var $rightColumn = getColumn(data, "insideRight");
		$content.append($leftColumn);
		$content.append($rightColumn);

		return $content;
	};

	var getDramaTooltip = function(drama){
		var $content = $("<div></div>");
		var strings = ["Titel:","Autor:", "Jahr:", "Typ:", "Sprecher:", "Konfigurationsdichte:",
		"Replikenanzahl:","Mittel Replikenlänge:", "Median Replikenlänge:",
		"Maximum Replikenlänge:", "Minimum Replikenlänge:"];
		var data = [drama.title, drama.author, drama.year, drama.type, drama.speakers.length,
		roundToTwoDecimals(drama.configuration_density),
		drama.number_of_speeches_in_drama, 
		roundToTwoDecimals(drama.average_length_of_speeches_in_drama),
		drama.median_length_of_speeches_in_drama, drama.maximum_length_of_speeches_in_drama, 
		drama.minimum_length_of_speeches_in_drama];

		var $leftColumn = getColumn(strings, "insideLeft");
		var $rightColumn = getColumn(data, "insideRight");
		$content.append($leftColumn);
		$content.append($rightColumn);

		return $content;
	};

	var initTooltipsForScenes = function(scenesInfo){
		for(var act = 0; act < scenesInfo.length; act++){
			for(var scene = 0; scene < scenesInfo[act].length; scene++){
				var $content = getSceneTooltip(scenesInfo[act][scene]);
				var sceneId = "scene_" + act + "_" + scene;
				$("#"+sceneId).tooltipster({
					content: $content,
					position: "bottom",
					trigger: 'hover'
				});
			}
		}
	};

	var getSceneTooltip = function(scene){
		var $content = $("<div></div>");
		var strings = ["Szene:", "Replikenanzahl:", "Mittel Replikenlänge:",
			"Median Replikenlänge:", "Maximum Replikenlänge:", "Minimum Replikenlänge:"];
		var data = [scene.number_of_scene, scene.number_of_speeches_in_scene, 
		roundToTwoDecimals(scene.average_length_of_speeches_in_scene), 
		scene.median_length_of_speeches_in_scene, scene.maximum_length_of_speeches_in_scene, 
		scene.minimum_length_of_speeches_in_scene]
		var $leftColumn = getColumn(strings, "insideLeft");
		var $rightColumn = getColumn(data, "insideRight");
		$content.append($leftColumn);
		$content.append($rightColumn);
		return $content;
	};

	var initTooltipsForActs = function(actsInfo){
		for(var i = 0;  i < actsInfo.length; i++){
			var $content = getActTooltip(actsInfo[i]);
			var actId = "act_" + i + "_id";
			$("#"+actId).tooltipster({
			content: $content,
			position: "bottom",
			trigger: 'hover'
			});
		}
	};

	var getActTooltip = function(act){
		var $content = $("<div></div>");

		var leftColumn = getColumn(["Akt:", "Replikenanzahl:", "Mittel Replikenlänge:",
			"Median Replikenlänge:", "Maximum Replikenlänge:", "Minimum Replikenlänge:"], "insideLeft");
		var data = [act.number_of_act, act.number_of_speeches_in_act, 
		roundToTwoDecimals(act.average_length_of_speeches_in_act), 
		act.median_length_of_speeches_in_act, act.maximum_length_of_speeches_in_act, 
		act.minimum_length_of_speeches_in_act];
		var rightColumn = getColumn(data, "insideRight");

		$content.append(leftColumn);
		$content.append(rightColumn);
		return $content;

	};

	var getColumn = function(strings, sideClass){
		var $column = $("<div>");
		$column.addClass(sideClass);
		for(var i = 0; i < strings.length; i++){
			var br = $("<br>");
			var span = $("<span>");
			span.text(strings[i]);
			$column.append(span);
			$column.append(br);
		}
		return $column;
	};

	var initTooltipsForSpeakers = function(speakersInfo){
		for(var i = 0; i < speakersInfo.length; i++){
			var $content = getSpeakerTooltip(speakersInfo[i]);
			var speakerId = "speaker_" + i;
			$("#"+speakerId).tooltipster({
			content: $content,
			position: "right",
			trigger: 'hover'
			});
		}
	};

	var getSpeakerTooltip = function(speaker){
		var $content = $("<div></div>");
		var strings = ["Name", "Replikenanzahl", "Mittel Replikenlänge",
		"Median Replikenlänge","Maximum Replikenlänge", "Minimum Replikenlänge"];
		var data = [];
		if(speaker.number_of_speakers_speeches != 0){
			data = [speaker.name, speaker.number_of_speakers_speeches,
			roundToTwoDecimals(speaker.average_length_of_speakers_speeches), 
			speaker.median_length_of_speakers_speeches,
			speaker.maximum_length_of_speakers_speeches,
			speaker.minimum_length_of_speakers_speeches];
		}else{
			data = [speaker.name, speaker.number_of_speakers_speeches,0, 0, 0, 0];
		}
		

		var $leftColumn = getColumn(strings, "insideLeft");
		var $rightColumn = getColumn(data, "insideRight");
		$content.append($leftColumn);
		$content.append($rightColumn);

		return $content;
	};

	var buildAttribute = function(name, attribute){
		$div = $("<div>");
		$div.text(name + ": " + attribute);
		return $div;
	};

	var fillCellsWithConfMatrix = function(matrix){
		for(var i = 0; i < matrix.length; i++){
			for(var j = 0; j < matrix[i].length; j++){
				var matrix_id = "matrix_" + i + "_" + j;
				if(matrix[i][j].matrix_number == 1){
					$("#" + matrix_id).addClass("filled");
					$content = getCellTooltip(matrix[i][j]);
					$("#" + matrix_id).tooltipster({
						content: $content,
						position: "top",
						trigger: 'hover'
						});
				}else{
					$("#" + matrix_id).text("");
					$("#" + matrix_id).attr("title", matrix[i][j].name);
				}
				
			}
		}
	};

	var fillTable = function(dramaInfo, scenesInfo){
		for(var speaker = 0; speaker < dramaInfo.speakers.length; speaker++){
			var $row = $("#speaker_" + speaker + "_row");
			var numberOfSceneAbsolute = 0;
			for(var act = 0; act < scenesInfo.length; act++){
				var actClass = "act_" + act;
				for(var scene = 0; scene < scenesInfo[act].length; scene++){
					var matrix_id = "matrix_" + speaker + "_" + numberOfSceneAbsolute;
					$td = $("<td></td>");
					$td.addClass(actClass);
					$td.attr("id", matrix_id);
					$row.append($td);
					numberOfSceneAbsolute++;
				}
			}
		}
	};

	var renderSpeakerColumn = function(dramaInfo){
		$tableBody = $("#table-body");
		for(i = 0; i < dramaInfo.speakers.length; i++){
			var $row = $("<tr></tr>");
			$row.attr("id", "speaker_" + i + "_row");
			var $th = $("<th></th>");
			$th.attr("id","speaker_" + i);
			var name = dramaInfo.speakers[i];
			$th.text(name);
			$row.append($th);
			$tableBody.append($row);
		}
	};

	var renderheadline = function(scenesInfo){
		$headlineAct  = $("#acts_headline");
		$headlineScene = $("#scenes_headline");
		
		for(var i = 0; i < scenesInfo.length; i++){
			var lengthOfAct = scenesInfo[i].length;
			
			var $th = ($("<th class='act_" + i + "' colspan='" + lengthOfAct +"'></th>"));
			var id = "act_" + i + "_id";
			$th.attr("id", id);
			$th.text((i+1) + ". Akt");
			$headlineAct.append($th);
		}

		for(var i = 0; i < scenesInfo.length; i++){
			for(var j = 0; j < scenesInfo[i].length; j++){
				var act = "act_" + i;
				var scene = "scene_" + i + "_" + j;
				var $th = $("<th></th>");
				$th.addClass(act);
				$th.attr("id", scene);
				$th.text((j+1) + ". Szene");
				$headlineScene.append($th);
			}
		}

	};

	var roundToTwoDecimals = function(number){
		number = (Math.round(number * 100)/100).toFixed(2);
		return number
	};

	var initId = function(){
		var params = window.location.search
		console.log("hello World");
		console.log(params);
		currentDrama_id = (params.substring(params.indexOf("=") + 1));
	};

	var initLinks = function(){
		$("#link-overall").attr("href", "drama.html?drama_id=" + currentDrama_id);
		$("#link-matrix").attr("href", "matrix.html?drama_id=" + currentDrama_id);
		$("#link-drama").attr("href", "singledrama.html?drama_id=" + currentDrama_id);
		$("#link-drama-actSceneAnalysis").attr("href", "singledrama.html?drama_id=" + currentDrama_id + "#act-scene-table");
		$("#link-drama-actStatistic").attr("href", "singledrama.html?drama_id=" + currentDrama_id + "#act-statistic");
		$("#link-drama-sceneStatistic").attr("href", "singledrama.html?drama_id=" + currentDrama_id + "#scene-statistic");
		$("#link-speakers").attr("href", "speakers.html?drama_id=" + currentDrama_id);
		$("#link-speaker-table").attr("href", "speakers.html?drama_id=" + currentDrama_id + "#speaker-table");
		$("#link-speeches-dominance").attr("href", "speakers.html?drama_id=" + currentDrama_id  + "#speeches-dominance");
		$("#link-speaker-statistic").attr("href", "speakers.html?drama_id=" + currentDrama_id  + "#speaker-statistic");
		$("#link-speaker-relations").attr("href", "speakers.html?drama_id=" + currentDrama_id  + "#speaker-relations");
		$("#link-speeches").attr("href", "speeches.html?drama_id=" + currentDrama_id);
		$("#link-histogram").attr("href", "speeches.html?drama_id=" + currentDrama_id + "#histogram");
		$("#link-curve-diagram").attr("href", "speeches.html?drama_id=" + currentDrama_id + "#curve-diagram");
	};

	that.init = init;

	return that;
};