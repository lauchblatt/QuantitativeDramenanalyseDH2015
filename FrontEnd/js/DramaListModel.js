Search.DramaListModel = function(){
	var that = {};
	var firebaseRef = null;

	var init = function(){
		firebaseRef = new Firebase("https://popping-heat-510.firebaseio.com/drama_data");

		// Attach an asynchronous callback to read the data at our posts reference

	};

	var retrieve = function(){
		firebaseRef.on("child_added", function(snapshot) {
			$(that).trigger("DataRetrieved", [snapshot.val()]);
		}, function (errorObject) {
		  console.log("The read failed: " + errorObject.code);
		});
	}

	that.init = init;
	that.retrieve = retrieve;

	return that;
};