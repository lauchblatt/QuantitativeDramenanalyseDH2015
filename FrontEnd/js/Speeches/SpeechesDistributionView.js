Speeches.SpeechesDistributionView = function(){
	var that = {};

	var render = function(scenesInfo){

		var data = new google.visualization.DataTable();
		data.addColumn("string", "Replik");
		data.addColumn("number", 'Replikenlänge in Worten');
		var array = [];
		var iterator = 0;
		for(act = 0; act < scenesInfo.length; act++){
			for(scene = 0; scene < scenesInfo[act].length; scene++){
				if(scenesInfo[act][scene].speeches !== undefined){
					for(speech = 0; speech < scenesInfo[act][scene].speeches.length; speech++){
						var row = ['Replikenlänge in Worten ' + iterator, scenesInfo[act][scene].speeches[speech]['length']];
						array.push(row);
						iterator++;
					}
				}
			}
		}
		data.addRows(array);

		var options = {
		  height: 700,
		  width: 1170,
		  animation: {
		  	duration: 1000
		  },
		  chartArea:{width:'75%',height:'80%'},
          title: 'Histogramm - Replikenverteilung der Längen in Worten'
        };

        var dashboard = new google.visualization.Dashboard(
            document.getElementById('distribution-dashbord'));

        // Create a range slider, passing some options
        var rangeSlider = new google.visualization.ControlWrapper({
          'controlType': 'NumberRangeFilter',
          'containerId': 'distribution-controls',
          'options': {
            'filterColumnLabel': 'Replikenlänge in Worten'
          }
        });

        // Create a pie chart, passing some options
        var chart = new google.visualization.ChartWrapper({
          'chartType': 'Histogram',
          'containerId': 'distribution-chart',
          'options': options
        });

        // Establish dependencies, declaring that 'filter' drives 'pieChart',
        // so that the pie chart will only display entries that are let through
        // given the chosen slider range.
        dashboard.bind(rangeSlider, chart);

        // Draw the dashboard.
        dashboard.draw(data);

	};

	that.render = render;

	return that;
};