SA_Speakers.SA_SpeakersModel = function(){
	var that = {};
	var dramaSpeakersProportions = {};
	var actsSpeakersProportions = [];
	var scenesSpeakersProportions = [];

	var dramaSpeakersMetrics = {};
	var actsSpeakersMetrics = [];
	var scenesSpeakersMetrics = [];

	var speakerMetricsPerAct = {};

	var init = function(){
		initData();
	};

	var initData = function(){
		console.log(sa_data);
		var drama = sa_data[0];

		initSpeakersMetrics(drama)
		initSingleSpeakerProportions(drama);
		initSpeakerCourseMetrics(drama);
		
	};

	var initSpeakerCourseMetrics = function(drama){
		allSpeakers = [];
		for(var i = 0; i < drama.speakers.length; i++){
			allSpeakers.push(drama.speakers[i]["name"]);
		}

		for(var j = 0; j < allSpeakers.length; j++){
			var currentName = allSpeakers[j];
			speakerMetricsPerAct[currentName] = [];
			for (var k = 0; k < drama.acts.length; k++){
				var currentAct = drama.acts[k];
				if(nameInSpeakers(currentAct.appearingSpeakers, currentName)){
					var speakerActMetrics = getSpeakerMetricsByName(currentAct.speakers, currentName);
					speakerMetricsPerAct[currentName].push(speakerActMetrics);
				}else{
					speakerMetricsPerAct[currentName].push(null);
				}
			}
		}
	};

	var nameInSpeakers = function(appearingSpeakers, currentName){
		if(appearingSpeakers.indexOf(currentName) > -1){
			return true;
		} else{
			return false;
		}
	};

	var getSpeakerMetricsByName = function(speakers, currentName){
		for(var i = 0; i < speakers.length; i++){
			if(currentName == speakers[i]["name"]){
				return speakers[i].sentimentMetricsBasic;
			}
		}
	};

	var initSpeakersMetrics = function(drama){
		dramaSpeakersMetrics = getSpeakersMetrics(drama.speakers);

		for(var i = 0; i < drama.acts.length; i++){
			var actMetrics = getSpeakersMetrics(drama.acts[i].speakers);
			actsSpeakersMetrics.push(actMetrics);
			var scenesPerActMetrics = []
			for(var j = 0; j < drama.acts[i].configurations.length; j++){
				var sceneMetrics = getSpeakersMetrics(drama.acts[i].configurations[j].speakers);
				scenesPerActMetrics.push(sceneMetrics);
			}
			scenesSpeakersMetrics.push(scenesPerActMetrics);
		}
	};

	var getSpeakersMetrics = function(speakers){
		metrics = {};
		for(var i = 0; i < speakers.length; i++){
			metrics[speakers[i]["name"]] = speakers[i].sentimentMetricsBasic;
		}
		return metrics;
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

	var getDramaSpeakersMetrics = function(){
		return dramaSpeakersMetrics;
	};

	var getActsSpeakersMetrics = function(){
		return actsSpeakersMetrics;
	};

	var getScenesSpeakersMetrics = function(){
		return scenesSpeakersMetrics;
	};

	var getSpeakerMetricsPerAct = function(){
		return speakerMetricsPerAct;
	};

	that.init = init;
	that.getDramaSpeakersProportions = getDramaSpeakersProportions;
	that.getActsSpeakersProportions = getActsSpeakersProportions;
	that.getScenesSpeakersProportions = getScenesSpeakersProportions;

	that.getDramaSpeakersMetrics = getDramaSpeakersMetrics;
	that.getActsSpeakersMetrics = getActsSpeakersMetrics;
	that.getScenesSpeakersMetrics = getScenesSpeakersMetrics;
	that.getSpeakerMetricsPerAct = getSpeakerMetricsPerAct;

	return that;
};