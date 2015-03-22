Search.DramaListModel = function(){
	var that = {};
	var firebaseRef = null;

	var init = function(){
		firebaseRef = new Firebase("https://popping-heat-510.firebaseio.com/drama_data");
	};

	var retrieveAllData = function(){
		firebaseRef.on("child_added", function(snapshot) {
			$(that).trigger("DataRetrieved", [snapshot.val()]);
		}, function (errorObject) {
		  console.log("The read failed: " + errorObject.code);
		});
	}

	var retrieveDramas = function(input){
		var date = {};
		date.from = 1500;
		date.to = 1600;
		input['date.when'] = date;

		if(jQuery.isEmptyObject(input)){
			retrieveAllData();
			return;
		}
		if('date.when' in input){
			retrieveDataByRange(input['date.when'])
		}
	};

	var retrieveDataByRange = function(range){
	};

	that.init = init;
	that.retrieveAllData = retrieveAllData;
	that.retrieveDramas = retrieveDramas;

	return that;
};