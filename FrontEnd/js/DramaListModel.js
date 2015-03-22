Search.DramaListModel = function(){
	var that = {};
	var firebaseRef = null;

	var init = function(){
		firebaseRef = new Firebase("https://popping-heat-510.firebaseio.com/drama_data");
	};

	var retrieveAllData = function(){
		firebaseRef.once("value", function(snapshot) {
			$(that).trigger("DataRetrieved", [snapshot.val()]);
		}, function (errorObject) {
		  console.log("The read failed: " + errorObject.code);
		});
	}

	var retrieveDramas = function(input){
		/*
		var range = {};
		range.from = 1750;
		range.to = 1755;
		input['year'] = range;
		console.log(input['year']);
		*/

		if(jQuery.isEmptyObject(input)){
			retrieveAllData();
			return;
		}

		if('year' in input){
			retrieveDataByRange(input['year'].from, input['year'].to, 'year')
		}
	};

	var retrieveDataByRange = function(from, to, attribute){
		firebaseRef.orderByChild(attribute).startAt(from).endAt(to).on("value", function(snapshot) {
			$(that).trigger("DataRetrieved", [snapshot.val()]);
		}, function (errorObject) {
		  console.log("The read failed: " + errorObject.code);
		});
	};

	that.init = init;
	that.retrieveAllData = retrieveAllData;
	that.retrieveDramas = retrieveDramas;

	return that;
};