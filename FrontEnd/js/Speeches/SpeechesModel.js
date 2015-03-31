Speeches.SpeechesModel = function(){
	var that = {};

	var currentDrama_id = 5;
	var scenesInfo = [];
	var dramaInfo = null;
	var distribution = {};

	var init = function(){
		currentDrama_id = localStorage["drama_id"];
		$(that).on("InitFinished", continueInit);
		initInfo("scenes_data");
		initInfo("drama_data");
	};

	var continueInit = function(){
		if(scenesInfo.length > 0  && dramaInfo != null){
			calculateDistribution();
			$(that).trigger("InfoFinished");
		}
		
	};

	var calculateDistribution = function(){
		for(act = 0; act < scenesInfo.length; act++){
			for(scene = 0; scene < scenesInfo[act].length; scene++){
				if(scenesInfo[act][scene].speeches !== undefined){
					for(speech = 0; speech < scenesInfo[act][scene].speeches.length; speech++){
							var currentspeechLength = scenesInfo[act][scene].speeches[speech].length;
							if(distribution[currentspeechLength] === undefined){
								distribution[currentspeechLength] = 1;
							}else{
								distribution[currentspeechLength] = distribution[currentspeechLength] + 1;
							}
					}	
				}
			}
		}
		console.log(distribution);
	};

	var initInfo = function(name){
		firebaseRef = new Firebase("https://katharsis.firebaseio.com/" + name +"/" + currentDrama_id);
		firebaseRef.on("value", function(snapshot) {
			switch (name) {
				case "scenes_data":
					scenesInfo = snapshot.val();
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

	var getDistribution = function(){
		return distribution;
	};

	that.init = init;
	that.getDramaInfo = getDramaInfo;
	that.getScenesInfo = getScenesInfo;
	that.getDistribution = getDistribution;

	return that;
};