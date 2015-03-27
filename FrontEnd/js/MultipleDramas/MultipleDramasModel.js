MultipleDramas.MultipleDramasModel = function(){
	var that = {};
	var dramaInfo = [];
	var firebaseRef = null;
	var chosenDramasIds = [];
	var chosenDramas = [];

	var init = function(){
		for(var i = 0; i < 100; i++){
			chosenDramasIds.push(i);
		}
		$(that).on("InitFinished", continueInit);
		initInfo("drama_data");
	};

	var continueInit = function(){
		if(dramaInfo != null){
			setChosenDramas();
			roundValues();
			$(that).trigger("InfoFinished");
		}
	};

	var roundValues = function(){
		for(var i = 0; i < chosenDramas.length; i++){
			chosenDramas[i].configuration_density = roundToTwoDecimals(chosenDramas[i].configuration_density);
			chosenDramas[i].average_length_of_speeches_in_drama = roundToTwoDecimals(chosenDramas[i].average_length_of_speeches_in_drama);
		}
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

	return that;
};