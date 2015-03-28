Speakers.SpeakersBarChartView = function(){
	var that = {};
	var speakersSelection = "";
	var speakersAttribute = "";

	var init = function(){
		initListener();
	};

	var initListener = function(){
		$("#selection-speakers").change(speakersSelectionClicked);
	};

	var speakersSelectionClicked = function(){
		$(that).trigger("SpeakersSelectionClicked");
	};

	var renderBarChart = function(speakersInfo){
		var data = new google.visualization.DataTable();
		data.addColumn("string", "Sprecher");
		data.addColumn("number", speakersSelection);
		speakersInfo.sort(sort_by(speakersAttribute,true));
		var array = [];
		for(i = 0; i < speakersInfo.length; i++){
			var row = [speakersInfo[i].name, speakersInfo[i][speakersAttribute]];
			array.push(row);
		}
		data.addRows(array);

		var estimatedHeight = speakersInfo.length * 30;
		if(estimatedHeight < 800){
			estimatedHeight = 800;
		}

		var options = {title:'Sprecher-Statistik',
        			   height: estimatedHeight,
        			   chartArea:{width:'55%',height:'90%'},
				        hAxis: {
        			   	title: speakersSelection
        			   },
        			   animation: {
                   	   	duration: 700,
                   	   	startup: true
                   	   },
        			   vAxis: {
        			   	baseline: 0
        			   }};

        // Create a dashboard.
        var dashboard = new google.visualization.Dashboard(
            document.getElementById('dashbord-speakers-barChart'));

        // Create a range slider, passing some options
        var barChartRangeSlider = new google.visualization.ControlWrapper({
          'controlType': 'NumberRangeFilter',
          'containerId': 'filter-speakers-barChart',
          'options': {
            'filterColumnLabel': speakersSelection
          }
        });

        var barChart = new google.visualization.ChartWrapper({
          'chartType': 'BarChart',
          'containerId': 'chart-speakers-barChart',
          'options': options
        });
        console.log(barChart);

        dashboard.bind(barChartRangeSlider, barChart);

        // Draw the dashboard.
        dashboard.draw(data);
	};

	var setSpeakersSelection = function(){
		speakersSelection = $("#selection-speakers").val();

		if(speakersSelection == "Anwesenheit"){speakersAttribute = "number_of_appearances"};
		if(speakersSelection == "Anwesenheit in Prozent"){speakersAttribute = "appearances_percentage";}
		if(speakersSelection == "Repliken"){speakersAttribute = "number_of_speakers_speeches";}
		if(speakersSelection == "Durchschnittliche Replikenlänge"){speakersAttribute = "average_length_of_speakers_speeches";}
		if(speakersSelection == "Median Replikenlänge"){speakersAttribute = "median_length_of_speakers_speeches";}
		if(speakersSelection == "Maximum Replikenlänge"){speakersAttribute = "maximum_length_of_speakers_speeches";}
		if(speakersSelection == "Minimum Replikenlänge"){speakersAttribute = "minimum_length_of_speakers_speeches";}
	};

	var sort_by = function(field, reverse, primer){

   		var key = primer ? 
        function(x) {return primer(x[field])} : 
       	function(x) {return x[field]};

   		reverse = !reverse ? 1 : -1;

   		return function (a, b) {
       	return a = key(a), b = key(b), reverse * ((a > b) - (b > a));
     	} 
	};

	that.setSpeakersSelection = setSpeakersSelection;
	that.init = init;
	that.renderBarChart = renderBarChart;

	return that;
};