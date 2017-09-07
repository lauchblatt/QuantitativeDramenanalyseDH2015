SA_Speakers.BasicDramaSpeakersView = function(){
	var that = {};
	var metricsForDrama = {};

	var init = function(dramaMetrics){
		metricsForDrama = dramaMetrics;
		initListener();
		renderSpeakers();

	};

	var initListener = function(){
		$("#selection-basicDramaSpeakers-speaker-bar").change(renderDramaBars);
		$("#selection-basicDramaSpeakers-bar-metric").change(renderDramaBars);
		$("#selection-basicDramaSpeakers-bar-normalisation").change(renderDramaBars);
	};

	var renderSpeakers = function(){
		for(var speaker in metricsForDrama){
			var $select = $("<option>" + speaker +"</option>");
			$("#selection-basicDramaSpeakers-speaker-bar").append($select);
		}
	};


	var renderDramaBars = function(){
		var speakerSelection = $("#selection-basicDramaSpeakers-speaker-bar")
		var metricSelection = $("#selection-basicDramaSpeakers-bar-metric").val();
		var normalisationSelection = $("#selection-basicDramaSpeakers-bar-normalisation").val()
		var metric = transformGermanMetric(metricSelection);
		var normalisation = transformGermanMetric(normalisationSelection);
		
		//var metrics = getDramaMetrics(normalisation, metric);
		//drawBarChartDrama(normalisationSelection, metricSelection, metrics);
		
	}

	var getDramaMetrics = function(normalisation, metricName, speakerName){
		var metrics = [];
		var selectedMetrics = metricsForDrama[normalisation][metricName];
		for(var metricName in selectedMetrics){
			var singleMetric = selectedMetrics[metricName];
			var color = "color: ";
			if(metricName == "positiveSentiWS" || metricName == "positiveSentiWSDichotom"){
				color = "color: green";
			}
			if(metricName == "negativeSentiWS" || metricName == "negativeSentiWSDichotom"){
				color = "color: red";
			}
			if(metricName == "negativeSentiWS"){
				singleMetric = singleMetric * -1;
			}
			var row = [transformEnglishMetric(metricName), singleMetric, (Math.round(singleMetric * 10000) / 10000).toString(), color];
			metrics.push(row);
		}
		return metrics;
	};

	var drawBarChartDrama = function(normalisation, metricName, metrics){

	};

	that.init = init;
	that.renderDramaBars = renderDramaBars;

	return that;
};