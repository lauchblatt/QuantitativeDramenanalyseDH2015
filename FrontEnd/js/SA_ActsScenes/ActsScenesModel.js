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
		}
		initRowsProportionsActs(drama.acts);
	};

	var initRowsProportionsActs = function(acts){
		for (i = 0; i < acts.length; i++){
			metricsAct = acts[i].sentimentMetricsBasic.metricsTotal;
			polarityWeighted = [["Positiv", metricsAct.positiveSentiWS], ["Negativ", metricsAct.negativeSentiWS]];
			polarityCount = [["Positiv", metricsAct.positiveSentiWSDichotom],
			 ["Negativ", metricsAct.negativeSentiWSDichotom]];
			emotion = [["Zorn", metricsAct.anger], ["Erwartung", metricsAct.anticipation], 
			["Ekel", metricsAct.disgust], ["Angst", metricsAct.fear], ["Freude", metricsAct.joy],
			["Traurigkeit", metricsAct.sadness], ["Überraschung", metricsAct.surprise],
			["Vertrauen", metricsAct.trust]];

			actProportionData = {}
			actProportionData["normalisedSBWs"] = {};
			actProportionData["normalisedSBWs"]["polarityWeighted"] = polarityWeighted;
			actProportionData["normalisedSBWs"]["polarityCount"] = polarityCount;
			actProportionData["normalisedSBWs"]["emotions"] = emotion;
			actsProportionData.push(actProportionData);
		}
	};

	var getMetricsActs = function(){
		return metricsActs;
	};

	var getActsProportionData = function(){
		return actsProportionData;
	};


	that.init = init;
	that.getMetricsActs = getMetricsActs;
	that.getActsProportionData = getActsProportionData;

	return that;
};