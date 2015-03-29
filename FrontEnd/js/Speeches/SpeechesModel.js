Speeches.SpeechesModel = function(){
	var that = {};

	var currentDrama_id = 5;
	var scenesInfo = [];
	var dramaInfo = null;

	var init = function(){
		$(that).on("InitFinished", continueInit);
		initInfo("scenes_data");
		initInfo("drama_data");
	};

	var continueInit = function(){
		if(scenesInfo.length > 0  && dramaInfo != null){
			$(that).trigger("InfoFinished");
		}
		
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

	that.init = init;
	that.getDramaInfo = getDramaInfo;
	that.getScenesInfo = getScenesInfo;

	return that;
};