SingleDrama.BarChartDramaView = function(){
	var that = {};
	var actSelection = "";
	var actAttribute = "";
	var scenesSelection = "";
	var scenesAttribute = "";

	var init = function(){
		initListener();
	};

	var initListener = function(){
		$("#selection-act").change(actSelectionClicked);
		$("#selection-scenes").change(scenesSelectionClicked);

	};

	var actSelectionClicked = function(){
		$(that).trigger("ActSelectionClicked");
	};

	var scenesSelectionClicked = function(){
		$(that).trigger("ScenesSelectionClicked");
	};

	var drawChartAct = function(actInfo){
		if(actSelection == "Replikenlänge"){
			drawSpeechesChartAct(actInfo);
			return;
		}
        var data = new google.visualization.DataTable();
        data.addColumn('number', 'Akte');
        if(actSelection == "Szenen" || actSelection == "Sprecher" || actSelection == "Replikenlänge"){
        	data.addColumn('number', actSelection);
        }else{
        	data.addColumn('number', actSelection);
        }
        var array = [];
        if(actAttribute == "average_length_of_speeches_in_act"){
        	for(var i = 0; i < actInfo.length; i++){
        	var row = [(i+1), roundToTwoDecimals(actInfo[i][actAttribute])];
        	array.push(row);
        	}
        } else{
        	if(actAttribute == "speaker_length"){
        		for(var i = 0; i < actInfo.length; i++){
        			var row = [(i+1), actInfo[i].appearing_speakers.length];
        			array.push(row);
        		}
        	}else{
        		for(var i = 0; i < actInfo.length; i++){
	        	var row = [(i+1), actInfo[i][actAttribute]];
	        	array.push(row);
	        	}
        	}	
        }
        console.log(data);
        data.addRows(array);
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
        			   	title: actSelection,
        			   	baseline: 0
        			   },
                   	   animation: {
                   	   	duration: 700,
                   	   	startup: true
                   	   }};

        
        var chart = new google.visualization.ColumnChart(document.getElementById('chart-div-act'));
        var chart_div = document.getElementById('chart-div-act');

        $("#download-png-act").unbind("click");
        $("#download-png-act").on("click", function(){
        	window.open(chart.getImageURI());
        	//drawChartAct(actInfo);
        });

        chart.draw(data, options);

	};

	var setActSelection = function(){
		actSelection = $("#selection-act").val();

		if(actSelection == "Szenen"){actAttribute = "number_of_scenes";}
		if(actSelection == "Sprecher"){actAttribute = "speaker_length";}
		if(actSelection == "Repliken"){actAttribute = "number_of_speeches_in_act";}
		if(actSelection == "Durchschnittliche Replikenlänge"){actAttribute = "average_length_of_speeches_in_act";}
		if(actSelection == "Median Replikenlänge"){actAttribute = "median_length_of_speeches_in_act";}
		if(actSelection == "Maximum Replikenlänge"){actAttribute = "maximum_length_of_speeches_in_act";}
		if(actSelection == "Minimum Replikenlänge"){actAttribute = "minimum_length_of_speeches_in_act";}
	};

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

	var drawChartForScenesInAct = function(divId, scenesInfoPerAct, act){
		if(scenesSelection == "Replikenlänge"){
			drawSpeechesChartScenes(scenesInfoPerAct, act, divId);
			return;
		}
        var data = new google.visualization.DataTable();
        data.addColumn('number', 'Szenen');
        if(scenesSelection == "Sprecher" || scenesSelection == "Replikenlänge"){
        	data.addColumn('number', scenesSelection);
        }else{
        	data.addColumn('number', scenesSelection);
        }
        var array = [];
        if(scenesAttribute == "average_length_of_speeches_in_scene"){
        	for(var i = 0; i < scenesInfoPerAct.length; i++){
        	var row = [(i+1), roundToTwoDecimals(scenesInfoPerAct[i][scenesAttribute])];
        	array.push(row);
        	}
        } else{
        	for(var i = 0; i < scenesInfoPerAct.length; i++){
        	var row = [(i+1), scenesInfoPerAct[i][scenesAttribute]];
        	array.push(row);
        	}
        }
        
        data.addRows(array);
        var ticksArray = [];
        console.log(scenesInfoPerAct);
        for(var k = 0; k < scenesInfoPerAct.length; k++){
        	ticksArray.push(k+1);
        }
        var options = {title:'Szenen-Statistik: Akt ' + act,
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
        			   	title: scenesSelection,
        			   	baseline: 0
        			   },
                   	   animation: {
                   	   	duration: 700,
                   	   	startup: true
                   	   }};
        var chart = new google.visualization.ColumnChart(document.getElementById(divId));

        var chart_div = document.getElementById(divId);

        $("#download-png-" + (act-1)).unbind("click");
        $("#download-png-" + (act-1)).on("click", function(){
        	window.open(chart.getImageURI());
        });

        chart.draw(data, options);
	};

	var drawSpeechesChartScenes = function(scenesInfoPerAct, act, divId){
		console.log(scenesInfoPerAct);
		var data = new google.visualization.DataTable();
		data.addColumn('number', 'Szenen');
		data.addColumn('number', 'Minimum Replikenlänge');
		data.addColumn('number', 'Durchschnittliche Replikenlänge');
		data.addColumn('number', 'Median Replikenlänge');
		data.addColumn('number', 'Maximum Replikenlänge');
		var array = [];
		for(var i = 0; i < scenesInfoPerAct.length; i++){
			var row = [(i+1), scenesInfoPerAct[i].minimum_length_of_speeches_in_scene, 
			roundToTwoDecimals(scenesInfoPerAct[i].average_length_of_speeches_in_scene),
			scenesInfoPerAct[i].median_length_of_speeches_in_scene,
			scenesInfoPerAct[i].maximum_length_of_speeches_in_scene];
			array.push(row);
		}
		console.log(array);
		var ticksArray = [];
        for(var k = 0; k < scenesInfoPerAct.length; k++){
        	ticksArray.push(k+1);
        }
		data.addRows(array);
		        var options = {title:'Szenen-Statistik: Akt ' + act,
        			   height: 600,
        			   width: 1170,
				        hAxis: {
        			   	title: 'Szenen',
        			   	ticks: ticksArray
        			   },
        			   vAxis: {
        			   	baseline: 0
        			   },
                   	   animation: {
                   	   	duration: 700,
                   	   	startup: true
                   	   }};
        var chart = new google.visualization.ColumnChart(document.getElementById(divId));
        $("#download-png-" + (act-1)).unbind("click");
        $("#download-png-" + (act-1)).on("click", function(){
        	window.open(chart.getImageURI());
        });
        chart.draw(data, options);
	};

	var setScenesSelection = function(){
		scenesSelection = $("#selection-scenes").val();

		if(scenesSelection == "Sprecher"){scenesAttribute = "number_of_speakers"};
		if(scenesSelection == "Repliken"){scenesAttribute = "number_of_speeches_in_scene";}
		if(scenesSelection == "Durchschnittliche Replikenlänge"){scenesAttribute = "average_length_of_speeches_in_scene";}
		if(scenesSelection == "Median Replikenlänge"){scenesAttribute = "median_length_of_speeches_in_scene";}
		if(scenesSelection == "Maximum Replikenlänge"){scenesAttribute = "maximum_length_of_speeches_in_scene";}
		if(scenesSelection == "Minimum Replikenlänge"){scenesAttribute = "minimum_length_of_speeches_in_scene";}
	};

	var roundToTwoDecimals = function(number){
		number = (Math.round(number * 100)/100).toFixed(2);
		return parseFloat(number)
	};

	that.init = init;
	that.drawChartAct = drawChartAct;
	that.setActSelection = setActSelection;
	that.drawChartScenes = drawChartScenes;
	that.setScenesSelection = setScenesSelection;

	return that;
};