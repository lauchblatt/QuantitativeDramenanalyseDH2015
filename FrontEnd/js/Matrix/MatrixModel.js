Matrix.MatrixModel = function(){
	var that = {};
	var currentDrama_id = 67;
	//!!! Important for future dramas with for example only one act
	//Only works, if dramaInfo is an Object, scenesInfo, actsInfo, speakersInfo is Array

	/* Globals to work with db-Info */
	var dramaInfo = null;
	var scenesInfo = [];
	var actsInfo = [];
	var speakersInfo = [];
	var firebaseRef = null; 

	/* Fields to calculate and represent matrix */

	var speakersNames = [];
	/* Two Dimensional Arrays are not supported for javascript */
	var matrix = [];

	var init = function(){
		$(that).on("InitFinished", continueInit);
		initInfo("drama_data");
		initInfo("scenes_data");
		initInfo("acts_data");
		initInfo("speakers_data")
	};

	var continueInit = function(){
		if(dramaInfo && scenesInfo.length > 0 && actsInfo.length > 0 && speakersInfo.length > 0){
			console.log("everything is set");
			speakersNames = dramaInfo.speakers;
			calculateMatrix();
			$(that).trigger("ModelInitFinished");
		}
	};

	var calculateMatrix = function(){
		/* Init Two Dimensional Matrix */
		initMatrix();

		for(var i = 0; i < dramaInfo.speakers.length; i++){
			sceneCounter = 0;
			for(var j = 0; j < scenesInfo.length; j++){
				for(var k = 0; k < scenesInfo[j].length; k++){
					/*
					console.log('###');
					console.log("Akt " + j);
					console.log("Scene " + k);
					console.log(dramaInfo.speakers[i]);
					console.log(scenesInfo[j][k].appearing_speakers);
					*/
					
					var speakerAppears = checkIfSpeakerInList(dramaInfo.speakers[i],
						scenesInfo[j][k].appearing_speakers);
					if(speakerAppears){
						matrix[i][sceneCounter] = 1;
					}else{
						matrix[i][sceneCounter] = 0;
					}
					sceneCounter++;
					/*
					console.log(speakerAppears);
					console.log('###');
					*/
				}
			}
		}
		//console.log(matrix);
	};

	var checkIfSpeakerInList = function(speaker, speakerList){
		console.log(speaker);
		console.log(speakerList);
		if(speakerList === undefined){
			return false;
		}
		if (speakerList.indexOf(speaker) > -1) {
    		return true;
		} else {
    		return false;
		}
	};

	var initMatrix = function(){
		matrix = new Array(dramaInfo.speakers.length);
		for(var i = 0; i < dramaInfo.speakers.length; i++){
			matrix[i] = new Array(dramaInfo.number_of_scenes);
		}
	};

	var initInfo = function(name){
		firebaseRef = new Firebase("https://popping-heat-510.firebaseio.com/" + name +"/" + currentDrama_id);
		firebaseRef.on("value", function(snapshot) {
			switch (name) {
				case "scenes_data":
					scenesInfo = snapshot.val();
					break;
				case "acts_data":
					actsInfo = snapshot.val();
					break;
				case "speakers_data":
					speakersInfo = snapshot.val();
					break;
				case "drama_data":
					dramaInfo = snapshot.val();
					break;
				default:
					console.log("Something went wrong.");
			}
			$(that).trigger("InitFinished");
		}, function (errorObject) {
		  console.log("The read failed: " + errorObject.code);
		});
	};

	var getDramaInfo = function(){
		return dramaInfo;
	};

	var getScenesInfo = function(){
		return scenesInfo;
	};

	var getActsInfo = function(){
		return actsInfo;
	};

	var getSpeakersInfo = function(){
		return speakersInfo;
	};

	var getMatrix = function(){
		return matrix;
	};

	that.init = init;
	that.getDramaInfo = getDramaInfo;
	that.getScenesInfo = getScenesInfo;
	that.getActsInfo = getActsInfo;
	that.getSpeakersInfo = getSpeakersInfo;
	that.getMatrix = getMatrix;

	return that;
};