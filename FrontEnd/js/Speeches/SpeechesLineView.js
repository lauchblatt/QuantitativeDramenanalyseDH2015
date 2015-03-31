Speeches.SpeechesLineView = function(){
	var that = {};

	var render = function(distribution){
		var data = new google.visualization.DataTable();
		data.addColumn("number", "Replikenlänge in Worten");
		data.addColumn("number", 'Replikenhäufigkeit');
		var array = [];
		for(var key in distribution){
			var row = [parseInt(key), distribution[key]];
			console.log(row);
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
          title: 'Replikenlängen, Absolute Häufigkeit',
          curveType: 'function',
          legend: {
          	position: 'none'
          },
          hAxis : {
          	title: 'Replikenlänge'
          },
          vAxis: {
          	title: 'Absolute Häufigkeit',
            baseline: 0
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

        var chart_div = document.getElementById('curve-chart');

        $("#pngButton").unbind("click");
        $("#pngButton").on("click", function(){
          chart_div.innerHTML = '<img src="' + chart.getChart().getImageURI() + '">';
          console.log(chart_div.innerHTML);
          window.open(chart.getChart().getImageURI());
          render(distribution);
        });

        dashboard.draw(data);
	};

	that.render = render;

	return that;
};