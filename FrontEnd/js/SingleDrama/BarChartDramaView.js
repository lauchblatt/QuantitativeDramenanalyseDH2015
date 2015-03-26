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

	var drawBarChart = function(actInfo){
		// Create the data table.
        var data = new google.visualization.DataTable();
        data.addColumn('string', 'Akte');
        data.addColumn('number', 'Anzahl der ' + actSelection);
        var array = [];
        for(var i = 0; i < actInfo.length; i++){
        	var column = ['Akt ' + (i+1), actInfo[i][actAttribute]];
        	array.push(column);
        }
        console.log(array);
        data.addRows(array);

        // Set chart options
        var options = {title:'Akt-Statistik',
        			   height: 600,
        			   vAxis: {
        			   	baseline: 0
        			   },
                   	   animation: {
                   	   	duration: 700,
                   	   	startup: true
                   	   }};

        // Instantiate and draw our chart, passing in some options.
        var chart = new google.visualization.ColumnChart(document.getElementById('chart-div-act'));
        chart.draw(data, options);

	};

	var setActSelection = function(){
		actSelection = $("#selection-act").val();

		if(actSelection == "Szenen"){actAttribute = "number_of_scenes";}
		//TODO Number of Speakers if(actSelection == "Sprecher")
		if(actSelection == "Repliken"){actAttribute = "number_of_speeches_in_act";}
	};

	var getActSelection = function(){
		return actSelection;
	};

	that.init = init;
	that.drawBarChart = drawBarChart;
	that.setActSelection = setActSelection;
	that.getActSelection = getActSelection;

	return that;
};