ActsScenes.ActsScenesModel = function(){
	var that = {};
	var metricsActs = [];
	var metricsScenes = [];
	var pureMetricsScenes = [];
	var actsProportionData = [];
	var dramaProportionData = {};
	var scenesProportionData = [];
	var metricsSpeeches = [];

	var init = function(){
		initData();
	};

	var initData = function(){
		console.log(sa_data);
		var drama = sa_data[0];
		
		for(i = 0; i < drama.acts.length; i++){
			metricsActs.push(drama.acts[i].sentimentMetricsBasic)
			var metricsScenesPerAct = [];
			for(j = 0; j < drama.acts[i].configurations.length; j++){
				metricsScenesPerAct.push(drama.acts[i].configurations[j].sentimentMetricsBasic);
				var metricsOfScene = drama.acts[i].configurations[j].sentimentMetricsBasic;
				metricsOfScene.numberOfScene = j+1;
				metricsOfScene.numberOfAct = i+1;
				pureMetricsScenes.push(metricsOfScene);
				for(k = 0; k < drama.acts[i].configurations[j].speeches.length; k++){
					var speech = drama.acts[i].configurations[j].speeches[k];
					var metricsOfSpeech = speech.sentimentMetricsBasic;
					metricsOfSpeech.subsequentNumber = speech.subsequentNumber;
					metricsOfSpeech.numberInConf = speech.numberInConf;
					metricsOfSpeech.numberInAct = speech.numberInAct;
					metricsSpeeches.push(metricsOfSpeech);
				}
			}
			metricsScenes.push(metricsScenesPerAct);
		}
		initRowsProportionsDrama(drama);
		initRowsProportionsActs(drama.acts);
		initRowsProportionsScenes(drama.acts);
	};

	var initRowsProportionsDrama = function(drama){
		dramaProportionData = getProportionDataOfUnit(drama);
	};

	var initRowsProportionsActs = function(acts){
		for (i = 0; i < acts.length; i++){
			actProportionData = getProportionDataOfUnit(acts[i]);
			actsProportionData.push(actProportionData);;
		}
	};

	var initRowsProportionsScenes = function(acts){
		for(i = 0; i < acts.length; i++){
			scenesProportionPerAct = [];
			for(j = 0; j < acts[i].configurations.length; j++){
				sceneProportionData = getProportionDataOfUnit(acts[i].configurations[j]);
				scenesProportionPerAct.push(sceneProportionData);
			}
			scenesProportionData.push(scenesProportionPerAct);
		}
	};

	var getProportionDataOfUnit = function(unit){
		var metricsUnit = unit.sentimentMetricsBasic.metricsTotal;
		var polarityWeighted = [["Positiv", metricsUnit.positiveSentiWS], ["Negativ", metricsUnit.negativeSentiWS]];
		var polarityCount = [["Positiv", metricsUnit.positiveSentiWSDichotom],
		["Negativ", metricsUnit.negativeSentiWSDichotom]];
		var emotion = [["Zorn", metricsUnit.anger], ["Erwartung", metricsUnit.anticipation], 
		["Ekel", metricsUnit.disgust], ["Angst", metricsUnit.fear], ["Freude", metricsUnit.joy],
		["Traurigkeit", metricsUnit.sadness], ["Überraschung", metricsUnit.surprise],
		["Vertrauen", metricsUnit.trust]];
		var emotionPresent = [["Emotion vorhanden", metricsUnit.emotionPresent]];

		var proportionData = {}
		proportionData["normalisedSBWs"] = {};
		proportionData["normalisedSBWs"]["polaritySentiWS"] = polarityWeighted;
		proportionData["normalisedSBWs"]["polaritySentiWSDichotom"] = polarityCount;
		proportionData["normalisedSBWs"]["emotions"] = emotion;
		proportionData["normalisedSBWs"]["emotionPresent"] = emotionPresent

		
		var noPolarityWords = unit.lengthInWords - 
		(metricsUnit.positiveSentiWSDichotom + metricsUnit.negativeSentiWSDichotom);
		var noEmotionWords = unit.lengthInWords - metricsUnit.emotionPresent;

		var polarityCountCopy = polarityCount.slice();
		var emotionCopy = emotion.slice();
		var emotionPresentCopy = emotionPresent.slice();

		polarityCountCopy.push(["Keine Polarität", noPolarityWords]);
		emotionCopy.push(["Keine Emotion", noEmotionWords]);
		emotionPresentCopy.push(["Keine Emotion", noEmotionWords]);

		proportionData["normalisedAllWords"] = {};
		proportionData["normalisedAllWords"]["polaritySentiWSDichotom"] = polarityCountCopy;
		proportionData["normalisedAllWords"]["emotions"] = emotionCopy;
		proportionData["normalisedAllWords"]["emotionPresent"] = emotionPresentCopy;

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

	var getDramaProportionData = function(){
		return dramaProportionData;
	};

	var getScenesProportionData = function(){
		return scenesProportionData;
	};

	var getPureMetricsScenes = function(){
		return pureMetricsScenes;
	};

	var getMetricsSpeeches = function(){
		return metricsSpeeches;
	};

	that.init = init;
	that.getMetricsActs = getMetricsActs;
	that.getMetricsScenes = getMetricsScenes;
	that.getActsProportionData = getActsProportionData;
	that.getDramaProportionData = getDramaProportionData;
	that.getScenesProportionData = getScenesProportionData;
	that.getPureMetricsScenes = getPureMetricsScenes;
	that.getMetricsSpeeches = getMetricsSpeeches;

	return that;
};