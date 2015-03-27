MultipleDramas.YearView = function(){
	var that = {};

	var renderScatterChart = function(dramas){
		var data = new google.visualization.DataTable();
		data.addColumn("number", "Jahr");
		data.addColumn("number", "Konfigurationsdichte");
		data.addColumn({'type': 'string', 'role': 'tooltip', 'p': {'html': true}});
		var array = [];
		for(i = 0; i < dramas.length; i++){
			var row = [dramas[i].year, dramas[i].configuration_density,
			createTooltip(dramas[i])];
			array.push(row);
		}
		data.addRows(array);

		var options = {
          title: 'Epochenverlauf',
          height: 700,
          tooltip: { isHtml: true },
          hAxis: {title: 'Jahr', format: ''},
          vAxis: {title: 'Konfigurationsdichte'},
          legend: 'none',
          explorer: {},
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
				        }
        };

        var chart = new google.visualization.ScatterChart(document.getElementById('chart-div'));

        chart.draw(data, options);
	};

	var createTooltip = function(drama){
		var divBegin = "<div class='tooltip-test'>"
		var headline = "<div>" + drama.title + " von " + getLastName(drama.author) + "</div>";
		var year = "<div>" + "<b>Jahr: </b>" + drama.year + "</div>";
		var data = "<div>" + "<b>Konfigurationsdichte: </b>" + drama.configuration_density + "</div>";
		var divEnd = "</div>";
		return (divBegin + headline + year + data + divEnd); 
	};

	var getLastName = function(author){
		author = author.slice(0, author.indexOf(","));
		return author;
	};

	that.renderScatterChart = renderScatterChart;

	return that;
};