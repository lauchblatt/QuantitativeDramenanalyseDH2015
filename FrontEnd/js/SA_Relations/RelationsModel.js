SA_Relations.RelationsModel = function(){
	var that = {};

	var dramaRelationsMetrics = {};
	var actsRelationsMetrics = {};

	var numberOfActs = -1;

	var init = function(){
		initData();
	};

	var initData = function(){
		console.log(sa_data);
		var drama = sa_data[0];
		numberOfActs = drama.acts.length;

		initDramaRelationsMetrics(drama);
		console.log(dramaRelationsMetrics);
		initActsRelationsMetrics(drama);
		console.log(actsRelationsMetrics);
		
	};

	var initActsRelationsMetrics = function(drama){
		var speakers = drama.speakers;
		for(i = 0; i < speakers.length; i++){
			actsRelationsMetrics[speakers[i].name] = {};
			for(var target in dramaRelationsMetrics[speakers[i].name]){
				actsRelationsMetrics[speakers[i].name][target] = new Array(5);
			}
		}
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

	that.init = init;
	that.getDramaRelationsMetrics = getDramaRelationsMetrics;
	that.getActsRelationsMetrics = getActsRelationsMetrics;
	that.getNumberOfActs = getNumberOfActs;

	return that;
};