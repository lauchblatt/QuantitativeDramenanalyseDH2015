SA_Speakers.SpeakersScenesView = function(){
	var that = {};
	var metricsForSpeakerPerScenes = {};

	var init = function(speakerScenesMetrics){
		metricsForSpeakerPerScenes = speakerScenesMetrics;
		initListener();
		renderSpeakerDropDown();

	};

	var initListener = function(){
		$("#selection-speakerScenes-line-metric").change(renderSpeakersScenesLine);
		$("#selection-speakerScenes-line-type").change(renderSpeakersScenesLine);
		$("#selection-speakersScenes-speaker-line").change(renderSpeakersScenesLine);
	};

	var renderSpeakerDropDown = function(){
		var $speakerSelect = $("#selection-speakersScenes-speaker-line");
		for (var speaker in metricsForSpeakerPerScenes){
			var $select = $("<option>" + speaker + "</option>");
			$speakerSelect.append($select);
		}	
	};


	var renderSpeakersScenesLine = function(){
		console.log(metricsForSpeakerPerScenes);
		var metricSelection = $("#selection-speakerScenes-line-metric").val();
		var normalisationSelection = $("#selection-speakerScenes-line-type").val()
		var speakerSelection = $("#selection-speakersScenes-speaker-line").val()
		var metric = transformGermanMetric(metricSelection);
		var normalisation = transformGermanMetric(normalisationSelection);
		var metrics = getSpeakerScenesMetrics(metric, normalisation, speakerSelection);
		console.log(metrics);
		
		drawSpeakersScenesLineChart(metricSelection, normalisationSelection, speakerSelection, metrics);
	};

	var getSpeakerScenesMetrics = function(metricName, normalisation, speakerName){
		var speakerMetricsActs = metricsForSpeakerPerScenes[speakerName];
		var metrics = [];
		for(i = 0; i < speakerMetricsActs.length; i++){
			for(j = 0; j <speakerMetricsActs[i].length; j++){
				if(speakerMetricsActs[i][j] == null){
					var sceneName = (i+1).toString() + ". Akt, " + (j+1).toString() + " .Szene";
					metrics.push([sceneName, 0]);
				}else{
					var metric = speakerMetricsActs[i][j][normalisation][metricName];
					var sceneName = (i+1).toString() + ". Akt, " + (j+1).toString() + " .Szene";
					metrics.push([sceneName, metric]);
				}
			}
		}
		return metrics;
	};

	var drawSpeakersScenesLineChart = function(germanMetric, germanType, speakerName, metrics){
		var vAxisTitle = germanMetric + " - " + germanType;
		var data = new google.visualization.DataTable();
		data.addColumn("string", "sceneName")
		data.addColumn("number", germanMetric)
        data.addRows(metrics);

        var options = {title:'Szenen-Verlauf - ' + speakerName + ": " + vAxisTitle,
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
        			   	title: 'Szenen',
        			   	slantedText: false
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
		formatter.format(data, 1);
        
        var dashboard = new google.visualization.Dashboard(document.getElementById('dashbord-speakersScenes'));

        var lineChartSpeechesSlider = new google.visualization.ControlWrapper({
          'controlType': 'NumberRangeFilter',
          'containerId': 'filter-speakersScenes',
          'options': {
            'filterColumnLabel': germanMetric
          }
        });

        var lineChart = new google.visualization.ChartWrapper({
          'chartType': 'LineChart',
          'containerId': 'chart-speakersScenes',
          'options': options
        });
        dashboard.bind(lineChartSpeechesSlider, lineChart);
        dashboard.draw(data);
	};

	that.init = init;
	that.renderSpeakersScenesLine = renderSpeakersScenesLine;

	return that;
};