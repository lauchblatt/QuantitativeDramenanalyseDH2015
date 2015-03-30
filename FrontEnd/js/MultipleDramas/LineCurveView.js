MultipleDramas.LineCurveView = function(){
	var that = {};

	var render = function(distribution){
		var data = new google.visualization.DataTable();
		data.addColumn("number", "Replikenlänge in Worten");
		data.addColumn("number", 'Replikenhäufigkeit');
		var array = [];
		for(var key in distribution){
			var row = [parseInt(key), distribution[key]];
			array.push(row);
		}
		data.addRows(array);

		var options = {
		  height: 700,
		  width: 1170,
		  animation: {
		  	duration: 1000
		  },
		  chartArea:{width:'75%',height:'80%'},
          title: 'Replikenlängen, Relative Häufigkeit',
          curveType: 'function',
          legend: {
          	position: 'none'
          },
          hAxis : {
          	title: 'Replikenlänge'
          },
          vAxis: {
          	title: 'Häufigkeit'
          }
        };

        var dashboard = new google.visualization.Dashboard(
            document.getElementById('curve-dashbord'));

        var rangeSlider = new google.visualization.ControlWrapper({
          'controlType': 'NumberRangeFilter',
          'containerId': 'curve-controls',
          'options': {
            'filterColumnLabel': 'Replikenlänge in Worten'
          }
        });

        var chart = new google.visualization.ChartWrapper({
          'chartType': 'LineChart',
          'containerId': 'curve-chart',
          'options': options
        });

        dashboard.bind(rangeSlider, chart);

        dashboard.draw(data);
	};

	that.render = render;

	return that;
};