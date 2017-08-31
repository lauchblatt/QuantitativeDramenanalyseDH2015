ActsScenes.ActsScenesView = function(){
	var that = {};
	var metricsForActs = []

	var init = function(metricsActs){
		metricsForActs = metricsActs
		initListener()
	};

	var initListener = function(){
		$("#selection-act-bar-metric").change(renderActBars);
		$("#selection-act-bar-normalisation").change(renderActBars);
	};

	var renderActBars = function(){
		metricSelection = $("#selection-act-bar-metric").val();
		normalisationSelection = $("#selection-act-bar-normalisation").val()
		metric = transformGermanMetric(metricSelection);
		normalisation = transformGermanMetric(normalisationSelection)
		metrics = getActsMetricsByName(normalisation, metric)
		drawBarChartAct(normalisationSelection, metricSelection, metrics)
	};

	//Loop to render all Graphs for Scenes dynamically
	var drawChartScenes = function(scenesInfo){
		$charts_scenes = $("#charts-scenes");
		for(var act = 0; act < scenesInfo.length; act++){
			$div_chart = $("<div></div>");
			$div_chart.addClass("scenes-chart");
			$div_chart.attr("id", "chart-div-scenes-" + act);
			$charts_scenes.append($div_chart);
			var $button = $("<button class='btn btn-primary png-download'></button>");
			$button.attr("id", "download-png-" + act);
			$button.text("Download PNG");
			var $buttonDiv = $("<div>").addClass("container").append($button);
			$charts_scenes.append($buttonDiv);
			drawChartForScenesInAct(("chart-div-scenes-" + act), scenesInfo[act], (act+1));
		}
	};

	var getActsMetricsByName = function(normalisation, metricName){
		var specificMetricsForActs = []
		for(var i = 0; i < metricsForActs.length; i++){
			metric = metricsForActs[i][normalisation][metricName];
			actName = (i+1).toString() + " .Akt";
			tuple = [actName, metric, (Math.round(metric * 100) / 100).toString()];
			specificMetricsForActs.push(tuple);
		}
		return specificMetricsForActs;
	};

	var drawBarChartAct = function(normalisation, metricName, numberMetricPairs){
		var vAxisTitle = metricName + " - " + normalisation
		var data = new google.visualization.DataTable();
		data.addColumn("string", "Act-Number")
		data.addColumn("number", metricName)
		data.addColumn({type:'string', role:'annotation'})
        data.addRows(numberMetricPairs);
        var options = {title:'Akt-Statistik',
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
        			   	baseline: 0
        			   },
                   	   animation: {
                   	   	duration: 700,
                   	   	startup: true
                   	   }};

        
        var chart = new google.visualization.ColumnChart(document.getElementById('chart-div-act'));
        var chart_div = document.getElementById('chart-div-act');

        chart.draw(data, options);

	};

	var transformGermanMetric = function(name){
		console.log(name)
		switch(name) {
		    case "Polarität (gewichtet)":
		        return "polaritySentiWS";
		        break;
		    case "Polarität (Wortanzahl)":
		        return "polaritySentiWSDichotom";
		        break;
		    case "Positiv (gewichtet)":
		        return "positiveSentiWS";
		        break;
		    case "Positiv (Wortanzahl)":
		        return "positiveSentiWSDichotom";
		        break;
		    case "Negativ (gewichtet)":
		        return "negativeSentiWS";
		        break;
		    case "Negativ (Wortanzahl)":
		        return "negativeSentiWSDichotom";
		        break;
		    case "Zorn":
		        return "anger";
		        break;
		    case "Erwartung":
		        return "anticipation";
		        break;
		    case "Ekel":
		        return "disgust";
		        break;
		    case "Angst":
		        return "fear";
		        break;
		    case "Freude":
		        return "joy";
		        break;
		    case "Traurigkeit":
		        return "sadness";
		        break;
		    case "Überraschung":
		        return "surprise";
		        break;
		    case "Vertrauen":
		        return "trust";
		        break;
		    case "Absolut":
		        return "metricsTotal";
		        break;
		    case "Normalisiert an Anzahl aller Wörter":
		        return "metricsNormalisedLengthInWords";
		        break;
		    case "Normalisiert an Sentiment-Tragenden Wörtern":
		        return "metricsNormalisedSBWs";
		        break;
		    default:
		        console.log("ERROR")
		    }
	};

	that.init = init;
	that.render = render;

	return that;
};