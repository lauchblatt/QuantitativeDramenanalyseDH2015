Search.DramaListModel = function(){
	var that = {};
	var firebaseRef = null;

	var init = function(){
		firebaseRef = null;
		firebaseRef = new Firebase("https://popping-heat-510.firebaseio.com/drama_data");
	};

	var retrieveAllData = function(){
		$(that).trigger("EmptyTable");
		firebaseRef.on("child_added", function(snapshot) {
			$(that).trigger("DataRetrieved", [snapshot.val()]);
		}, function (errorObject) {
		  console.log("The read failed: " + errorObject.code);
		});
	}

	var retrieveDramas = function(input){

		if(jQuery.isEmptyObject(input)){
			retrieveAllData();
			return;
		}

		if('year' in input){
			retrieveDataByRange(input['year'].from, input['year'].to, 'year');
		}
		
		if('number_of_speeches_in_drama' in input){
			retrieveDataByRange(input['number_of_speeches_in_drama'].from, 
				input['number_of_speeches_in_drama'].to, 'number_of_speeches_in_drama');
		}
	};

	var retrieveDataByRange = function(from, to, attribute){
		$(that).trigger("EmptyTable");
		firebaseRef = null;
		firebaseRef = new Firebase("https://popping-heat-510.firebaseio.com/drama_data");
		if(from === undefined){from = 0};
		if(to === undefined){to = ""};
		firebaseRef.orderByChild(attribute).startAt(from).endAt(to).on("child_added", function(snapshot) {
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