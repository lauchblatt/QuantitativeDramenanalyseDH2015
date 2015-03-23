Matrix.MatrixModel = function(){
	var that = {};
	var currentDrama_id = 1;
	var scenesInfo = [];
	var actsInfo = [];
	var speakersInfo = [];
	var firebaseRef = null; 

	var init = function(){
		$(that).on("InitFinished", continueInit);
		scenesInfo = initInfo("scenes_data");
	};

	var continueInit = function(){
		console.log(scenesInfo);
	};

	var initInfo = function(name){
		firebaseRef = new Firebase("https://popping-heat-510.firebaseio.com/" + name +"/" + currentDrama_id);
		firebaseRef.on("value", function(snapshot) {
			scenesInfo = snapshot.val();
			$(that).trigger("InitFinished");
		}, function (errorObject) {
		  console.log("The read failed: " + errorObject.code);
		});
	};

	that.init = init;

	return that;
};