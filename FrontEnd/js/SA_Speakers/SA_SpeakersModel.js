SA_Speakers.SA_SpeakersModel = function(){
	var that = {};
	var dramaSpeakersProportions = {};
	var actsSpeakersProportions = [];
	var scenesSpeakersProportions = [];

	var init = function(){
		initData();
	};

	var initData = function(){
		console.log(sa_data);
		var drama = sa_data[0];

		initSingleSpeakerProportions(drama);
		
	};

	var initSingleSpeakerProportions = function(drama){
		dramaSpeakersProportions = getSpeakersProportions(drama.speakers);

		for(var i = 0; i < drama.acts.length; i++){
			var actSpeakersProportions = getSpeakersProportions(drama.acts[i].speakers);
			actsSpeakersProportions.push(actSpeakersProportions);
			var scenesPerActProportions = []

			for(var j = 0; j < drama.acts[i].configurations.length; j++){
				var sceneSpeakersProportions = getSpeakersProportions(drama.acts[i].configurations[j].speakers);
				scenesPerActProportions.push(sceneSpeakersProportions);
			}
			scenesSpeakersProportions.push(scenesPerActProportions);
		}
	};

	var getSpeakersProportions = function(speakers){
		var speakersProportions = {};
		for(var i = 0; i < speakers.length; i++){
			speakersProportions[speakers[i]["name"]] = getProportionDataOfUnit(speakers[i]);
		}
		return speakersProportions;
	}

	var getDramaSpeakersProportions = function(){
		return dramaSpeakersProportions;
	};

	var getActsSpeakersProportions = function(){
		return actsSpeakersProportions;
	};

	var getScenesSpeakersProportions = function(){
		return scenesSpeakersProportions;
	};

	that.init = init;
	that.getDramaSpeakersProportions = getDramaSpeakersProportions;
	that.getActsSpeakersProportions = getActsSpeakersProportions;
	that.getScenesSpeakersProportions = getScenesSpeakersProportions;

	return that;
};