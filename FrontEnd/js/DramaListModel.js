Search.DramaListModel = function(){
	var that = {};
	var firebaseRef = null;

	var init = function(){
		firebaseRef = new Firebase("https://popping-heat-510.firebaseio.com/");

		// Attach an asynchronous callback to read the data at our posts reference

	};

	var retrieve = function(){
		firebaseRef.orderByChild("Title").on("child_added", function(snapshot) {
			console.log("Data Retrieved");
			console.log(snapshot.val());
		  	$(that).trigger("AllDataRetrieved", [snapshot.val()]);
		}, function (errorObject) {
		  console.log("The read failed: " + errorObject.code);
		});
	}

	that.init = init;
	that.retrieve = retrieve;

	return that;
};