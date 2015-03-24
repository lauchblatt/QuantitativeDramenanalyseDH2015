Search.DramaListModel = function(){
	var that = {};
	var firebaseRef = null;
	//List of Criterions to compare them later
	var rangeList_year = [];
	var rangeList_numberOfSpeeches = [];

	//List of current dramas
	var dramas = [];

	var init = function(){
		firebaseRef = null;
		firebaseRef = new Firebase("https://popping-heat-510.firebaseio.com/drama_data");

		$(that).on("AllDramasRetrieved", filterAllDataByTitleAndAuthor);
	};

	var retrieveAllData = function(input){
		firebaseRef = null;
		firebaseRef = new Firebase("https://popping-heat-510.firebaseio.com/drama_data");

		$(that).trigger("EmptyTable");
		firebaseRef.orderByChild('author').on("value", function(snapshot) {
			dramas= snapshot.val();
			$(that).trigger("AllDramasRetrieved", [input]);
		}, function (errorObject) {
		  console.log("The read failed: " + errorObject.code);
		});
	};

	var filterAllDataByTitleAndAuthor = function(event, input){
		//If Title is criterion, filter the dramas by title
		if('title' in input){
			dramas = filterListByWord('title', input['title']);
		}

		//If Author is criterion, filter the dramas by author
		if('author' in input){
			dramas = filterListByWord('author', input['author']);
		}

		sendDramas(dramas);
	};

	var retrieveDramas = function(input){
		// Reset all Criterions-Lists, and the list for the result
		dramas = [];
		rangeList_year = [];
		rangeList_numberOfSpeeches = [];

		//If no criterion is chosen, show all dramas, but filter them
		if(!('number_of_speeches_in_drama' in input) && !('year' in input)){
			retrieveAllData(input);
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

		//Compare all criterion-lists to find dramas that fit all criterions
		var rangeDramas = compareRangeLists();
		if(rangeDramas !== undefined){	
			dramas = rangeDramas;
		}
		//If Title is criterion, filter the dramas by title
		if('title' in input){
			dramas = filterListByWord('title', input['title']);
		}

		//If Author is criterion, filter the dramas by author
		if('author' in input){
			dramas = filterListByWord('author', input['author']);
		}

		sendDramas(dramas);

	};

	var filterListByWord = function(attribute, word){
		var word = word.toLowerCase();
		var split = word.split(" ");
		filteredDramaList = [];
		for(var i = 0; i < dramas.length; i++){
			for(var j = 0; j < split.length; j++){
				if(dramas[i][attribute].toLowerCase().indexOf(split[j]) > -1){
				filteredDramaList.push(dramas[i]);
				break;
				}
			}
		}
		return filteredDramaList;
	};

	var sendDramas = function(dramas){
		console.log("sendDramas");
		for(var i = 0; i < dramas.length; i++){
			$(that).trigger("DataRetrieved", [dramas[i]]);
		}
		$("table").css("display", "none");
		$("table").fadeIn(1000);
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