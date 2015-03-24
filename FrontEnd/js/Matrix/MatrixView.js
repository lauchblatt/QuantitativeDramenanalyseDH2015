Matrix.MatrixView = function(){
	var that = {};

	var init = function(dramaInfo, actsInfo, scenesInfo, speakersInfo, matrix){
		renderTitle(dramaInfo);
		renderheadline(scenesInfo);
		renderSpeakerColumn(dramaInfo);
		fillTable(dramaInfo, scenesInfo);
		fillCellsWithConfMatrix(matrix);
		initTooltipsForSpeakers(speakersInfo);
		initTooltipsForActs(actsInfo);
		$("#confMatrix").fadeIn("slow");
	};

	var initTooltipsForActs = function(actsInfo){
		for(var i = 0;  i < actsInfo.length; i++){
			var $content = getActTooltip(actsInfo[i]);
			var actId = "act_" + i + "_id";
			console.log($content);
			console.log(actId);
			$("#"+actId).tooltipster({
			content: $content,
			position: "bottom",
			trigger: 'click'
			});
		}
	};

	var getActTooltip = function(act){
		var $content = $("<div></div>");
		$content.append(buildAttribute(("Akt"), act.number_of_act));
		$content.append(buildAttribute("Replikenanzahl", act.number_of_speeches_in_act));
		$content.append(buildAttribute("Mittel Replikenlänge",
			roundToTwoDecimals(act.average_length_of_speeches_in_act)));
		$content.append(buildAttribute("Median Replikenlänge", 
			act.median_length_of_speeches_in_act));
		$content.append(buildAttribute("Maximum Replikenlänge", 
			act.maximum_length_of_speeches_in_act));
		$content.append(buildAttribute("Minimum Replikenlänge", 
			act.minimum_length_of_speeches_in_act));
		return $content;
	};

	var initTooltipsForSpeakers = function(speakersInfo){
		for(var i = 0; i < speakersInfo.length; i++){
			var $content = getSpeakerTooltip(speakersInfo[i]);
			var speakerId = "speaker_" + i;
			$("#"+speakerId).tooltipster({
			content: $content,
			position: "right",
			trigger: 'click'
			});
		}
	};

	var getSpeakerTooltip = function(speaker){
		var $content = $("<div></div>");
		$content.append(buildAttribute("Name", speaker.name));
		$content.append(buildAttribute("Replikenanzahl", speaker.number_of_speakers_speeches));
		$content.append(buildAttribute("Mittel Replikenlänge",
			roundToTwoDecimals(speaker.average_length_of_speakers_speeches)));
		$content.append(buildAttribute("Median Replikenlänge", 
			speaker.median_length_of_speakers_speeches));
		$content.append(buildAttribute("Maximum Replikenlänge", 
			speaker.maximum_length_of_speakers_speeches));
		$content.append(buildAttribute("Minimum Replikenlänge", 
			speaker.minimum_length_of_speakers_speeches));
		return $content;
	};

	var buildAttribute = function(name, attribute){
		var $div = $("<div></div>");
		$div.text(name + ": " + attribute);
		return $div;
	};

	var renderTitle = function(dramaInfo){
		$("#title").text(dramaInfo["title"] + " von " + dramaInfo.author);
		$test = $("<div></div>");
		$test.addClass("test");
		$test.text("Hello World");
		$("#title").tooltipster({
			content: $test,
			trigger: 'click'
		});
	};

	var fillCellsWithConfMatrix = function(matrix){
		for(var i = 0; i < matrix.length; i++){
			for(var j = 0; j < matrix[i].length; j++){
				var matrix_id = "matrix_" + i + "_" + j;
				$("#" + matrix_id).text(matrix[i][j]);
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
				var act = "'act_" + i + "'";
				var scene = "'scene_" + i + "_" + j +"'";
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

	that.init = init;

	return that;
};