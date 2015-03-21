Search.DramaListModel = function(){
	var that = {};
	var firebaseRef = null;

	var init = function(){
		firebaseRef = new Firebase("https://popping-heat-510.firebaseio.com/");

		// Attach an asynchronous callback to read the data at our posts reference

	};

	var retrieveAllData = function(){
		firebaseRef.orderByChild('Number of Replicas in Drama').startAt(1000).endAt(2000).on("child_added", function(snapshot) {
			console.log("Data Retrieved");
			console.log(snapshot.val());
			console.log(snapshot.val().Title + " has " + snapshot.val()["Number of Replicas in Drama"] + " Speeches in Drama.");
		  $(that).trigger("AllDataRetrieved", [snapshot.val()]);
		}, function (errorObject) {
		  console.log("The read failed: " + errorObject.code);
		});
	}

	that.init = init;
	that.retrieveAllData = retrieveAllData;

	return that;
};