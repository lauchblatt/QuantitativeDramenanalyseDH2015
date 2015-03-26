Speakers.SpeechesDominanceView = function(){
	var that = {};

	var renderPieChart = function(speakersInfo){
		var data = new google.visualization.DataTable();
		data.addColumn("string", "Sprecher");
		data.addColumn("number", "Zahl der Repliken");
		var array = [];
		for(i = 0; i < speakersInfo.length; i++){
			var row = [speakersInfo[i].name, speakersInfo[i].number_of_speakers_speeches];
			array.push(row);
		}
		data.addRows(array);

		var options = {
		  height: 1000,
          title: 'Replikendominanz',
          is3D: true,
        };

        // Create a dashboard.
        var dashboard = new google.visualization.Dashboard(
            document.getElementById('dashboard-div'));

        // Create a range slider, passing some options
        var donutRangeSlider = new google.visualization.ControlWrapper({
          'controlType': 'NumberRangeFilter',
          'containerId': 'filter-div',
          'options': {
            'filterColumnLabel': 'Zahl der Repliken'
          }
        });

        var pieChart = new google.visualization.ChartWrapper({
          'chartType': 'PieChart',
          'containerId': 'chart-div',
          'options': options
        });

        dashboard.bind(donutRangeSlider, pieChart);

        // Draw the dashboard.
        dashboard.draw(data);
	};

	that.renderPieChart = renderPieChart;

	return that;
};