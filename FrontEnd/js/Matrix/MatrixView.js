Matrix.MatrixView = function(){
	var that = {};

	var init = function(dramaInfo, actsInfo, scenesInfo, speakersInfo, matrix){
		renderheadline(scenesInfo);
		renderSpeakerColumn(dramaInfo);
		fillTable(dramaInfo, scenesInfo);
		fillCellsWithConfMatrix(matrix);
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

	that.init = init;

	return that;
};