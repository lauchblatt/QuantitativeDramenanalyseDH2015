SingleDrama.DramaModel = function(){
	var that = {};
	var currentDrama_id = 40;
	var actsInfo = [];
	var scenesInfo = [];
	var firebaseRef = null;

	var init = function(){
		$(that).on("InitFinished", continueInit);
		initInfo("acts_data");
		initInfo("scenes_data");
	};

	var continueInit = function(){
		if(scenesInfo.length > 0 && actsInfo.length > 0){
			calculateNumberOfScenesForAct();
			$(that).trigger("ActsInfoFinished");
			//TODO in Backend besser
			//calculateNumberOfSpeakersForAct();
		}
	};

	var calculateNumberOfScenesForAct = function(){
		for(act = 0; act < scenesInfo.length; act++){
			actsInfo[act].number_of_scenes = scenesInfo[act].length; 
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
				default:
					console.log("Something went wrong.");
			}
			$(that).trigger("InitFinished");
		}, function (errorObject) {
		  console.log("The read failed: " + errorObject.code);
		});
	};

	var getActInfo = function(){
		return actsInfo;
	}

	that.init = init;
	that.getActInfo = getActInfo;

	return that;
};