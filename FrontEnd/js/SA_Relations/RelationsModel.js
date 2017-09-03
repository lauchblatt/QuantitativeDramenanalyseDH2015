SA_Relations.RelationsModel = function(){
	var that = {};

	var dramaRelationsMetrics = {};

	var init = function(){
		initData();
	};

	var initData = function(){
		console.log(sa_data);
		var drama = sa_data[0];

		initDramaRelationsMetrics(drama);
		
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

	that.init = init;
	that.getDramaRelationsMetrics = getDramaRelationsMetrics;

	return that;
};