SA_Relations.RelationsModel = function(){
	var that = {};

	var dramaRelationsMetrics = {};
	var actsRelationsMetrics = {};
	var scenesRelationsMetrics = {};

	var numberOfActs = 0;
	var numberOfScenes = 0;
	var numberOfScenesPerAct = [];

	var init = function(){
		initData();
	};

	var initData = function(){
		console.log(sa_data);
		var drama = sa_data[0];
		setNumberOfScenesAndActs(drama);
		initDramaRelationsMetrics(drama);
		
		initActsAndScenesObjects(drama);
		
		initActsRelationsMetrics(drama);
		initScenesRelationsMetrics(drama);
		console.log("Hello");
		console.log(scenesRelationsMetrics);
		
	};

	var setNumberOfScenesAndActs = function(drama){
		for(i = 0; i < drama.acts.length; i++){
			numberOfScenes = numberOfScenes + drama.acts[i].configurations.length;
			numberOfScenesPerAct.push(drama.acts[i].configurations.length);		
		}
		numberOfActs = drama.acts.length;
	};

	var initActsAndScenesObjects = function(drama){
		var speakers = drama.speakers;
		for(i = 0; i < speakers.length; i++){
			actsRelationsMetrics[speakers[i].name] = {};
			scenesRelationsMetrics[speakers[i].name] = {};
			for(var target in dramaRelationsMetrics[speakers[i].name]){
				actsRelationsMetrics[speakers[i].name][target] = new Array(numberOfActs);
				scenesRelationsMetrics[speakers[i].name][target] = new Array(numberOfActs);
				for(var j = 0; j < numberOfScenesPerAct.length; j++){
					scenesRelationsMetrics[speakers[i].name][target][j] = new Array(numberOfScenesPerAct[j]);
				}			
			}
		}
	};

	var initScenesRelationsMetrics = function(drama){
		for(var i = 0; i < drama.acts.length; i++){
			for(var j = 0; j < drama.acts[i].configurations.length; j++){
				var confSpeakers = drama.acts[i].configurations[j].speakers;
				for(var k = 0; k < confSpeakers.length; k++){
					var sentimentRelations = confSpeakers[k].sentimentRelations;
					for(var l = 0; l < sentimentRelations.length; l++){
						var origin = sentimentRelations[l].originSpeaker;
						var target = sentimentRelations[l].targetSpeaker;
						scenesRelationsMetrics[origin][target][i][j] = sentimentRelations[l].sentimentMetricsBasic;
					}
				}
			}

		}
	};

	var initActsRelationsMetrics = function(drama){

		for(var k = 0; k < drama.acts.length; k++){
			var actSpeakers = drama.acts[k].speakers;
			for(var l = 0; l < actSpeakers.length; l++){
				var sentimentRelations = actSpeakers[l].sentimentRelations;
				for(var m = 0; m < sentimentRelations.length; m++){
					var origin = sentimentRelations[m].originSpeaker;
					var target = sentimentRelations[m].targetSpeaker;
					actsRelationsMetrics[origin][target][k] = sentimentRelations[m].sentimentMetricsBasic;
				}
			}
		}
		fillUndefinedWithNull();
	};

	var fillUndefinedWithNull = function(){
		for(var speaker in actsRelationsMetrics){
			for(var target in actsRelationsMetrics[speaker]){
				for(i = 0; i < actsRelationsMetrics[speaker][target].length; i++){
					if(actsRelationsMetrics[speaker][target][i] == undefined){
						actsRelationsMetrics[speaker][target][i] = null;
					}
				}
			}
		}
	};

	var initDramaRelationsMetrics = function(drama){
		var speakers = drama.speakers;
		for(i = 0; i < speakers.length; i++){
			var relationsPerSpeaker = speakers[i].sentimentRelations;
			if(relationsPerSpeaker.length > 0){
				var relationsPerTarget = {};
				for(j = 0; j < relationsPerSpeaker.length; j++){
					var target = relationsPerSpeaker[j].targetSpeaker;
					var metrics = relationsPerSpeaker[j].sentimentMetricsBasic;
					relationsPerTarget[target] = metrics;
				}
				dramaRelationsMetrics[speakers[i]["name"]] = relationsPerTarget;
			}

		}
	};

	var getDramaRelationsMetrics = function(){
		return dramaRelationsMetrics;
	};

	var getActsRelationsMetrics = function(){
		return actsRelationsMetrics;
	};

	var getNumberOfActs = function(){
		return numberOfActs;
	};

	var getNumberOfScenes = function(){
		return numberOfScenes;
	};

	that.init = init;
	that.getDramaRelationsMetrics = getDramaRelationsMetrics;
	that.getActsRelationsMetrics = getActsRelationsMetrics;
	that.getNumberOfActs = getNumberOfActs;
	that.getNumberOfScenes = getNumberOfScenes;

	return that;
};