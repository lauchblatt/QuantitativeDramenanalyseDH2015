ActsScenes.SpeechesView = function(){
	var that = {};
	var metricsForSpeeches = []

	var init = function(speechesData){
		metricsForSpeeches = speechesData;
		console.log(metricsForSpeeches);
		initListener();
	};

	var initListener = function(){

		$("#selection-dramaSpeeches-line-metric").change(renderSpeechesLineChart);
		$("#selection-dramaSpeeches-line-type").change(renderSpeechesLineChart);
	};

	var renderSpeechesLineChart = function(){
		var metricSelection = $("#selection-dramaSpeeches-line-metric").val();
		var typeSelection = $("#selection-dramaSpeeches-line-type").val();

		var metric = transformGermanMetric(metricSelection);
		var type = transformGermanMetric(typeSelection);

		var metricPairs = getMetricPairs(type, metric);
		drawSpeechesLineChart(metricPairs, metricSelection, typeSelection);

	};

	var getMetricPairs = function(type, metric){
		var metricPairs = []
		for(i = 0; i < metricsForSpeeches.length; i++){
			pair = [i, metricsForSpeeches[i][type][metric]];
			metricPairs.push(pair);
		}
		return metricPairs;
	};

	var drawSpeechesLineChart = function(metricPairs, germanMetric, germanType){
		var vAxisTitle = germanMetric + " - " + germanType;
		var data = new google.visualization.DataTable();
		data.addColumn("number", "numberOfSpeech")
		data.addColumn("number", germanMetric)
        data.addRows(metricPairs);

        var options = {title:'Repliken-Verlauf (ganzes Drama): ' + vAxisTitle,
        			   height: 600,
        			   width: 1130,
        			   explorer: { 
					        actions: ['dragToZoom', 'rightClickToReset'],
					        axis: 'horizontal',
					        keepInBounds: true,
					        maxZoomIn: 10.0
						},
        			   chartArea:{width:'80%',height:'75%'},
        			    trendlines: {
				          0: {
				          	tooltip: false,
				            type: 'polynomial',
				            color: 'green',
				            lineWidth: 3,
				            opacity: 0.4,
				            showR2: false,
				            visibleInLegend: false
				          }
				        },
				        hAxis: {
        			   	title: 'Repliken',
        			   	format: ' '
        			   },
        			   vAxis: {
        			   	title: vAxisTitle,
        			   }
        			};

        var formatter = new google.visualization.NumberFormat(
    		{fractionDigits: 6});
		formatter.format(data, 1); // Apply formatter to second column
        
        // Create a dashboard.
        var dashboard = new google.visualization.Dashboard(document.getElementById('dashbord-speeches-lineChart'));

        // Create a range slider, passing some options
        var lineChartSpeechesSlider = new google.visualization.ControlWrapper({
          'controlType': 'NumberRangeFilter',
          'containerId': 'filter-speeches-lineChart',
          'options': {
            'filterColumnLabel': germanMetric
          }
        });

        var lineChart = new google.visualization.ChartWrapper({
          'chartType': 'LineChart',
          'containerId': 'chart-speeches-lineChart',
          'options': options
        });
        dashboard.bind(lineChartSpeechesSlider, lineChart);

        // Draw the dashboard.
        dashboard.draw(data);
	};

	that.init = init;
	that.renderSpeechesLineChart = renderSpeechesLineChart;

	return that;
};