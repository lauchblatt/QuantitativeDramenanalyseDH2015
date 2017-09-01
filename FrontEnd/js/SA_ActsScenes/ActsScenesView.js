ActsScenes.ActsScenesView = function(){
	var that = {};
	var metricsForActs = [];
	var actsProportionData = {};

	var init = function(metricsActs, proportionDataForActs){
		metricsForActs = metricsActs;
		actsProportionData = proportionDataForActs;

		initNumberOfActs(actsProportionData.length)
		initListener()

	};

	var initNumberOfActs = function(numberOfActs){
		$select = $("#selection-acts-pie-number");
		for(i = 0; i < numberOfActs; i++){
			option = $("<option></option>")
			actNumber = i + 1;
			option.text(actNumber.toString() + " .Akt");
			$select.append(option);
		}
	};

	var initListener = function(){
		$("#selection-act-bar-metric").change(renderActsBars);
		$("#selection-act-bar-normalisation").change(renderActsBars);

		$("#selection-acts-pie-number").change(renderActPieChart);
		$("#selection-acts-pie-metric").change(renderActPieChart);
		$("#selection-acts-pie-type").change(renderActPieChart);
	};

	var renderActPieChart = function(){
		var actNumber = $("#selection-acts-pie-number").val();
		var metric = $("#selection-acts-pie-metric").val();
		var type = $("#selection-acts-pie-type").val();
		actNumber = parseInt(actNumber) - 1;
		metric = transformGermanMetric(metric);
		type = transformGermanMetric(type);
		drawActPieChart(actNumber, type, metric);
	};

	var drawActPieChart = function(actNumber, proportionType, metricName){
		var data = new google.visualization.DataTable();
		data.addColumn("string", "Category");
		data.addColumn("number", "Count");

        data.addRows(actsProportionData[actNumber][proportionType][metricName]);
        var options = {
		  height: 600,
      		width: 1000,
      		chartArea:{width:'70%',height:'75%'},
          	title: 'Sentiment-Anteile pro Akt',
          	is3D: true,
        	};
        var chart = new google.visualization.PieChart(document.getElementById('chart-div-act-pie'))
        chart.draw(data, options)
	};

	var renderActsBars = function(){
		metricSelection = $("#selection-act-bar-metric").val();
		normalisationSelection = $("#selection-act-bar-normalisation").val()
		metric = transformGermanMetric(metricSelection);
		normalisation = transformGermanMetric(normalisationSelection);
		metrics = getActsMetricsByName(normalisation, metric);
		drawBarChartAct(normalisationSelection, metricSelection, metrics);
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
		    case "Emotion vorhanden":
		    	return "emotionPresent";
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
		    case "Emotionen":
		    	return "emotions";
		    	break;
		    case "Verteilung von Sentiment-Tragenden Wörtern":
		    	return "normalisedSBWs";
		    	break;
		    case "Verteilung von allen Wörtern":
		    	return "normalisedAllWords";
		    	break;
		    default:
		        console.log("ERROR")
		    }
	};

	that.init = init;
	that.renderActsBars = renderActsBars;
	that.renderActPieChart = renderActPieChart;

	return that;
};