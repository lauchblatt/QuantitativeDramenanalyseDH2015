SA_Speakers.SpeakersActsView = function(){
	var that = {};
	var metricsForSpeakerPerActs = {};


	var init = function(speakerActsMetrics){
		metricsForSpeakerPerActs = speakerActsMetrics;
		initListener();
		renderSpeakerDropDown();

	};

	var initListener = function(){
		$("#selection-speakersActs-bar-metric").change(renderSpeakersActBars);
		$("#selection-speakersActs-bar-normalisation").change(renderSpeakersActBars);
		$("#selection-speakersActs-speaker-bar").change(renderSpeakersActBars);
	};

	var renderSpeakerDropDown = function(){
		var $speakerSelect = $("#selection-speakersActs-speaker-bar");
		for (var speaker in metricsForSpeakerPerActs){
			var $select = $("<option>" + speaker + "</option>");
			$speakerSelect.append($select);
		}	
	};


	var renderSpeakersActBars = function(){
		var metricSelection = $("#selection-speakersActs-bar-metric").val();
		var normalisationSelection = $("#selection-speakersActs-bar-normalisation").val()
		var speakerSelection = $("#selection-speakersActs-speaker-bar").val()
		var metric = transformGermanMetric(metricSelection);
		var normalisation = transformGermanMetric(normalisationSelection);
		var metrics = getSpeakerActsMetrics(metric, normalisation, speakerSelection);
		drawSpeakersActBarsChart(normalisationSelection, metricSelection, speakerSelection, metrics);
	};

	var getSpeakerActsMetrics = function(metricName, normalisation, speaker){
		var speakerMetrics = metricsForSpeakerPerActs[speaker];
		var metrics = [];
		for(i = 0; i < speakerMetrics.length; i++){
			if(speakerMetrics[i] == null){
				metrics.push([(i+1), 0, "kein Auftritt"]);
			}else{
				var metric = speakerMetrics[i][normalisation][metricName];
				metrics.push([(i+1), metric, (Math.round(metric * 10000) / 10000).toString()]);
			}
		}
		return metrics;
	};

	var drawSpeakersActBarsChart = function(germanType, germanMetric, speakerName, metrics){
		var vAxisTitle = germanMetric + " - " + germanType;
		var data = new google.visualization.DataTable();
		data.addColumn("number", "Act-Number")
		data.addColumn("number", germanMetric)
		data.addColumn({type:'string', role:'annotation'})

        data.addRows(metrics);
        
        var options = {title:'Akt-Verlauf - ' + speakerName + ' : ' + vAxisTitle,
        			   height: 600,
        			   width: 1130,
        			   chartArea:{width:'70%',height:'75%'},
        			    trendlines: {
				          0: {
				          	tooltip: false,
				            type: 'polynomial',
				            color: 'green',
				            lineWidth: 3,
				            opacity: 0.3,
				            showR2: false,
				            visibleInLegend: false
				          }
				        },
				        hAxis: {
        			   	title: 'Akte'
        			   },
        			   vAxis: {
        			   	title: vAxisTitle,
        			   	baseline: 0,
        			   },
                   	   animation: {
                   	   	duration: 700,
                   	   	startup: true
                   	   }};
        
        var formatter = new google.visualization.NumberFormat(
    		{fractionDigits: 6});
		formatter.format(data, 1); // Apply formatter to second column

        var chart = new google.visualization.ColumnChart(document.getElementById("chart-div-speakersAct"));

        chart.draw(data, options);
	};

	that.init = init;
	that.renderSpeakersActBars = renderSpeakersActBars;

	return that;
};