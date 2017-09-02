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

		$("#selection-speakersScenesPerAct-bar").change(renderScenesPerActBars);
		$("#selection-speakersScenesPerAct-bar-metric").change(renderScenesPerActBars);
		$("#selection-speakersScenesPerAct-bar-normalisation").change(renderScenesPerActBars)


	};

	var renderSpeakerDropDown = function(){
		var $speakerSelect = $("#selection-speakersScenes-speaker-line");
		var $speakerSelectActScenes = $("#selection-speakersScenesPerAct-bar");
		for (var speaker in metricsForSpeakerPerScenes){
			var $select1 = $("<option>" + speaker + "</option>");
			var $select2 = $("<option>" + speaker + "</option>");
			$speakerSelect.append($select1);
			$speakerSelectActScenes.append($select2);
		}	
	};

	var renderScenesPerActBars = function(){
		var speakerSelection = $("#selection-speakersScenesPerAct-bar").val();
		var metricSelection = $("#selection-speakersScenesPerAct-bar-metric").val();
		var normalisationSelection = $("#selection-speakersScenesPerAct-bar-normalisation").val()
		
		var metric = transformGermanMetric(metricSelection);
		var normalisation = transformGermanMetric(normalisationSelection);
		var metrics = getSpeakerScenesPerActMetrics(metric, normalisation, speakerSelection);
		drawChartScenesPerAct(metricSelection, normalisationSelection, speakerSelection, metrics);		
	};

	var drawChartScenesPerAct = function(metricName, typeName, speakerName, metrics){

		$charts_scenes = $("#charts-speakersScenesPerAct-bar");
		console.log(metrics);
		for(var act = 0; act < metrics.length; act++){
			$div_chart = $("<div></div>");
			$div_chart.addClass("scenes-chart");
			$div_chart.attr("id", "chart-div-speakersScenesPerAct-" + act);
			$charts_scenes.append($div_chart);
			var actNumber = act + 1;
			drawBarChartForScenesInAct(("chart-div-speakersScenesPerAct-" + act), 
				metricName, typeName, metrics[act], actNumber, speakerName);
		}
	};

	var drawBarChartForScenesInAct = function(divId, metricName, typeName, metrics, actNumber, speakerName){
        var vAxisTitle = metricName + " - " + typeName
		var data = new google.visualization.DataTable();
		data.addColumn("number", "Scene-Number");
		data.addColumn("number", metricName);
		data.addColumn({type:'string', role:'annotation', 'p': {'html': true}});

        data.addRows(metrics);
        //necessary to have consistent gaps according to the scenes on the graph 
        var ticksArray = [];
        for(var k = 0; k < metrics.length; k++){
        	ticksArray.push(k+1);
        }
        var options = {title:'Szenen-Verlauf in Akt ' + actNumber + " - " + speakerName + ": " + vAxisTitle,
        			   height: 600,
        			   width: 1170,
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
        			   	ticks: ticksArray
        			   },
        			   vAxis: {
        			   	title: vAxisTitle,
        			   	baseline: 0
        			   },
                   	   animation: {
                   	   	duration: 700,
                   	   	startup: true
                   	   }};
        
        var formatter = new google.visualization.NumberFormat(
    		{fractionDigits: 6});
		formatter.format(data, 1); // Apply formatter to second column

        var chart = new google.visualization.ColumnChart(document.getElementById(divId));

        chart.draw(data, options);
	};


	var renderSpeakersScenesLine = function(){
		var metricSelection = $("#selection-speakerScenes-line-metric").val();
		var normalisationSelection = $("#selection-speakerScenes-line-type").val()
		var speakerSelection = $("#selection-speakersScenes-speaker-line").val()
		var metric = transformGermanMetric(metricSelection);
		var normalisation = transformGermanMetric(normalisationSelection);
		var metrics = getSpeakerScenesMetrics(metric, normalisation, speakerSelection);
		
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

	var getSpeakerScenesPerActMetrics = function(metricName, normalisation, speakerName){
		var speakerMetricsActs = metricsForSpeakerPerScenes[speakerName];
		var metrics = [];
		for(i = 0; i < speakerMetricsActs.length; i++){
			var metricsPerAct = [];
			for(j = 0; j <speakerMetricsActs[i].length; j++){
				if(speakerMetricsActs[i][j] == null){
					metricsPerAct.push([j+1, 0, "kein Auftritt"]);
				}else{
					var metric = speakerMetricsActs[i][j][normalisation][metricName];
					metricsPerAct.push([j+1, metric, (Math.round(metric * 10000) / 10000).toString()]);
				}
			}
			metrics.push(metricsPerAct);
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
	that.renderScenesPerActBars = renderScenesPerActBars;

	return that;
};