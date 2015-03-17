DramaAnalyzer.DramaModel = function(){
	var that = {};
	var firebaseRef = null;

	var init = function(){
		firebaseRef = new Firebase("https://popping-heat-510.firebaseio.com/");

		// Attach an asynchronous callback to read the data at our posts reference

	};

	var retrieveAllData = function(){
		firebaseRef.on("value", function(snapshot) {
		  $(that).trigger("AllDataRetrieved", [snapshot.val()]);
		}, function (errorObject) {
		  console.log("The read failed: " + errorObject.code);
		});
	}

	that.init = init;
	that.retrieveAllData = retrieveAllData;

	return that;
};