SA_Speakers.SpeakersComparisonView = function(){
	var that = {};

	var init = function(){

		initListener();
	};

	var initListener = function(){

		$("#selection-speakersComparison-bar-metric").change(renderSpeakersComparisonBarChart);
		$("#selection-speakersComparison-normalisation").change(renderSpeakersComparisonBarChart);
	};

	var renderSpeakersComparisonBarChart = function(){

	};

	var drawSpeakersComparisonBarChart = function(metricName, proportionType, germanMetric, germanType, proportions){

	};

	that.init = init;

	return that;
};