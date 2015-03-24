Matrix.MatrixModel = function(){
	var that = {};
	var currentDrama_id = 1;
	//!!! Important for future dramas with for example only one act
	//Only works, if dramaInfo is an Object, scenesInfo, actsInfo, speakersInfo is Array
	var dramaInfo = null;
	var scenesInfo = [];
	var actsInfo = [];
	var speakersInfo = [];
	var firebaseRef = null; 

	var init = function(){
		$(that).on("InitFinished", continueInit);
		initInfo("drama_data");
		initInfo("scenes_data");
		initInfo("acts_data");
		initInfo("speakers_data")
	};

	var continueInit = function(){
		console.log(dramaInfo);
		console.log(scenesInfo);
		console.log(actsInfo);
		console.log(speakersInfo);
		if(dramaInfo && scenesInfo.length > 0 && actsInfo.length > 0 && speakersInfo.length > 0){
			console.log("everything is set");
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

	that.init = init;

	return that;
};