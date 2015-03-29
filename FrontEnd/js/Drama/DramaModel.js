Drama.DramaModel = function(){
	var that = {};
	var currentDrama_id = 35;
	var dramaInfo = null;

	var init = function(){
		initInfo("drama_data");
	};

	var initInfo = function(name){
		firebaseRef = new Firebase("https://popping-heat-510.firebaseio.com/" + name +"/" + currentDrama_id);
		firebaseRef.on("value", function(snapshot) {
		dramaInfo = snapshot.val();
		$(that).trigger("InitFinished");
		}, function (errorObject) {
		  console.log("The read failed: " + errorObject.code);
		});
	};

	var getDramaInfo = function(){
		return dramaInfo;
	};

	that.init = init;
	that.getDramaInfo = getDramaInfo;

	return that;
};