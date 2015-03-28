MultipleDramas.MultipleDramasModel = function(){
	var that = {};
	var dramaInfo = [];
	var firebaseRef = null;
	var chosenDramasIds = [];
	var chosenDramas = [];
	var authorList = [];
	var categoryList = [];

	var init = function(){
		for(var i = 0; i < 103; i++){
			chosenDramasIds.push(i);
		}
		$(that).on("InitFinished", continueInit);
		initInfo("drama_data");
	};

	var continueInit = function(){
		if(dramaInfo != null){
			setChosenDramas();
			roundValues();
			setAuthorList();
			setCategoryList();
			$(that).trigger("InfoFinished");
		}
	};

	var roundValues = function(){
		for(var i = 0; i < chosenDramas.length; i++){
			chosenDramas[i].configuration_density = roundToTwoDecimals(chosenDramas[i].configuration_density);
			chosenDramas[i].average_length_of_speeches_in_drama = roundToTwoDecimals(chosenDramas[i].average_length_of_speeches_in_drama);
		}
	};

	var setCategoryList = function(){
		var categories = [];
		for(var i = 0; i < chosenDramas.length; i++){
			if($.inArray(chosenDramas[i].type, categories) === -1){
				if(chosenDramas[i].type !== undefined){
					categories.push(chosenDramas[i].type);
				}
			}
		}

		for(var i = 0; i < categories.length; i++){
			var dramaObjects = $.grep(chosenDramas, function(e){ return e.type == categories[i]; });
			var categoryObject = generateCategoryObject(dramaObjects);
			categoryList.push(categoryObject);
		}
	};

	var getCategoryList = function(){
		return categoryList;
	};

	var generateCategoryObject = function(dramaObjects){
		var categoryObj = {};

		categoryObj.type = dramaObjects[0].type;
		var average_number_of_scenes = 0;
		var average_number_of_speeches = 0;
		var average_number_of_speakers = 0;
		var average_configuration_density = 0;
		var average_average_length_of_speeches = 0;
		var average_median_length_of_speeches = 0;
		var average_maximum_length_of_speeches = 0;
		var average_minimum_length_of_speeches = 0;
		var titles = [];

		for(var i = 0; i < dramaObjects.length; i++){
			average_number_of_scenes += dramaObjects[i].number_of_scenes;
			average_number_of_speeches += dramaObjects[i].number_of_speeches_in_drama;
			average_number_of_speakers += dramaObjects[i].speakers.length;
			average_configuration_density += dramaObjects[i].configuration_density;
			average_average_length_of_speeches += dramaObjects[i].average_length_of_speeches_in_drama;
			average_median_length_of_speeches += dramaObjects[i].median_length_of_speeches_in_drama;
			average_maximum_length_of_speeches += dramaObjects[i].maximum_length_of_speeches_in_drama;
			average_minimum_length_of_speeches += dramaObjects[i].minimum_length_of_speeches_in_drama;
			titles.push(dramaObjects[i].title);
		}

		categoryObj.average_number_of_scenes = roundToTwoDecimals(average_number_of_scenes/dramaObjects.length);
		categoryObj.average_number_of_speeches = roundToTwoDecimals(average_number_of_speeches/dramaObjects.length);
		categoryObj.average_number_of_speakers = roundToTwoDecimals(average_number_of_speakers/dramaObjects.length);
		categoryObj.average_configuration_density = roundToTwoDecimals(average_configuration_density/dramaObjects.length);
		categoryObj.average_average_length_of_speeches = roundToTwoDecimals(average_average_length_of_speeches/dramaObjects.length);
		categoryObj.average_median_length_of_speeches = roundToTwoDecimals(average_median_length_of_speeches/dramaObjects.length);
		categoryObj.average_maximum_length_of_speeches = roundToTwoDecimals(average_maximum_length_of_speeches/dramaObjects.length);
		categoryObj.average_minimum_length_of_speeches = roundToTwoDecimals(average_minimum_length_of_speeches/dramaObjects.length);
		categoryObj.titles = titles;

		return categoryObj;

	};

	var setAuthorList = function(){
		var authors = [];
		for(var i = 0; i < chosenDramas.length; i++){
			if($.inArray(chosenDramas[i].author, authors) === -1){
				authors.push(chosenDramas[i].author);
			}
		}

		for(var i = 0; i < authors.length; i++){
			var dramaObjects = $.grep(chosenDramas, function(e){ return e.author == authors[i]; });
			var authorObject = generateAuthorObject(dramaObjects);
			authorList.push(authorObject);
		}
	};

	var getAuthorList = function(){
		return authorList;
	};

	var generateAuthorObject = function(dramaObjects){
		var authorObj = {};

		authorObj.name = dramaObjects[0].author;
		var average_number_of_scenes = 0;
		var average_number_of_speeches = 0;
		var average_number_of_speakers = 0;
		var average_configuration_density = 0;
		var average_average_length_of_speeches = 0;
		var average_median_length_of_speeches = 0;
		var average_maximum_length_of_speeches = 0;
		var average_minimum_length_of_speeches = 0;
		var titles = [];

		for(var i = 0; i < dramaObjects.length; i++){
			average_number_of_scenes += dramaObjects[i].number_of_scenes;
			average_number_of_speeches += dramaObjects[i].number_of_speeches_in_drama;
			average_number_of_speakers += dramaObjects[i].speakers.length;
			average_configuration_density += dramaObjects[i].configuration_density;
			average_average_length_of_speeches += dramaObjects[i].average_length_of_speeches_in_drama;
			average_median_length_of_speeches += dramaObjects[i].median_length_of_speeches_in_drama;
			average_maximum_length_of_speeches += dramaObjects[i].maximum_length_of_speeches_in_drama;
			average_minimum_length_of_speeches += dramaObjects[i].minimum_length_of_speeches_in_drama;
			titles.push(dramaObjects[i].title);
		}

		authorObj.average_number_of_scenes = roundToTwoDecimals(average_number_of_scenes/dramaObjects.length);
		authorObj.average_number_of_speeches = roundToTwoDecimals(average_number_of_speeches/dramaObjects.length);
		authorObj.average_number_of_speakers = roundToTwoDecimals(average_number_of_speakers/dramaObjects.length);
		authorObj.average_configuration_density = roundToTwoDecimals(average_configuration_density/dramaObjects.length);
		authorObj.average_average_length_of_speeches = roundToTwoDecimals(average_average_length_of_speeches/dramaObjects.length);
		authorObj.average_median_length_of_speeches = roundToTwoDecimals(average_median_length_of_speeches/dramaObjects.length);
		authorObj.average_maximum_length_of_speeches = roundToTwoDecimals(average_maximum_length_of_speeches/dramaObjects.length);
		authorObj.average_minimum_length_of_speeches = roundToTwoDecimals(average_minimum_length_of_speeches/dramaObjects.length);
		authorObj.titles = titles;

		return authorObj;

	};

	var setChosenDramas = function(){
		for(var i = 0; i < dramaInfo.length; i++){
			if(chosenDramasIds.indexOf(dramaInfo[i].id) > -1){
				chosenDramas.push(dramaInfo[i]);
			}
		}
	};

	var getChosenDramas = function(){
		return chosenDramas;
	}

	var initInfo = function(name){
		firebaseRef = new Firebase("https://popping-heat-510.firebaseio.com/" + name);
		firebaseRef.on("value", function(snapshot) {
			dramaInfo = snapshot.val();
			$(that).trigger("InitFinished");
		}, function (errorObject) {
		  console.log("The read failed: " + errorObject.code);
		});
	};

	var roundToTwoDecimals = function(number){
		number = (Math.round(number * 100)/100).toFixed(2);
		return parseFloat(number)
	};

	that.init = init;
	that.getChosenDramas = getChosenDramas;
	that.getAuthorList = getAuthorList;
	that.getCategoryList = getCategoryList;

	return that;
};