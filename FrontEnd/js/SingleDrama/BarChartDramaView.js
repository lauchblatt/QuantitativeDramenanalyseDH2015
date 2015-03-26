SingleDrama.BarChartDramaView = function(){
	var that = {};
	var actSelection = "";
	var actAttribute = "";

	var init = function(){
		initListener();
	};

	var initListener = function(){
		$("#selection-act").change(actSelectionClicked);
	};

	var actSelectionClicked = function(){
		$(that).trigger("ActSelectionClicked");
	};

	var drawChartAct = function(actInfo){
		if(actSelection == "Replikenlänge"){
			drawSpeechesChartAct(actInfo);
			return;
		}
        var data = new google.visualization.DataTable();
        data.addColumn('string', 'Akte');
        if(actSelection == "Szenen" || actSelection == "Sprecher" || actSelection == "Replikenlänge"){
        	data.addColumn('number', 'Anzahl der ' + actSelection);
        }else{
        	data.addColumn('number', actSelection);
        }
        var array = [];
        for(var i = 0; i < actInfo.length; i++){
        	var row = ['Akt ' + (i+1), actInfo[i][actAttribute]];
        	array.push(row);
        }
        data.addRows(array);
        var options = {title:'Akt-Statistik',
        			   height: 600,
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
		data.addColumn('string', 'Akte');
		data.addColumn('number', 'Minimum Replikenlänge');
		data.addColumn('number', 'Durchschnittliche Replikenlänge');
		data.addColumn('number', 'Median Replikenlänge');
		data.addColumn('number', 'Maximum Replikenlänge');
		var array = [];
		for(var i = 0; i < actInfo.length; i++){
			var row = ['Akt ' + (i+1), actInfo[i].minimum_length_of_speeches_in_act, 
			actInfo[i].average_length_of_speeches_in_act,
			actInfo[i].median_length_of_speeches_in_act,
			actInfo[i].maximum_length_of_speeches_in_act];
			array.push(row);
		}
		data.addRows(array);
		        var options = {title:'Akt-Statistik',
        			   height: 600,
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

	var getActSelection = function(){
		return actSelection;
	};

	that.init = init;
	that.drawChartAct = drawChartAct;
	that.setActSelection = setActSelection;
	that.getActSelection = getActSelection;

	return that;
};