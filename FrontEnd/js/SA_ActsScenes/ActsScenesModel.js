ActsScenes.ActsScenesModel = function(){
	var that = {};
	var metricsActs = [];
	var metricsScenes = [];
	var actsProportionData = [];

	var init = function(){
		initData();
	};

	var initData = function(){
		console.log(sa_data);
		var drama = sa_data[0];
		
		for(i = 0; i < drama.acts.length; i++){
			metricsActs.push(drama.acts[i].sentimentMetricsBasic)
			for(j = 0; j < drama.acts[i].configurations.length; j++){
				metricsScenes.push(drama.acts[i].configurations[j].sentimentMetricsBasic)
			}
		}
		initRowsProportionsActs(drama.acts);
	};

	var initRowsProportionsActs = function(acts){
		for (i = 0; i < acts.length; i++){
			actProportionData = getProportionDataOfUnit(acts[i], acts[i].lengthInWords);
			actsProportionData.push(actProportionData);;
		}
	};

	var getProportionDataOfUnit = function(unit, lengthInWords){
		var metricsUnit = unit.sentimentMetricsBasic.metricsTotal;
		var polarityWeighted = [["Positiv", metricsUnit.positiveSentiWS], ["Negativ", metricsUnit.negativeSentiWS]];
		var polarityCount = [["Positiv", metricsUnit.positiveSentiWSDichotom],
		["Negativ", metricsUnit.negativeSentiWSDichotom]];
		var emotion = [["Zorn", metricsUnit.anger], ["Erwartung", metricsUnit.anticipation], 
		["Ekel", metricsUnit.disgust], ["Angst", metricsUnit.fear], ["Freude", metricsUnit.joy],
		["Traurigkeit", metricsUnit.sadness], ["Überraschung", metricsUnit.surprise],
		["Vertrauen", metricsUnit.trust]];

		var proportionData = {}
		proportionData["normalisedSBWs"] = {};
		proportionData["normalisedSBWs"]["polaritySentiWS"] = polarityWeighted;
		proportionData["normalisedSBWs"]["polaritySentiWSDichotom"] = polarityCount;
		proportionData["normalisedSBWs"]["emotions"] = emotion;

		console.log(polarityCount)
		
		var noPolarityWords = unit.lengthInWords - 
		(metricsUnit.positiveSentiWSDichotom + metricsUnit.negativeSentiWSDichotom);
		var noEmotionWords = unit.lengthInWords - metricsUnit.emotionPresent;

		var polarityCountCopy = polarityCount.slice();
		var emotionCopy = emotion.slice();
		polarityCountCopy.push(["Keine Polarität", noPolarityWords]);
		emotionCopy.push(["Keine Emotion", noEmotionWords]);
		proportionData["normalisedAllWords"] = {};
		proportionData["normalisedAllWords"]["polaritySentiWSDichotom"] = polarityCountCopy;
		proportionData["normalisedAllWords"]["emotions"] = emotionCopy;
		
		console.log(polarityCountCopy)

		return proportionData;

	};

	var getMetricsActs = function(){
		return metricsActs;
	};

	var getMetricsScenes = function(){
		return metricsScenes;
	};

	var getActsProportionData = function(){
		return actsProportionData;
	};

	that.init = init;
	that.getMetricsActs = getMetricsActs;
	that.getMetricsScenes = getMetricsScenes;
	that.getActsProportionData = getActsProportionData;

	return that;
};