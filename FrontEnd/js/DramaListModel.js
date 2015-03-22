Search.DramaListModel = function(){
	var that = {};
	var firebaseRef = null;
	var rangeList_year = [];
	var rangeList_numberOfSpeeches = [];

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
		// Reset all Criterions-Lists
		rangeList_year = [];
		rangeList_numberOfSpeeches = [];

		if(jQuery.isEmptyObject(input)){
			retrieveAllData();
			return;
		}

		if('year' in input){
			retrieveDataByRange(input['year'].from, input['year'].to, 'year', rangeList_year);
		}

		if('number_of_speeches_in_drama' in input){
			retrieveDataByRange(input['number_of_speeches_in_drama'].from, 
				input['number_of_speeches_in_drama'].to, 'number_of_speeches_in_drama', rangeList_numberOfSpeeches);
		}
		console.log("Stop");
		console.log(compareRangeLists());

	};

	var retrieveDataByRange = function(from, to, attribute, criterionList){
		$(that).trigger("EmptyTable");
		firebaseRef = null;
		firebaseRef = new Firebase("https://popping-heat-510.firebaseio.com/drama_data");
		if(from === undefined){from = 0};
		if(to === undefined){to = ""};
		firebaseRef.orderByChild(attribute).startAt(from).endAt(to).on("child_added", function(snapshot) {
			criterionList.push(snapshot.val());
		}, function (errorObject) {
		  console.log("The read failed: " + errorObject.code);
		});
	};

	var compareRangeLists = function(){
		console.log("compareRangeLists startet");
		var listsToCompare = [];
		var sameDramas = [];
		if(rangeList_year.length > 0){listsToCompare.push(rangeList_year);}
		if(rangeList_numberOfSpeeches.length > 0){listsToCompare.push(rangeList_numberOfSpeeches);}

		if(listsToCompare.length == 1){
			sameDramas = listsToCompare[0];
			return sameDramas;
		}
		var list = listsToCompare[0];
		for(var i = 1; i < listsToCompare.length; i++){
			console.log("Listen zum Vergleich");
			console.log(list);
			console.log(listsToCompare[i]);
			list = objectsInListAreSame(list, listsToCompare[i]);
		}
		sameDramas = list;
		return sameDramas;
	};

	var objectsInListAreSame = function(list1, list2){
		var sameObjects = [];
		for(var i = 0; i < list1.length; i++){
			for(var j = 0; j < list2.length; j++){
				if(list1[i]['id'] == list2[j]['id']){
					sameObjects.push(list1[i]);
				}
			}
		}
		return sameObjects;
	};

   var objectsAreSame = function(x, y) {
	   var objectsAreSame = true;
	   for(var propertyName in x) {
	      if(x[propertyName] !== y[propertyName]) {
	         objectsAreSame = false;
	         break;
	      }
	   }
	   return objectsAreSame;
	};

	that.init = init;
	that.retrieveAllData = retrieveAllData;
	that.retrieveDramas = retrieveDramas;

	return that;
};