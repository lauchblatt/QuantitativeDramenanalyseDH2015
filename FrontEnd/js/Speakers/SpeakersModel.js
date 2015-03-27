Speakers.SpeakersModel = function(){
	var that = {};
	var currentDrama_id = 44;
	var speakersInfo = [];
	var scenesInfo = [];
	var dramaInfo = null;

	var init = function(){
		$(that).on("InitFinished", continueInit);
		initInfo('speakers_data');
		initInfo("scenes_data");
		initInfo("drama_data");
	};

	var continueInit = function(){
		if(speakersInfo.length > 0 && scenesInfo.length > 0  && dramaInfo != null){
			calculateAppearancePerSpeakers();
			roundAverageLengths();
			calculateScenesPerSpeakers();
			$(that).trigger("InfoFinished");
		}
		
	};

	var calculateScenesPerSpeakers = function(){
		for(i = 0; i < speakersInfo.length; i++){
			var ratio = roundToTwoDecimals(speakersInfo[i].number_of_appearances/dramaInfo.number_of_scenes);
			var percentage = parseInt(ratio * 100);
			speakersInfo[i].appearances_percentage = percentage;
		}
	};

	var roundAverageLengths = function(){
		for(i = 0; i < speakersInfo.length; i++){
			speakersInfo[i].average_length_of_speakers_speeches = 
			roundToTwoDecimals(speakersInfo[i].average_length_of_speakers_speeches);
		}
	};

	var calculateAppearancePerSpeakers = function(){
		for(var speaker = 0; speaker < speakersInfo.length; speaker++){
			calculateAppearancePerSpeaker(speakersInfo[speaker]);
		}
	};

	var calculateAppearancePerSpeaker = function(speaker){
		var appearances = 0;
		for(var act = 0; act < scenesInfo.length; act++){
			for(var scene = 0; scene < scenesInfo[act].length; scene++){
				if(!(scenesInfo[act][scene].appearing_speakers === undefined)){
					for(var i = 0; i < scenesInfo[act][scene].appearing_speakers.length; i++){
						if(speaker.name == scenesInfo[act][scene].appearing_speakers[i]){
							appearances++;
						}
					}
				}
			}
		}
		speaker.number_of_appearances = appearances;
	}

	var initInfo = function(name){
		firebaseRef = new Firebase("https://popping-heat-510.firebaseio.com/" + name +"/" + currentDrama_id);
		firebaseRef.on("value", function(snapshot) {
			switch (name) {
				case "speakers_data":
					speakersInfo = snapshot.val();
					break;
				case "scenes_data":
					scenesInfo = snapshot.val();
					break;
				case "drama_data":
					dramaInfo = snapshot.val();
					break;
				default:
					console.log("Something went wrong.");
			}
			$(that).trigger("InitFinished");
		}, function (errorObject) {
		  console.log("The read failed: " + errorObject.code);
		});
	};

	var roundToTwoDecimals = function(number){
		number = (Math.round(number * 100)/100).toFixed(2);
		return parseFloat(number)
	};

	var getSpeakersInfo = function(){
		return speakersInfo;
	};

	that.init = init;
	that.getSpeakersInfo = getSpeakersInfo;

	return that;
};