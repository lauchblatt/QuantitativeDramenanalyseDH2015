MultipleDramas.YearView = function(){
	var that = {};
	var yearSelection = "";
	var yearAttribute = "";

	var init = function(){
		initListener();
		$("#chart-div-year").css("display", "none");
	};

	var initListener = function(){
		$("#selection-year").change(yearSelectionClicked);
	};

	var yearSelectionClicked = function(){
		$(that).trigger("YearSelectionClicked");
	};

	var renderScatterChart = function(dramas){
		$("#chart-div-year").css("display", "none");
		var data = new google.visualization.DataTable();
		data.addColumn("number", "Jahr");
		data.addColumn("number", yearSelection);
		data.addColumn({'type': 'string', 'role': 'tooltip', 'p': {'html': true}});
		var array = [];
		for(i = 0; i < dramas.length; i++){
			var row = [dramas[i].year, dramas[i][yearAttribute],
			createTooltip(dramas[i])];
			array.push(row);
		}
		data.addRows(array);

		var options = {
          title: 'Epochenverlauf',
          height: 700,
          width: 1000,
          tooltip: { isHtml: true },
          hAxis: {title: 'Jahr', format: ' '},
          vAxis: {title: yearSelection},
          explorer: {},
          legend: 'none',
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

        var chart = new google.visualization.ScatterChart(document.getElementById('chart-div-year'));

        chart.draw(data, options);
        $("#chart-div-year").fadeIn(1000);
	};

	var createTooltip = function(drama){
		var divBegin = "<div class='tooltip-test'>"
		var headline = "<div>" + drama.title + " von " + getLastName(drama.author) + "</div>";
		var year = "<div>" + "<b>Jahr: </b>" + drama.year + "</div>";
		var data = "<div>" + "<b>" + yearSelection + ": </b>" + drama[yearAttribute] + "</div>";
		var divEnd = "</div>";
		return (divBegin + headline + year + data + divEnd); 
	};

	var setYearSelection = function(){
		yearSelection = $("#selection-year").val();

		if(yearSelection == "Szenenanzahl"){yearAttribute = "number_of_scenes"};
		if(yearSelection == "Replikenanzahl"){yearAttribute = "number_of_speeches_in_drama";}
		//TODO Sprecheranzahl
		if(yearSelection == "Konfigurationsdichte"){yearAttribute = "configuration_density";}
		if(yearSelection == "Durchschnittliche Replikenlänge"){yearAttribute = "average_length_of_speeches_in_drama";}
		if(yearSelection == "Median Replikenlänge"){yearAttribute = "median_length_of_speeches_in_drama";}
		if(yearSelection == "Maximum Replikenlänge"){yearAttribute = "maximum_length_of_speeches_in_drama";}
		if(yearSelection == "Minimum Replikenlänge"){yearAttribute = "minimum_length_of_speeches_in_drama";}

		console.log(yearSelection);
		console.log(yearAttribute);
	};

	var getLastName = function(author){
		author = author.slice(0, author.indexOf(","));
		return author;
	};

	that.renderScatterChart = renderScatterChart;
	that.setYearSelection = setYearSelection;
	that.init = init;

	return that;
};