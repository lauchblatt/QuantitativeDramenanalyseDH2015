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
        	data.addColumn('number', 'Anzahl der ' + actSelection);
        }else{
        	data.addColumn('number', actSelection);
        }
        var array = [];
        for(var i = 0; i < actInfo.length; i++){
        	var row = [(i+1), actInfo[i][actAttribute]];
        	array.push(row);
        }
        console.log(data);
        data.addRows(array);
        var options = {title:'Akt-Statistik',
        			   height: 600,
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
        			   	baseline: 0
        			   },
                   	   animation: {
                   	   	duration: 700,
                   	   	startup: true
                   	   }};
        var chart = new google.visualization.ColumnChart(document.getElementById('chart-div-act'));
        chart.draw(data, options);

	};

	var drawSpeechesChartAct = function(actInfo){
		var data = new google.visualization.DataTable();
		data.addColumn('number', 'Akte');
		data.addColumn('number', 'Minimum Replikenlänge');
		data.addColumn('number', 'Durchschnittliche Replikenlänge');
		data.addColumn('number', 'Median Replikenlänge');
		data.addColumn('number', 'Maximum Replikenlänge');
		var array = [];
		for(var i = 0; i < actInfo.length; i++){
			var row = [(i+1), actInfo[i].minimum_length_of_speeches_in_act, 
			actInfo[i].average_length_of_speeches_in_act,
			actInfo[i].median_length_of_speeches_in_act,
			actInfo[i].maximum_length_of_speeches_in_act];
			array.push(row);
		}
		data.addRows(array);
		        var options = {title:'Akt-Statistik',
        			   height: 600,
        			   hAxis: {
        			   	title: 'Akte'
        			   },
                   	   animation: {
                   	   	duration: 700,
                   	   	startup: true
                   	   }};
        var chart = new google.visualization.ColumnChart(document.getElementById('chart-div-act'));
        chart.draw(data, options);
	};

	var setActSelection = function(){
		actSelection = $("#selection-act").val();

		if(actSelection == "Szenen"){actAttribute = "number_of_scenes";}
		//TODO Number of Speakers if(actSelection == "Sprecher")
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
        	data.addColumn('number', 'Anzahl der ' + scenesSelection);
        }else{
        	data.addColumn('number', scenesSelection);
        }
        var array = [];
        for(var i = 0; i < scenesInfoPerAct.length; i++){
        	var row = [(i+1), scenesInfoPerAct[i][scenesAttribute]];
        	array.push(row);
        }
        data.addRows(array);
        var ticksArray = [];
        for(var k = 0; k < scenesInfoPerAct.length; k++){
        	ticksArray.push(k+1);
        }
        var options = {title:'Szenen-Statistik: Akt ' + act,
        			   height: 600,
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
        			   	baseline: 0
        			   },
                   	   animation: {
                   	   	duration: 700,
                   	   	startup: true
                   	   }};
        var chart = new google.visualization.ColumnChart(document.getElementById(divId));
        chart.draw(data, options);
	};

	var drawSpeechesChartScenes = function(scenesInfoPerAct, act, divId){
		var data = new google.visualization.DataTable();
		data.addColumn('number', 'Szenen');
		data.addColumn('number', 'Minimum Replikenlänge');
		data.addColumn('number', 'Durchschnittliche Replikenlänge');
		data.addColumn('number', 'Median Replikenlänge');
		data.addColumn('number', 'Maximum Replikenlänge');
		var array = [];
		for(var i = 0; i < scenesInfoPerAct.length; i++){
			var row = [(i+1), scenesInfoPerAct[i].minimum_length_of_speeches_in_scene, 
			scenesInfoPerAct[i].average_length_of_speeches_in_scene,
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

	that.init = init;
	that.drawChartAct = drawChartAct;
	that.setActSelection = setActSelection;
	that.drawChartScenes = drawChartScenes;
	that.setScenesSelection = setScenesSelection;

	return that;
};