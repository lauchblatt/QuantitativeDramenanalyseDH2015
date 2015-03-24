Matrix.MatrixView = function(){
	var that = {};

	var init = function(dramaInfo, actsInfo, scenesInfo, speakersInfo, matrix){
		renderheadline(scenesInfo);
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
				$th = $("<th class=" + act +"id=" + scene + "</th>");
				$th.text((j+1) + ". Szene");
				$headlineScene.append($th);
			}
		}

	};

	that.init = init;

	return that;
};