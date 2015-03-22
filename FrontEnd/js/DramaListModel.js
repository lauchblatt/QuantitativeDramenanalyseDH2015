Search.DramaListModel = function(){
	var that = {};
	var firebaseRef = null;
	//List of Criterions to compare them later
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

		//If not criterion is chosen, show all dramas
		if(jQuery.isEmptyObject(input)){
			retrieveAllData();
			return;
		}

		//If Year is a criterion, save all dramas in the range in rangeList_year
		if('year' in input){
			retrieveDataByRange(input['year'].from, input['year'].to, 'year', rangeList_year);
		}

		//If Number of Speeches is a criterion, save all dramas in the range in rangeList_numberOfSpeeches
		if('number_of_speeches_in_drama' in input){
			retrieveDataByRange(input['number_of_speeches_in_drama'].from, 
				input['number_of_speeches_in_drama'].to, 'number_of_speeches_in_drama', rangeList_numberOfSpeeches);
		}
		console.log("Stop");
		//Compare all criterion-lists to find dramas that fit all criterions
		var dramas = compareRangeLists();
		sendDramas(dramas);

	};

	var sendDramas = function(dramas){
		for(var i = 0; i < dramas.length; i++){
			$(that).trigger("DataRetrieved", [dramas[i]]);
		}
	};

	var retrieveDataByRange = function(from, to, attribute, criterionList){
		$(that).trigger("EmptyTable");
		//Reser Firebase
		firebaseRef = null;
		firebaseRef = new Firebase("https://popping-heat-510.firebaseio.com/drama_data");

		//Check if from and to is set
		if(from === undefined){from = 0};
		if(to === undefined){to = ""};

		//Get all dramas that fit the criterion and save it in the fitting list
		firebaseRef.orderByChild(attribute).startAt(from).endAt(to).on("child_added", function(snapshot) {
			criterionList.push(snapshot.val());
		}, function (errorObject) {
		  console.log("The read failed: " + errorObject.code);
		});
	};

	/*Method to compare criterion-lists and find fitting dramas
	return list of dramas that fit all range-criterions
	*/
	var compareRangeLists = function(){
		console.log("compareRangeLists startet");
		var listsToCompare = [];
		var sameDramas = [];

		//Compare only lists that have more than one element
		if(rangeList_year.length > 0){listsToCompare.push(rangeList_year);}
		if(rangeList_numberOfSpeeches.length > 0){listsToCompare.push(rangeList_numberOfSpeeches);}

		//If only one range-criterion is set, return the dramas
		if(listsToCompare.length == 1){
			sameDramas = listsToCompare[0];
			return sameDramas;
		}

		//Set first list to compare wiht the next
		var list = listsToCompare[0];
		for(var i = 1; i < listsToCompare.length; i++){
			//Compare current list with next list
			//Replace current list with list of dramas that are in both criterion list, and so on
			//until the last list is compared
			list = objectsInListAreSame(list, listsToCompare[i]);
		}
		sameDramas = list;
		return sameDramas;
	};

	//Compares two lists of dramas and return a list of dramas
	//that are in both lists; comparison by id
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

	that.init = init;
	that.retrieveAllData = retrieveAllData;
	that.retrieveDramas = retrieveDramas;

	return that;
};